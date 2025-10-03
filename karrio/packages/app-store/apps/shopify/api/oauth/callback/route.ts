import { NextRequest, NextResponse } from 'next/server';
import { oauthStates } from '../authorize/route';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get('code');
  const state = searchParams.get('state');
  const shop = searchParams.get('shop');
  const error = searchParams.get('error');

  // Handle OAuth errors
  if (error) {
    const errorDescription = searchParams.get('error_description') || 'OAuth authorization failed';
    return new Response(`
      <html>
        <body>
          <script>
            alert('OAuth Error: ${errorDescription}');
            window.close();
          </script>
        </body>
      </html>
    `, {
      headers: { 'Content-Type': 'text/html' }
    });
  }

  if (!code || !state || !shop) {
    return new Response(`
      <html>
        <body>
          <script>
            alert('Missing required OAuth parameters');
            window.close();
          </script>
        </body>
      </html>
    `, {
      headers: { 'Content-Type': 'text/html' }
    });
  }

  try {
    // Validate state parameter
    const stateData = oauthStates.get(state);
    if (!stateData || stateData.expires < Date.now()) {
      throw new Error('Invalid or expired OAuth state');
    }

    // Clean up used state
    oauthStates.delete(state);

    // Verify shop matches
    if (stateData.shop !== shop) {
      throw new Error('Shop domain mismatch');
    }

    // Check environment variables
    const clientId = process.env.SHOPIFY_APP_KEY;
    const clientSecret = process.env.SHOPIFY_APP_SECRET;

    console.log('OAuth Callback Debug:', {
      clientId: clientId ? 'SET' : 'NOT SET',
      clientSecret: clientSecret ? 'SET' : 'NOT SET',
      shop,
      code: code ? 'RECEIVED' : 'MISSING',
      state: state ? 'RECEIVED' : 'MISSING'
    });

    if (!clientId || !clientSecret) {
      throw new Error('Shopify app credentials not configured (SHOPIFY_APP_KEY or SHOPIFY_APP_SECRET missing)');
    }

    // Exchange authorization code for access token
    const tokenResponse = await fetch(`https://${shop}/admin/oauth/access_token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        client_id: clientId,
        client_secret: clientSecret,
        code,
      }),
    });

    if (!tokenResponse.ok) {
      const errorText = await tokenResponse.text();
      console.error('Shopify token exchange error:', errorText);
      throw new Error(`Token exchange failed: ${tokenResponse.statusText} - ${errorText}`);
    }

    const tokenData = await tokenResponse.json();
    const { access_token, scope } = tokenData;

    if (!access_token) {
      throw new Error('No access token received');
    }

    // Get shop information
    const shopResponse = await fetch(`https://${shop}/admin/api/2023-10/shop.json`, {
      headers: {
        'X-Shopify-Access-Token': access_token,
      },
    });

    let shopInfo: { name?: string } | null = null;
    if (shopResponse.ok) {
      const shopData = await shopResponse.json();
      shopInfo = shopData.shop;
    }

    // Update app installation with OAuth tokens
    // Note: In a real implementation, you'd update the database here
    // For now, we'll use the GraphQL API to update metafields

    const updatePayload = {
      query: `
        mutation UpdateAppInstallation($id: String!, $metafields: [CreateMetafieldInput!]!) {
          update_app_installation(id: $id, metafields: $metafields) {
            installation {
              id
              metafields {
                id
                key
                value
              }
            }
            errors {
              field
              messages
            }
          }
        }
      `,
      variables: {
        id: stateData.installation_id,
        metafields: [
          {
            key: 'shopify_shop_domain',
            value: shop,
            type: 'text',
            is_required: true,
          },
          {
            key: 'shopify_access_token',
            value: access_token,
            type: 'password',
            is_required: true,
          },
          {
            key: 'shopify_scope',
            value: scope || 'read_orders,write_shipping',
            type: 'text',
            is_required: false,
          },
          ...(shopInfo ? [{
            key: 'shopify_shop_name',
            value: shopInfo.name || shop,
            type: 'text',
            is_required: false,
          }] : []),
        ],
      },
    };

    // Call GraphQL API to update installation
    // Use the internal GraphQL endpoint with cookie-based authentication
    const apiUrl = `${process.env.NEXT_PUBLIC_APP_URL}/api/graphql`;
    console.log('Calling GraphQL API:', apiUrl);

    const apiResponse = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Forward cookies from the request for authentication
        'Cookie': request.headers.get('cookie') || '',
      },
      body: JSON.stringify(updatePayload),
    });

    const responseText = await apiResponse.text();
    console.log('GraphQL API Response:', {
      status: apiResponse.status,
      statusText: apiResponse.statusText,
      response: responseText.substring(0, 500) // Log first 500 chars
    });

    if (!apiResponse.ok) {
      console.error('Failed to update app installation:', responseText);
      throw new Error(`GraphQL API error: ${apiResponse.status} ${apiResponse.statusText}`);
    }

    try {
      const result = JSON.parse(responseText);
      if (result.errors) {
        console.error('GraphQL errors:', result.errors);
        throw new Error(`GraphQL errors: ${JSON.stringify(result.errors)}`);
      }
    } catch (parseError) {
      console.error('Failed to parse GraphQL response:', parseError);
      // Continue anyway - might be a non-JSON response
    }

    // Success - close popup and refresh parent
    return new Response(`
      <html>
        <head>
          <title>Shopify Connected Successfully</title>
          <style>
            body {
              font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
              display: flex;
              align-items: center;
              justify-content: center;
              height: 100vh;
              margin: 0;
              background: #f6f6f7;
            }
            .container {
              text-align: center;
              background: white;
              padding: 2rem;
              border-radius: 8px;
              box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .success {
              color: #16a34a;
              font-size: 48px;
              margin-bottom: 1rem;
            }
            h1 {
              color: #1f2937;
              margin-bottom: 0.5rem;
            }
            p {
              color: #6b7280;
              margin-bottom: 1.5rem;
            }
            .shop-info {
              background: #f3f4f6;
              padding: 1rem;
              border-radius: 4px;
              margin: 1rem 0;
            }
          </style>
        </head>
        <body>
          <div class="container">
            <div class="success">✅</div>
            <h1>Shopify Connected Successfully!</h1>
            <p>Your Shopify store has been connected to Karrio.</p>
            ${shopInfo ? `
              <div class="shop-info">
                <strong>${shopInfo.name}</strong><br>
                <small>${shop}</small>
              </div>
            ` : ''}
            <p><small>This window will close automatically...</small></p>
          </div>
          <script>
            // Close the popup and refresh the parent window
            setTimeout(() => {
              if (window.opener) {
                window.opener.location.reload();
              }
              window.close();
            }, 2000);
          </script>
        </body>
      </html>
    `, {
      headers: { 'Content-Type': 'text/html' }
    });

  } catch (error) {
    console.error('OAuth callback error:', error);

    return new Response(`
      <html>
        <body>
          <script>
            alert('OAuth Error: ${error instanceof Error ? error.message : 'Unknown error'}');
            window.close();
          </script>
        </body>
      </html>
    `, {
      headers: { 'Content-Type': 'text/html' }
    });
  }
}
