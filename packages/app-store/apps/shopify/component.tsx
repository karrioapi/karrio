import React, { useEffect } from "react";
import { AppComponentProps } from "@karrio/app-store/types";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Alert, AlertDescription } from "@karrio/ui/components/ui/alert";
import { Store, CheckCircle, AlertCircle, ExternalLink } from "lucide-react";

export default function ShopifyComponent({ app, context }: AppComponentProps) {
  // Get metafields from installation - check both metafields array and config object
  const getMetafieldValue = (key: string, defaultValue?: any) => {
    // Try metafields array first
    const metafieldValue = app.installation?.metafields?.find(m => m.key === key)?.value;
    if (metafieldValue !== undefined) return metafieldValue;

    // Try config object as fallback (using any to avoid TypeScript errors)
    const configValue = (app.installation as any)?.config?.[key];
    if (configValue !== undefined) return configValue;

    return defaultValue;
  };

  const shopDomain = getMetafieldValue('shopify_shop_domain');
  const accessToken = getMetafieldValue('shopify_access_token');
  const carrierServiceName = getMetafieldValue('carrier_service_name', 'Karrio Shipping');
  const rateCalculationEnabled = getMetafieldValue('enable_rate_calculation', 'true') !== 'false';

  const isConnected = !!(shopDomain && accessToken);

  // Debug logging to help troubleshoot
  useEffect(() => {
    if (process.env.NODE_ENV === 'development') {
      console.log('Shopify Component Debug:', {
        hasInstallation: !!app.installation,
        metafields: app.installation?.metafields,
        config: (app.installation as any)?.config,
        shopDomain,
        hasAccessToken: !!accessToken,
        isConnected,
        apiKey: app.installation?.api_key ? 'present' : 'missing',
        metafieldValues: {
          domain: app.installation?.metafields?.find(m => m.key === 'shopify_shop_domain')?.value,
          token: app.installation?.metafields?.find(m => m.key === 'shopify_access_token')?.value ? 'present' : 'missing',
        }
      });
    }
  }, [app.installation, shopDomain, accessToken, isConnected]);

  const webhookUrl = app.installation?.id
    ? `${process.env.NEXT_PUBLIC_KARRIO_PUBLIC_URL || 'https://api.karrio.io'}/api/apps/shopify/carrier-service/rates/${app.installation.id}`
    : '';

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-green-600 rounded-lg flex items-center justify-center">
          <Store className="h-6 w-6 text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold">Shopify Integration</h1>
          <p className="text-muted-foreground">
            Connect your Shopify store for automated shipping rate calculations
          </p>
        </div>
      </div>

      {/* Connection Status */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            Connection Status
            {isConnected ? (
              <Badge variant="default" className="bg-green-100 text-green-800">
                <CheckCircle className="h-3 w-3 mr-1" />
                Connected
              </Badge>
            ) : (
              <Badge variant="destructive">
                <AlertCircle className="h-3 w-3 mr-1" />
                Not Connected
              </Badge>
            )}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {isConnected ? (
            <div className="space-y-4">
              <div className="p-3 bg-green-50 rounded-lg border border-green-200">
                <div className="flex items-center gap-2 mb-2">
                  <CheckCircle className="h-4 w-4 text-green-600" />
                  <span className="text-sm font-medium text-green-800">Successfully Connected</span>
                </div>
                <p className="text-xs text-green-700">
                  Your Shopify store is connected and ready for shipping rate calculations
                </p>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Shop Domain:</span>
                  <span className="text-sm text-muted-foreground">{shopDomain}</span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Carrier Service:</span>
                  <span className="text-sm text-muted-foreground">{carrierServiceName}</span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">Rate Calculation:</span>
                  <Badge variant={rateCalculationEnabled ? "default" : "secondary"}>
                    {rateCalculationEnabled ? "Enabled" : "Disabled"}
                  </Badge>
                </div>

                {shopDomain && (
                  <div className="pt-2">
                    <a
                      href={`https://${shopDomain}/admin`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 text-sm text-blue-600 hover:text-blue-800"
                    >
                      Open Shopify Admin
                      <ExternalLink className="h-3 w-3" />
                    </a>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <Alert>
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                Configure your Shopify store connection in the app settings to enable rate calculations.
              </AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Webhook Information */}
      {isConnected && (
        <Card>
          <CardHeader>
            <CardTitle>Webhook Configuration</CardTitle>
            <CardDescription>
              Use this URL in your Shopify carrier service configuration
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div>
                <label className="text-sm font-medium">Carrier Service URL:</label>
                <div className="mt-1 p-2 bg-gray-50 rounded border text-sm font-mono break-all">
                  {webhookUrl}
                </div>
              </div>

              <Alert>
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  Configure this URL in your Shopify admin under Settings → Shipping and delivery → Carrier services.
                  Set the service discovery to enabled.
                </AlertDescription>
              </Alert>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Quick Setup Guide */}
      <Card>
        <CardHeader>
          <CardTitle>Setup Guide</CardTitle>
          <CardDescription>
            Follow these steps to integrate Shopify with Karrio
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ol className="space-y-3 text-sm">
            <li className="flex gap-3">
              <span className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-800 rounded-full flex items-center justify-center text-xs font-medium">1</span>
              <span>Configure your Shopify store credentials in the app settings</span>
            </li>
            <li className="flex gap-3">
              <span className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-800 rounded-full flex items-center justify-center text-xs font-medium">2</span>
              <span>In Shopify admin, go to Settings → Shipping and delivery</span>
            </li>
            <li className="flex gap-3">
              <span className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-800 rounded-full flex items-center justify-center text-xs font-medium">3</span>
              <span>Add a new carrier service with the webhook URL above</span>
            </li>
            <li className="flex gap-3">
              <span className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-800 rounded-full flex items-center justify-center text-xs font-medium">4</span>
              <span>Enable service discovery and save</span>
            </li>
            <li className="flex gap-3">
              <span className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-800 rounded-full flex items-center justify-center text-xs font-medium">5</span>
              <span>Test by creating a test order in Shopify checkout</span>
            </li>
          </ol>
        </CardContent>
      </Card>
    </div>
  );
}
