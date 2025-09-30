"use client";
import React, { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Button } from "@karrio/ui/components/ui/button";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Switch } from "@karrio/ui/components/ui/switch";
import { Alert, AlertDescription } from "@karrio/ui/components/ui/alert";
import { Separator } from "@karrio/ui/components/ui/separator";
import {
  Store,
  CheckCircle2,
  AlertCircle,
  Settings,
  Link2,
  Globe,
  Save,
  RotateCcw,
  ExternalLink,
  Key,
  Webhook,
  ShoppingCart,
  Zap,
  Loader2,
  ShoppingBag,
  Link as LinkIcon
} from "lucide-react";
import type { AppConfigurationContext } from "../../types";

type ConnectionStatus = 'disconnected' | 'connected' | 'testing';

export default function ShopifyConfiguration({
  app,
  context,
  karrio,
  onConfigChange,
  onSave,
  onCancel,
}: AppConfigurationContext) {
  // Initialize state from current configuration
  const [config, setConfig] = useState({
    shopify_shop_domain: app.installation?.metafields?.find(m => m.key === 'shopify_shop_domain')?.value || '',
    shopify_access_token: app.installation?.metafields?.find(m => m.key === 'shopify_access_token')?.value || '',
    carrier_service_name: app.installation?.metafields?.find(m => m.key === 'carrier_service_name')?.value || 'Karrio Shipping',
    enable_rate_calculation: app.installation?.metafields?.find(m => m.key === 'enable_rate_calculation')?.value === 'true' || true,
    default_package_weight: parseFloat(app.installation?.metafields?.find(m => m.key === 'default_package_weight')?.value || '0.5') || 0.5,
    rate_markup_percentage: parseFloat(app.installation?.metafields?.find(m => m.key === 'rate_markup_percentage')?.value || '0') || 0,
  });

  const [isLoading, setIsLoading] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);
  const [oauthState, setOauthState] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>('disconnected');
  const [testResults, setTestResults] = useState<{ success: boolean, message: string } | null>(null);
  const [oauthSupported, setOauthSupported] = useState<boolean | null>(null);

  // Check if OAuth is completed
  const isOAuthCompleted = Boolean(config.shopify_shop_domain && config.shopify_access_token);

  // Check if OAuth is supported (environment variables are set)
  useEffect(() => {
    const checkOAuthSupport = async () => {
      try {
        const response = await fetch('/api/apps/shopify/oauth/check-support');
        const result = await response.json();
        setOauthSupported(result.supported);
      } catch (error) {
        console.error('Failed to check OAuth support:', error);
        setOauthSupported(false);
      }
    };

    checkOAuthSupport();
  }, []);

  // Track changes to enable/disable save button
  useEffect(() => {
    const currentConfig = {
      shopify_shop_domain: app.installation?.metafields?.find(m => m.key === 'shopify_shop_domain')?.value || '',
      shopify_access_token: app.installation?.metafields?.find(m => m.key === 'shopify_access_token')?.value || '',
      carrier_service_name: app.installation?.metafields?.find(m => m.key === 'carrier_service_name')?.value || 'Karrio Shipping',
      enable_rate_calculation: app.installation?.metafields?.find(m => m.key === 'enable_rate_calculation')?.value === 'true' || true,
      default_package_weight: parseFloat(app.installation?.metafields?.find(m => m.key === 'default_package_weight')?.value || '0.5') || 0.5,
      rate_markup_percentage: parseFloat(app.installation?.metafields?.find(m => m.key === 'rate_markup_percentage')?.value || '0') || 0,
    };

    const hasChanged = JSON.stringify(config) !== JSON.stringify(currentConfig);
    setHasChanges(hasChanged);
  }, [config, app.installation?.metafields]);

  // Check connection status based on saved metafields (not local config)
  useEffect(() => {
    const savedDomain = app.installation?.metafields?.find(m => m.key === 'shopify_shop_domain')?.value;
    const savedToken = app.installation?.metafields?.find(m => m.key === 'shopify_access_token')?.value;

    if (savedDomain && savedToken) {
      setConnectionStatus('connected');
    } else {
      setConnectionStatus('disconnected');
    }
  }, [app.installation?.metafields]);

  const handleConfigChange = (key: string, value: any) => {
    setConfig(prev => ({
      ...prev,
      [key]: value
    }));
    onConfigChange(key, value);
  };

  const handleSave = async () => {
    setIsLoading(true);
    try {
      // Convert boolean to string for backend compatibility
      const configToSave = {
        ...config,
        enable_rate_calculation: config.enable_rate_calculation.toString(),
        default_package_weight: config.default_package_weight.toString(),
        rate_markup_percentage: config.rate_markup_percentage.toString(),
      };

      // Update all config values
      Object.entries(configToSave).forEach(([key, value]) => {
        onConfigChange(key, value);
      });

      await onSave();
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    const originalConfig = {
      shopify_shop_domain: app.installation?.metafields?.find(m => m.key === 'shopify_shop_domain')?.value || '',
      shopify_access_token: app.installation?.metafields?.find(m => m.key === 'shopify_access_token')?.value || '',
      carrier_service_name: app.installation?.metafields?.find(m => m.key === 'carrier_service_name')?.value || 'Karrio Shipping',
      enable_rate_calculation: app.installation?.metafields?.find(m => m.key === 'enable_rate_calculation')?.value === 'true' || true,
      default_package_weight: parseFloat(app.installation?.metafields?.find(m => m.key === 'default_package_weight')?.value || '0.5') || 0.5,
      rate_markup_percentage: parseFloat(app.installation?.metafields?.find(m => m.key === 'rate_markup_percentage')?.value || '0') || 0,
    };
    setConfig(originalConfig);
  };

  const initiateOAuth = async () => {
    if (!config.shopify_shop_domain) {
      alert('Please enter your shop domain first');
      return;
    }

    setOauthState('loading');

    try {
      // Generate OAuth URL
      const oauthUrl = `/api/apps/shopify/oauth/authorize?installation_id=${app.installation?.id || ''}&shop=${config.shopify_shop_domain}`;

      // Open OAuth in new window
      const popup = window.open(
        oauthUrl,
        'shopify-oauth',
        'width=600,height=700,scrollbars=yes,resizable=yes'
      );

      // Listen for OAuth completion
      const checkClosed = setInterval(() => {
        if (popup?.closed) {
          clearInterval(checkClosed);
          setOauthState('idle');
          // Refresh configuration to get new tokens
          window.location.reload();
        }
      }, 1000);

    } catch (error) {
      console.error('OAuth initiation failed:', error);
      setOauthState('error');
    }
  };

  const testConnection = async () => {
    if (!config.shopify_shop_domain || !config.shopify_access_token) {
      setTestResults({
        success: false,
        message: 'Shop domain and access token are required'
      });
      return;
    }

    setConnectionStatus('testing');

    try {
      // Ensure shop domain has correct format
      let shopDomain = config.shopify_shop_domain.trim();
      if (!shopDomain.endsWith('.myshopify.com')) {
        if (shopDomain.includes('.')) {
          // If it already has a domain, don't modify it
        } else {
          // Add .myshopify.com if it's just the shop name
          shopDomain = `${shopDomain}.myshopify.com`;
        }
      }

      const requestBody = {
        installation_id: app.installation?.id || '',
        shop_domain: shopDomain,
        access_token: config.shopify_access_token,
      };

      console.log('Testing connection with:', {
        ...requestBody,
        access_token: '***REDACTED***'
      });

      const response = await fetch('/api/apps/shopify/test-connection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      console.log('Response status:', response.status);
      console.log('Response headers:', Object.fromEntries(response.headers.entries()));

      const responseText = await response.text();
      console.log('Raw response:', responseText);

      let result;
      try {
        result = JSON.parse(responseText);
      } catch (e) {
        console.error('Failed to parse JSON response:', e);
        setConnectionStatus('disconnected');
        setTestResults({
          success: false,
          message: `Invalid response: ${responseText.substring(0, 100)}`
        });
        return;
      }

      console.log('Parsed response:', result);

      if (result.success) {
        setConnectionStatus('connected');
        setTestResults({
          success: true,
          message: `Connected to ${result.shop_name || config.shopify_shop_domain}`
        });
      } else {
        setConnectionStatus('disconnected');
        setTestResults({
          success: false,
          message: result.error || 'Connection failed'
        });
      }
    } catch (error) {
      setConnectionStatus('disconnected');
      setTestResults({
        success: false,
        message: 'Failed to test connection'
      });
    }
  };

  return (
    <div className="flex flex-col h-full relative">
      {/* Scrollable Content */}
      <div className="grid gap-6 pb-32 p-4">

        {/* Connection Status */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ShoppingBag className="h-5 w-5" />
              Shopify Connection
            </CardTitle>
            <CardDescription>
              Connect your Shopify store to enable shipping rate calculations
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">

            {/* Connection Status Badge */}
            <div className="flex items-center justify-between p-4 border rounded-md">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <div className={`w-2 h-2 rounded-full ${connectionStatus === 'connected' ? 'bg-green-500' :
                    connectionStatus === 'testing' ? 'bg-yellow-500 animate-pulse' :
                      'bg-red-500'
                    }`}></div>
                  <Label className="font-medium">
                    {connectionStatus === 'connected' ? 'Connected' :
                      connectionStatus === 'testing' ? 'Testing...' :
                        'Disconnected'}
                  </Label>
                </div>
                <p className="text-xs text-muted-foreground">
                  {connectionStatus === 'connected' ? 'Your Shopify store is connected and ready' :
                    connectionStatus === 'testing' ? 'Testing connection to your Shopify store' :
                      'Connect your Shopify store to get started'}
                </p>
              </div>
              {connectionStatus === 'connected' && (
                <Badge variant="default" className="text-xs">
                  <CheckCircle2 className="w-3 h-3 mr-1" />
                  Authorized
                </Badge>
              )}
            </div>

            {/* Test Results */}
            {testResults && (
              <Alert variant={testResults.success ? "default" : "destructive"}>
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  {testResults.message}
                </AlertDescription>
              </Alert>
            )}

            {connectionStatus === 'disconnected' ? (
              /* Setup Flow - OAuth or Manual */
              <div className="space-y-4">
                {oauthSupported === null ? (
                  /* Loading OAuth support check */
                  <div className="flex items-center justify-center py-4">
                    <Loader2 className="h-5 w-5 animate-spin mr-2" />
                    <span className="text-sm text-muted-foreground">Checking configuration...</span>
                  </div>
                ) : oauthSupported ? (
                  /* OAuth Flow */
                  <>
                    <div className="flex items-center gap-2 p-3 bg-blue-50 rounded-lg border border-blue-200">
                      <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                      <span className="text-sm text-blue-700 font-medium">OAuth Setup Available</span>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="shopify_shop_domain">Shop Domain</Label>
                      <Input
                        id="shopify_shop_domain"
                        value={config.shopify_shop_domain}
                        onChange={(e) => handleConfigChange('shopify_shop_domain', e.target.value)}
                        placeholder="mystore.myshopify.com"
                      />
                      <p className="text-xs text-muted-foreground">
                        Enter your Shopify store domain (e.g., mystore.myshopify.com)
                      </p>
                    </div>

                    <Button
                      onClick={initiateOAuth}
                      disabled={!config.shopify_shop_domain || oauthState === 'loading'}
                      className="w-full"
                    >
                      {oauthState === 'loading' ? (
                        <>
                          <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                          Connecting to Shopify...
                        </>
                      ) : (
                        <>
                          <ExternalLink className="h-4 w-4 mr-2" />
                          Connect with Shopify OAuth
                        </>
                      )}
                    </Button>
                  </>
                ) : (
                  /* Manual Setup Flow */
                  <>
                    <div className="flex items-center gap-2 p-3 bg-amber-50 rounded-lg border border-amber-200">
                      <div className="w-2 h-2 bg-amber-500 rounded-full"></div>
                      <span className="text-sm text-amber-700 font-medium">Manual Setup Required</span>
                    </div>

                    <Alert>
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription className="text-sm">
                        OAuth environment variables are not configured. Please enter your Shopify credentials manually.
                        You can get these from your Shopify app settings or create a private app.
                      </AlertDescription>
                    </Alert>

                    <div className="space-y-4">
                      <div className="space-y-2">
                        <Label htmlFor="shopify_shop_domain">Shop Domain</Label>
                        <Input
                          id="shopify_shop_domain"
                          value={config.shopify_shop_domain}
                          onChange={(e) => handleConfigChange('shopify_shop_domain', e.target.value)}
                          placeholder="mystore.myshopify.com"
                        />
                        <p className="text-xs text-muted-foreground">
                          Your Shopify store domain (e.g., mystore.myshopify.com)
                        </p>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="shopify_access_token">Access Token</Label>
                        <Input
                          id="shopify_access_token"
                          type="password"
                          value={config.shopify_access_token}
                          onChange={(e) => handleConfigChange('shopify_access_token', e.target.value)}
                          placeholder="shpat_..."
                        />
                        <p className="text-xs text-muted-foreground">
                          Your Shopify private app access token or admin API access token
                        </p>
                      </div>

                      <Button
                        onClick={testConnection}
                        disabled={!config.shopify_shop_domain || !config.shopify_access_token || connectionStatus === 'testing'}
                        variant="outline"
                        className="w-full"
                      >
                        {connectionStatus === 'testing' ? (
                          <>
                            <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                            Testing Connection...
                          </>
                        ) : (
                          <>
                            <CheckCircle2 className="h-4 w-4 mr-2" />
                            Test Connection
                          </>
                        )}
                      </Button>
                    </div>
                  </>
                )}

                {!oauthSupported && (
                  <div className="p-4 bg-gray-50 rounded-md border">
                    <h4 className="font-medium text-gray-900 mb-2">How to get Shopify credentials:</h4>
                    <ol className="text-sm text-gray-700 space-y-1 list-decimal list-inside">
                      <li>Go to your Shopify admin → Apps → App and sales channel settings</li>
                      <li>Click "Develop apps" → "Create an app"</li>
                      <li>Configure Admin API scopes: <code className="bg-gray-200 px-1 rounded">read_orders, write_shipping</code></li>
                      <li>Install the app and copy the Admin API access token</li>
                    </ol>
                  </div>
                )}

                {oauthSupported && (
                  <div className="p-4 bg-blue-50 rounded-md border border-blue-200">
                    <h4 className="text-sm font-medium text-blue-900 mb-2">What happens next?</h4>
                    <ul className="text-xs text-blue-800 space-y-1">
                      <li>• You'll be redirected to Shopify to authorize the connection</li>
                      <li>• Grant permissions for reading orders and managing shipping</li>
                      <li>• Return here to complete the setup</li>
                    </ul>
                  </div>
                )}
              </div>
            ) : (
              /* Connection Established - Show current status */
              <div className="space-y-4">
                <div className="flex items-center gap-2 p-3 bg-green-50 rounded-lg border border-green-200">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-green-700 font-medium">
                    Connected to {app.installation?.metafields?.find(m => m.key === 'shopify_shop_domain')?.value || config.shopify_shop_domain}
                  </span>
                </div>

                {testResults && (
                  <Alert className={testResults.success ? "border-green-200 bg-green-50" : "border-red-200 bg-red-50"}>
                    <AlertCircle className={`h-4 w-4 ${testResults.success ? "text-green-600" : "text-red-600"}`} />
                    <AlertDescription className={`text-sm ${testResults.success ? "text-green-700" : "text-red-700"}`}>
                      {testResults.message}
                    </AlertDescription>
                  </Alert>
                )}

                <Button
                  onClick={testConnection}
                  disabled={connectionStatus === 'testing'}
                  variant="outline"
                  className="w-full"
                >
                  {connectionStatus === 'testing' ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Testing Connection...
                    </>
                  ) : (
                    <>
                      <CheckCircle2 className="h-4 w-4 mr-2" />
                      Test Connection
                    </>
                  )}
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Carrier Service Configuration */}
        {connectionStatus === 'connected' && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="h-5 w-5" />
                Carrier Service Settings
              </CardTitle>
              <CardDescription>
                Configure how Karrio appears in your Shopify checkout
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="carrier_service_name">Service Name</Label>
                <Input
                  id="carrier_service_name"
                  value={config.carrier_service_name}
                  onChange={(e) => handleConfigChange('carrier_service_name', e.target.value)}
                  placeholder="Karrio Shipping"
                />
                <p className="text-xs text-muted-foreground">
                  This name will appear in your Shopify checkout
                </p>
              </div>

              <Separator />

              <div className="flex items-center justify-between p-4 border rounded-md">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <Zap className="h-4 w-4" />
                    <Label className="font-medium">Live Rate Calculation</Label>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Allow Shopify to request real-time shipping rates from Karrio
                  </p>
                </div>
                <Switch
                  checked={config.enable_rate_calculation}
                  onCheckedChange={(checked) => handleConfigChange('enable_rate_calculation', checked)}
                />
              </div>
            </CardContent>
          </Card>
        )}

        {/* Shipping Settings */}
        {connectionStatus === 'connected' && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Key className="h-5 w-5" />
                Shipping Configuration
              </CardTitle>
              <CardDescription>
                Configure default shipping parameters
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="default_package_weight">Default Package Weight (kg)</Label>
                  <Input
                    id="default_package_weight"
                    type="number"
                    min="0"
                    step="0.1"
                    value={config.default_package_weight}
                    onChange={(e) => handleConfigChange('default_package_weight', parseFloat(e.target.value) || 0)}
                  />
                  <p className="text-xs text-muted-foreground">
                    Used for items without specified weight
                  </p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="rate_markup_percentage">Rate Markup (%)</Label>
                  <Input
                    id="rate_markup_percentage"
                    type="number"
                    min="0"
                    max="100"
                    step="0.1"
                    value={config.rate_markup_percentage}
                    onChange={(e) => handleConfigChange('rate_markup_percentage', parseFloat(e.target.value) || 0)}
                  />
                  <p className="text-xs text-muted-foreground">
                    Percentage markup added to shipping rates
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Integration Guide */}
        {connectionStatus === 'connected' && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <LinkIcon className="h-5 w-5" />
                Integration Status
              </CardTitle>
              <CardDescription>
                Your Shopify integration is ready
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                  <div className="flex items-center gap-2 mb-2">
                    <CheckCircle2 className="h-4 w-4 text-green-600" />
                    <span className="text-sm font-medium text-green-900">OAuth Connected</span>
                  </div>
                  <p className="text-xs text-green-800">
                    Shopify store is authorized and connected
                  </p>
                </div>

                <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                  <div className="flex items-center gap-2 mb-2">
                    <Zap className="h-4 w-4 text-blue-600" />
                    <span className="text-sm font-medium text-blue-900">Rates Enabled</span>
                  </div>
                  <p className="text-xs text-blue-800">
                    Live shipping rates will appear in checkout
                  </p>
                </div>
              </div>

              <Alert>
                <CheckCircle2 className="h-4 w-4" />
                <AlertDescription>
                  Your Shopify store is now connected to Karrio. Customers will see live shipping rates during checkout.
                </AlertDescription>
              </Alert>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Sticky Save Button */}
      <div className="sticky bottom-0 left-0 right-0 bg-white/95 backdrop-blur-sm border-t shadow-lg p-4 bg-background">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            {hasChanges ? (
              <>
                <div className="w-2 h-2 bg-orange-500 rounded-full animate-pulse"></div>
                Unsaved changes
              </>
            ) : (
              <>
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                All changes saved
              </>
            )}
          </div>
          <div className="flex items-center gap-3">
            {hasChanges && (
              <Button variant="outline" onClick={handleReset} disabled={isLoading}>
                <RotateCcw className="h-4 w-4 mr-2" />
                Reset
              </Button>
            )}
            <Button
              onClick={handleSave}
              disabled={!hasChanges || isLoading}
              className="min-w-[120px]"
            >
              <Save className="h-4 w-4 mr-2" />
              {isLoading ? 'Saving...' : 'Save Changes'}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
