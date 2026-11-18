import { NextRequest, NextResponse } from 'next/server';

// A shop domain is a bare `<shop>.myshopify.com` host name. It is parsed with URL and
// the input must equal the parsed host exactly, so nothing after a '#', '?', '/', '@'
// or ':' (or any case or whitespace the parser would normalise away) is accepted.
const SHOP_HOSTNAME = /^[a-z0-9][a-z0-9-]*\.myshopify\.com$/;

function parseShopDomain(value: unknown): string | null {
  if (typeof value !== 'string') return null;
  let url: URL;
  try {
    url = new URL(`https://${value}`);
  } catch {
    return null;
  }
  if (url.protocol !== 'https:' || url.username || url.password || url.port) return null;
  if (url.pathname !== '/' || url.search || url.hash) return null;
  if (url.hostname !== value || !SHOP_HOSTNAME.test(url.hostname)) return null;
  return url.hostname;
}

export async function POST(request: NextRequest) {
  try {
    const { installation_id, shop_domain, access_token } = await request.json();

    console.log('Test connection request:', {
      installation_id,
      shop_domain,
      access_token: access_token ? '***PROVIDED***' : 'MISSING'
    });

    if (!installation_id || !shop_domain || !access_token) {
      console.error('Missing parameters:', { installation_id, shop_domain, has_token: !!access_token });
      return NextResponse.json(
        {
          success: false,
          error: 'Missing required parameters'
        },
        { status: 400 }
      );
    }

    // Validate shop domain format
    const shopHost = parseShopDomain(shop_domain);
    if (!shopHost) {
      return NextResponse.json(
        {
          success: false,
          error: 'Invalid shop domain format'
        },
        { status: 400 }
      );
    }

    // Test connection by fetching shop information
    console.log(`Testing connection to: https://${shopHost}/admin/api/2023-10/shop.json`);

    const shopResponse = await fetch(`https://${shopHost}/admin/api/2023-10/shop.json`, {
      redirect: 'manual', // never forward the token to another host
      headers: {
        'X-Shopify-Access-Token': access_token,
        'Content-Type': 'application/json',
      },
    });

    console.log('Shopify API response status:', shopResponse.status);

    if (!shopResponse.ok) {
      const errorText = await shopResponse.text();
      console.error('Shopify API error:', {
        status: shopResponse.status,
        statusText: shopResponse.statusText,
        body: errorText
      });

      let errorMessage = 'Connection failed';

      if (shopResponse.status === 401) {
        errorMessage = 'Invalid access token - check your token is correct and has not expired';
      } else if (shopResponse.status === 403) {
        errorMessage = 'Insufficient permissions - token needs read_orders and write_shipping scopes';
      } else if (shopResponse.status === 404) {
        errorMessage = 'Shop not found - check your shop domain is correct';
      }

      return NextResponse.json({
        success: false,
        error: errorMessage,
        details: errorText,
        status_code: shopResponse.status,
      });
    }

    const shopData = await shopResponse.json();
    const shop = shopData.shop;

    // Test API access by checking available endpoints
    const apiResponse = await fetch(`https://${shopHost}/admin/api/2023-10.json`, {
      redirect: 'manual',
      headers: {
        'X-Shopify-Access-Token': access_token,
      },
    });

    let availableEndpoints: string[] = [];
    if (apiResponse.ok) {
      const apiData = await apiResponse.json();
      availableEndpoints = Object.keys(apiData);
    }

    return NextResponse.json({
      success: true,
      shop_name: shop?.name || shop_domain,
      shop_domain: shop?.domain || shop_domain,
      shop_email: shop?.email,
      shop_currency: shop?.currency,
      shop_timezone: shop?.iana_timezone,
      available_endpoints: availableEndpoints,
      connection_time: new Date().toISOString(),
    });

  } catch (error) {
    console.error('Connection test error:', error);

    return NextResponse.json(
      {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred'
      },
      { status: 500 }
    );
  }
}
