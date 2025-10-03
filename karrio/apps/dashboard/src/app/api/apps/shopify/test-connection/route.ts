import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
    try {
        const { shop_domain, access_token } = await request.json();

        if (!shop_domain || !access_token) {
            return NextResponse.json({
                success: false,
                error: 'Missing shop_domain or access_token'
            }, { status: 400 });
        }

        // Validate shop domain format
        if (!shop_domain.endsWith('.myshopify.com')) {
            return NextResponse.json({
                success: false,
                error: 'Invalid shop domain format. Must end with .myshopify.com'
            }, { status: 400 });
        }

        // Test the connection by making a request to Shopify's shop API
        const shopifyUrl = `https://${shop_domain}/admin/api/2023-04/shop.json`;

        const response = await fetch(shopifyUrl, {
            method: 'GET',
            headers: {
                'X-Shopify-Access-Token': access_token,
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            let errorMessage = 'Connection failed';

            if (response.status === 401) {
                errorMessage = 'Invalid access token';
            } else if (response.status === 403) {
                errorMessage = 'Access forbidden - check token permissions';
            } else if (response.status === 404) {
                errorMessage = 'Shop not found';
            }

            return NextResponse.json({
                success: false,
                error: errorMessage,
                status: response.status
            }, { status: 400 });
        }

        const shopData = await response.json();

        return NextResponse.json({
            success: true,
            message: 'Connection successful',
            shop: {
                name: shopData.shop?.name,
                domain: shopData.shop?.domain,
                email: shopData.shop?.email,
                currency: shopData.shop?.currency,
                timezone: shopData.shop?.timezone
            }
        });

    } catch (error) {
        console.error('Shopify connection test error:', error);
        return NextResponse.json({
            success: false,
            error: 'Failed to test connection'
        }, { status: 500 });
    }
}
