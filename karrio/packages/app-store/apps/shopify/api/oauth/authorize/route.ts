import { NextRequest, NextResponse } from 'next/server';
import { randomBytes } from 'crypto';

// Store OAuth state temporarily (in production, use Redis or database)
const oauthStates = new Map<string, { installation_id: string, shop: string, expires: number }>();

export async function GET(request: NextRequest) {
    const { searchParams } = new URL(request.url);
    const installation_id = searchParams.get('installation_id');
    const shop = searchParams.get('shop');

    if (!installation_id || !shop) {
        return NextResponse.json(
            { error: 'Missing installation_id or shop parameter' },
            { status: 400 }
        );
    }

    // Validate shop domain format
    if (!shop.endsWith('.myshopify.com')) {
        return NextResponse.json(
            { error: 'Invalid shop domain format' },
            { status: 400 }
        );
    }

    try {
        // Generate secure state parameter for CSRF protection
        const state = randomBytes(32).toString('hex');

        // Store state with expiration (5 minutes)
        oauthStates.set(state, {
            installation_id,
            shop,
            expires: Date.now() + 5 * 60 * 1000
        });

        // Clean up expired states
        for (const [key, value] of oauthStates.entries()) {
            if (value.expires < Date.now()) {
                oauthStates.delete(key);
            }
        }

        // Shopify OAuth parameters
        const clientId = process.env.SHOPIFY_APP_KEY;
        const redirectUri = `${process.env.NEXT_PUBLIC_APP_URL}/api/apps/shopify/oauth/callback`;
        const scopes = 'read_orders,write_shipping'; // Required scopes

        console.log('OAuth Debug:', {
            clientId: clientId ? 'SET' : 'NOT SET',
            redirectUri,
            shop,
            installation_id
        });

        if (!clientId) {
            return NextResponse.json(
                {
                    error: 'Shopify app credentials not configured',
                    details: 'SHOPIFY_APP_KEY environment variable is not set'
                },
                { status: 500 }
            );
        }

        // Build Shopify OAuth URL
        const authUrl = new URL(`https://${shop}/admin/oauth/authorize`);
        authUrl.searchParams.set('client_id', clientId);
        authUrl.searchParams.set('scope', scopes);
        authUrl.searchParams.set('redirect_uri', redirectUri);
        authUrl.searchParams.set('state', state);

        // Redirect to Shopify OAuth
        return NextResponse.redirect(authUrl.toString());

    } catch (error) {
        console.error('OAuth authorization error:', error);
        return NextResponse.json(
            { error: 'Failed to initiate OAuth flow' },
            { status: 500 }
        );
    }
}

// Export the state store for use in callback
export { oauthStates };
