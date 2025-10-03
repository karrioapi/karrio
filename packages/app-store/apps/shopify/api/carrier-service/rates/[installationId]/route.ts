import { NextRequest, NextResponse } from 'next/server';
import { generateAppJWT } from '@karrio/hooks/app-auth';
import crypto from 'crypto';

// Convert weight from grams to kg
function convertWeight(grams: number): number {
  return grams / 1000;
}

// Convert dimensions from cm to cm (Shopify uses cm)
function convertDimension(cm: number): number {
  return cm || 10; // Default 10cm if not provided
}

// Add days to a date for delivery estimates
function addDays(date: Date, days: number): Date {
  const result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
}

interface RouteContext {
  params: {
    installationId: string;
  };
}

export async function POST(request: NextRequest, { params }: RouteContext) {
  try {
    const body = await request.text();
    const rateRequest = JSON.parse(body);

    console.log(`Rate request for installation: ${params.installationId}`);

    // Extract rate data from Shopify request
    const { rate: rateData } = rateRequest;
    if (!rateData?.origin || !rateData?.destination || !rateData?.items) {
      return NextResponse.json({ rates: [] });
    }

    const { origin, destination, items, currency = 'USD' } = rateData;

    // Generate JWT for this installation
    // For server-side, we need to get user/org context from environment or request
    const userId = process.env.KARRIO_SYSTEM_USER_ID || 'system';
    const orgId = process.env.KARRIO_SYSTEM_ORG_ID || 'system';

    const jwt = await generateAppJWT(
      'shopify',
      params.installationId,
      userId,
      orgId,
      ['read', 'write']
    );

    // Calculate total weight and value for the single parcel
    const totalWeight = items.reduce((sum: number, item: any) =>
      sum + (item.grams || 0) * (item.quantity || 1), 0
    );

    const totalValue = items.reduce((sum: number, item: any) =>
      sum + (parseFloat(item.price || '0') * (item.quantity || 1)), 0
    );

    // Use the largest dimensions from all items for the parcel
    const maxWidth = Math.max(...items.map((item: any) => convertDimension(item.width)));
    const maxHeight = Math.max(...items.map((item: any) => convertDimension(item.height)));
    const maxLength = Math.max(...items.map((item: any) => convertDimension(item.length)));

    // Build Karrio shipment with ONE parcel containing all items
    const shipment = {
      shipper: {
        address_line_1: origin.address1 || '',
        address_line_2: origin.address2 || '',
        city: origin.city || '',
        state_code: origin.province || '',
        postal_code: origin.postal_code || origin.zip || '',
        country_code: origin.country || '',
        company_name: origin.company || '',
        person_name: origin.name || '',
        phone_number: origin.phone || '',
        email: origin.email || '',
      },
      recipient: {
        address_line_1: destination.address1 || '',
        address_line_2: destination.address2 || '',
        city: destination.city || '',
        state_code: destination.province || '',
        postal_code: destination.postal_code || destination.zip || '',
        country_code: destination.country || '',
        company_name: destination.company || '',
        person_name: destination.name || '',
        phone_number: destination.phone || '',
        email: destination.email || '',
      },
      parcels: [{
        weight: convertWeight(totalWeight),
        width: maxWidth,
        height: maxHeight,
        length: maxLength,
        weight_unit: 'KG' as const,
        dimension_unit: 'CM' as const,
        description: `Package with ${items.length} item(s)`,
        value_amount: totalValue,
        value_currency: currency,
        // Map Shopify items to commodities within the single parcel
        items: items.map((item: any) => ({
          weight: convertWeight((item.grams || 0) * (item.quantity || 1)),
          weight_unit: 'KG' as const,
          title: item.title || item.name || 'Item',
          description: item.title || item.name || 'Shopify item',
          quantity: item.quantity || 1,
          sku: item.sku || null,
          value_amount: item.price ? parseFloat(item.price) : 0,
          value_currency: currency,
          metadata: {
            shopify_variant_id: item.variant_id,
            shopify_product_id: item.product_id,
            shopify_item_id: item.id,
          },
        })),
      }],
    };

    // Call Karrio API with JWT
    const ratesResponse = await fetch(`${process.env.KARRIO_API_URL}/v1/rates`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${jwt}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(shipment),
    });

    if (!ratesResponse.ok) {
      console.error('Karrio API error:', ratesResponse.status);
      return NextResponse.json({ rates: [] });
    }

    const ratesData = await ratesResponse.json();
    const rates = ratesData.rates || [];

    // Convert Karrio rates to Shopify format
    const shopifyRates = rates.map((rate: any) => {
      const minDeliveryDate = rate.transit_days
        ? addDays(new Date(), rate.transit_days)
        : null;
      const maxDeliveryDate = rate.transit_days
        ? addDays(new Date(), rate.transit_days + 1)
        : null;

      return {
        service_name: `${rate.carrier_name} ${rate.service}`,
        service_code: rate.service.toLowerCase().replace(/\s+/g, '_'),
        total_price: Math.round(rate.total_charge * 100), // Convert to cents
        currency: rate.currency || currency,
        min_delivery_date: minDeliveryDate?.toISOString() || null,
        max_delivery_date: maxDeliveryDate?.toISOString() || null,
        description: rate.transit_days
          ? `${rate.service} delivery in ${rate.transit_days} business days`
          : `${rate.service} delivery`,
      };
    });

    return NextResponse.json({ rates: shopifyRates });

  } catch (error) {
    console.error('Rate calculation error:', error);
    return NextResponse.json({ rates: [] });
  }
}

// Health check
export async function GET(request: NextRequest, { params }: RouteContext) {
  return NextResponse.json({
    status: 'healthy',
    service: 'Karrio Shopify Carrier Service',
    installation: params.installationId,
    timestamp: new Date().toISOString(),
  });
}

// CORS preflight
export async function OPTIONS() {
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, X-Shopify-Hmac-Sha256',
    },
  });
}
