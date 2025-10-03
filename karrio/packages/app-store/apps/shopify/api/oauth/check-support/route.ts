import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // Check if required Shopify OAuth environment variables are set
    const clientId = process.env.SHOPIFY_APP_KEY;
    const clientSecret = process.env.SHOPIFY_APP_SECRET;

    const supported = !!(clientId && clientSecret);

    return NextResponse.json({
      supported,
      message: supported
        ? 'OAuth flow is available'
        : 'OAuth environment variables not configured - manual setup required'
    });
  } catch (error) {
    console.error('OAuth support check error:', error);
    return NextResponse.json({
      supported: false,
      message: 'Failed to check OAuth support'
    });
  }
}
