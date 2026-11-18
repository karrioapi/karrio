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
        const { shop_domain, access_token } = await request.json();

        if (!shop_domain || !access_token) {
            return NextResponse.json({
                success: false,
                error: 'Missing shop_domain or access_token'
            }, { status: 400 });
        }

        // Validate shop domain format
        const shopHost = parseShopDomain(shop_domain);
        if (!shopHost) {
            return NextResponse.json({
                success: false,
                error: 'Invalid shop domain format. Must be <shop>.myshopify.com'
            }, { status: 400 });
        }

        // Test the connection by making a request to Shopify's shop API
        const shopifyUrl = `https://${shopHost}/admin/api/2023-04/shop.json`;

        const response = await fetch(shopifyUrl, {
            method: 'GET',
            redirect: 'manual', // never forward the token to another host
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
