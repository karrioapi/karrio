"use client";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@karrio/ui/components/ui/card";
import { Switch } from "@karrio/ui/components/ui/switch";
import { Input } from "@karrio/ui/components/ui/input";
import { Button } from "@karrio/ui/components/ui/button";
import { Label } from "@karrio/ui/components/ui/label";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useConfigs, useConfigMutation, useConfigFieldsets, useConfigSchema } from "@karrio/hooks/admin-platform";
import { useAdminSystemUsage } from "@karrio/hooks/admin-usage";
import { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@karrio/ui/components/ui/dialog";
import { Pencil, Check, X, ExternalLink, Copy } from "lucide-react";
import { url$ } from "@karrio/lib";

type ConfigData = {
  EMAIL_USE_TLS: boolean;
  EMAIL_HOST_USER: string;
  EMAIL_HOST_PASSWORD: string;
  EMAIL_HOST: string;
  EMAIL_PORT: number;
  EMAIL_FROM_ADDRESS: string;
  GOOGLE_CLOUD_API_KEY: string;
  CANADAPOST_ADDRESS_COMPLETE_API_KEY: string;
  ORDER_DATA_RETENTION: number;
  TRACKER_DATA_RETENTION: number;
  SHIPMENT_DATA_RETENTION: number;
  API_LOGS_DATA_RETENTION: number;
  APP_NAME: string;
  APP_WEBSITE: string;
  ALLOW_SIGNUP: boolean;
  ALLOW_ADMIN_APPROVED_SIGNUP: boolean;
  DOCUMENTS_MANAGEMENT: boolean;
  DATA_IMPORT_EXPORT: boolean;
  PERSIST_SDK_TRACING: boolean;
  WORKFLOW_MANAGEMENT: boolean;
  AUDIT_LOGGING: boolean;
  ALLOW_MULTI_ACCOUNT: boolean;
  ADMIN_DASHBOARD: boolean;
  ORDERS_MANAGEMENT: boolean;
  APPS_MANAGEMENT: boolean;
  MULTI_ORGANIZATIONS: boolean;
  SHIPPING_RULES: boolean;
  [key: string]: any;
};

const defaultConfig: ConfigData = {
  EMAIL_USE_TLS: false,
  EMAIL_HOST_USER: "",
  EMAIL_HOST_PASSWORD: "",
  EMAIL_HOST: "",
  EMAIL_PORT: 587,
  EMAIL_FROM_ADDRESS: "",
  GOOGLE_CLOUD_API_KEY: "",
  CANADAPOST_ADDRESS_COMPLETE_API_KEY: "",
  ORDER_DATA_RETENTION: 90,
  TRACKER_DATA_RETENTION: 90,
  SHIPMENT_DATA_RETENTION: 90,
  API_LOGS_DATA_RETENTION: 30,
  APP_NAME: "",
  APP_WEBSITE: "",
  ALLOW_SIGNUP: true,
  ALLOW_ADMIN_APPROVED_SIGNUP: false,
  DOCUMENTS_MANAGEMENT: false,
  DATA_IMPORT_EXPORT: false,
  PERSIST_SDK_TRACING: false,
  WORKFLOW_MANAGEMENT: false,
  AUDIT_LOGGING: false,
  ALLOW_MULTI_ACCOUNT: false,
  ADMIN_DASHBOARD: false,
  ORDERS_MANAGEMENT: false,
  APPS_MANAGEMENT: false,
  MULTI_ORGANIZATIONS: false,
  SHIPPING_RULES: false,
};

type EditSection = 'email' | 'administration' | 'data_retention' | 'api_keys' | 'features' | 'platform' | string | null;

function SettingRow({ label, description, enabled }: { label: string; description?: string; enabled: boolean }) {
  return (
    <div className="flex items-center justify-between py-2">
      <div className="space-y-0.5">
        <p className="text-sm font-medium">{label}</p>
        {description && <p className="text-xs text-muted-foreground">{description}</p>}
      </div>
      {enabled ? (
        <Check className="h-4 w-4 text-green-500" />
      ) : (
        <X className="h-4 w-4 text-muted-foreground" />
      )}
    </div>
  );
}

function EndpointRow({ label, value, onCopy, onOpen }: { label: string; value: string; onCopy: () => void; onOpen: () => void }) {
  return (
    <div className="py-2">
      <p className="text-xs text-muted-foreground mb-1">{label}</p>
      <div className="flex items-center gap-2 group">
        <p className="text-sm font-medium truncate flex-1">{value}</p>
        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity shrink-0">
          <Button variant="ghost" size="icon" className="h-6 w-6" onClick={onCopy}>
            <Copy className="h-3.5 w-3.5" />
          </Button>
          <Button variant="ghost" size="icon" className="h-6 w-6" onClick={onOpen}>
            <ExternalLink className="h-3.5 w-3.5" />
          </Button>
        </div>
      </div>
    </div>
  );
}

export default function PlatformDetails() {
  const { toast } = useToast();
  const { metadata } = useAPIMetadata();
  const { query, configs } = useConfigs();
  const { query: { data: { usage } = {} } } = useAdminSystemUsage();
  const { fieldsets } = useConfigFieldsets();
  const { schema } = useConfigSchema();
  const [editSection, setEditSection] = useState<EditSection>(null);

  const { updateConfigs } = useConfigMutation();

  const handleUpdate = (data: Partial<ConfigData>) => {
    updateConfigs.mutate(data, {
      onSuccess: () => {
        toast({ title: "Settings saved successfully" });
        setEditSection(null);
      },
      onError: (error: any) => {
        toast({
          title: "Failed to save settings",
          description: error.message || "An error occurred",
          variant: "destructive",
        });
      },
    });
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text || "");
    toast({ title: "Copied to clipboard" });
  };

  const currentConfig = configs ? {
    ...defaultConfig,
    ...Object.fromEntries(
      Object.entries(configs).map(([key, value]) => [key, value === null ? defaultConfig[key as keyof ConfigData] : value])
    )
  } as ConfigData : defaultConfig;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold tracking-tight">Platform Overview</h1>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="border shadow-none">
          <CardContent className="p-4">
            <p className="text-sm text-muted-foreground">Total Users</p>
            <p className="text-2xl font-semibold">{usage?.user_count?.toLocaleString() || 0}</p>
          </CardContent>
        </Card>
        <Card className="border shadow-none">
          <CardContent className="p-4">
            <p className="text-sm text-muted-foreground">Organizations</p>
            <p className="text-2xl font-semibold">{usage?.organization_count?.toLocaleString() || 0}</p>
          </CardContent>
        </Card>
        <Card className="border shadow-none">
          <CardContent className="p-4">
            <p className="text-sm text-muted-foreground">Total Shipments</p>
            <p className="text-2xl font-semibold">{usage?.total_shipments?.toLocaleString() || 0}</p>
          </CardContent>
        </Card>
        <Card className="border shadow-none">
          <CardContent className="p-4">
            <p className="text-sm text-muted-foreground">API Requests</p>
            <p className="text-2xl font-semibold">{usage?.total_requests?.toLocaleString() || 0}</p>
          </CardContent>
        </Card>
      </div>

      {/* Platform Details & API Endpoints */}
      <div className="grid lg:grid-cols-2 gap-4">
        <Card className="border shadow-none">
          <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
            <div>
              <CardTitle className="text-base">Platform Details</CardTitle>
              <CardDescription>Branding and identity</CardDescription>
            </div>
            <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => setEditSection('platform')}>
              <Pencil className="h-4 w-4" />
            </Button>
          </CardHeader>
          <CardContent className="space-y-1">
            <div className="py-2">
              <p className="text-xs text-muted-foreground mb-1">Platform Name</p>
              <p className="text-sm font-medium">{currentConfig.APP_NAME || metadata?.APP_NAME || 'Not configured'}</p>
            </div>
            <div className="py-2">
              <p className="text-xs text-muted-foreground mb-1">Platform Website</p>
              <div className="flex items-center gap-2 group">
                <p className="text-sm font-medium truncate flex-1">{currentConfig.APP_WEBSITE || metadata?.APP_WEBSITE || 'Not configured'}</p>
                {(currentConfig.APP_WEBSITE || metadata?.APP_WEBSITE) && (
                  <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity shrink-0">
                    <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => copyToClipboard(currentConfig.APP_WEBSITE || metadata?.APP_WEBSITE || "")}>
                      <Copy className="h-3.5 w-3.5" />
                    </Button>
                    <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => window.open(currentConfig.APP_WEBSITE || metadata?.APP_WEBSITE, '_blank')}>
                      <ExternalLink className="h-3.5 w-3.5" />
                    </Button>
                  </div>
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border shadow-none">
          <CardHeader className="pb-2">
            <CardTitle className="text-base">API Endpoints</CardTitle>
            <CardDescription>Integration URLs</CardDescription>
          </CardHeader>
          <CardContent className="space-y-1">
            <EndpointRow
              label="API Host"
              value={metadata?.HOST || ''}
              onCopy={() => copyToClipboard(metadata?.HOST || "")}
              onOpen={() => window.open(metadata?.HOST, '_blank')}
            />
            <EndpointRow
              label="GraphQL"
              value={metadata?.GRAPHQL || ''}
              onCopy={() => copyToClipboard(metadata?.GRAPHQL || "")}
              onOpen={() => window.open(metadata?.GRAPHQL, '_blank')}
            />
            <EndpointRow
              label="Admin GraphQL"
              value={url$`${metadata?.HOST}/admin/graphql`}
              onCopy={() => copyToClipboard(url$`${metadata?.HOST}/admin/graphql`)}
              onOpen={() => window.open(url$`${metadata?.HOST}/admin/graphql`, '_blank')}
            />
          </CardContent>
        </Card>
      </div>

      {/* Administration & Features */}
      <div className="grid lg:grid-cols-2 gap-4">
        <Card className="border shadow-none">
          <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
            <div>
              <CardTitle className="text-base">Administration</CardTitle>
              <CardDescription>User access and signup settings</CardDescription>
            </div>
            <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => setEditSection('administration')}>
              <Pencil className="h-4 w-4" />
            </Button>
          </CardHeader>
          <CardContent className="divide-y">
            <SettingRow label="Allow Signup" description="Allow user signup" enabled={currentConfig.ALLOW_SIGNUP} />
            <SettingRow label="Admin Approved Signup" description="Require admin approval" enabled={currentConfig.ALLOW_ADMIN_APPROVED_SIGNUP} />
            <SettingRow label="Audit Logging" description="Track system activities" enabled={currentConfig.AUDIT_LOGGING} />
          </CardContent>
        </Card>

        <Card className="border shadow-none">
          <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
            <div>
              <CardTitle className="text-base">Features</CardTitle>
              <CardDescription>Platform capabilities</CardDescription>
            </div>
            <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => setEditSection('features')}>
              <Pencil className="h-4 w-4" />
            </Button>
          </CardHeader>
          <CardContent className="divide-y">
            <SettingRow label="Multi Organizations" enabled={currentConfig.MULTI_ORGANIZATIONS} />
            <SettingRow label="Orders Management" enabled={currentConfig.ORDERS_MANAGEMENT} />
            <SettingRow label="Workflow Management" enabled={currentConfig.WORKFLOW_MANAGEMENT} />
            <SettingRow label="Shipping Rules" enabled={currentConfig.SHIPPING_RULES} />
            <SettingRow label="Documents Management" enabled={currentConfig.DOCUMENTS_MANAGEMENT} />
            <SettingRow label="Apps Management" enabled={currentConfig.APPS_MANAGEMENT} />
          </CardContent>
        </Card>
      </div>

      {/* Email & Data Retention */}
      <div className="grid lg:grid-cols-2 gap-4">
        <Card className="border shadow-none">
          <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
            <div>
              <CardTitle className="text-base">Email Configuration</CardTitle>
              <CardDescription>SMTP settings for notifications</CardDescription>
            </div>
            <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => setEditSection('email')}>
              <Pencil className="h-4 w-4" />
            </Button>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-x-4 gap-y-2">
              <div className="py-2">
                <p className="text-xs text-muted-foreground mb-1">Host</p>
                <p className="text-sm font-medium">{currentConfig.EMAIL_HOST || 'Not configured'}</p>
              </div>
              <div className="py-2">
                <p className="text-xs text-muted-foreground mb-1">Port</p>
                <p className="text-sm font-medium">{currentConfig.EMAIL_PORT || 'Not configured'}</p>
              </div>
              <div className="py-2">
                <p className="text-xs text-muted-foreground mb-1">User</p>
                <p className="text-sm font-medium truncate">{currentConfig.EMAIL_HOST_USER || 'Not configured'}</p>
              </div>
              <div className="py-2">
                <p className="text-xs text-muted-foreground mb-1">From Address</p>
                <p className="text-sm font-medium truncate">{currentConfig.EMAIL_FROM_ADDRESS || 'Not configured'}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border shadow-none">
          <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
            <div>
              <CardTitle className="text-base">Data Retention</CardTitle>
              <CardDescription>Automatic cleanup periods</CardDescription>
            </div>
            <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => setEditSection('data_retention')}>
              <Pencil className="h-4 w-4" />
            </Button>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-3 gap-4">
              <div className="py-2">
                <p className="text-xs text-muted-foreground mb-1">Orders</p>
                <p className="text-sm font-medium">{currentConfig.ORDER_DATA_RETENTION || 90} days</p>
              </div>
              <div className="py-2">
                <p className="text-xs text-muted-foreground mb-1">Shipments</p>
                <p className="text-sm font-medium">{currentConfig.SHIPMENT_DATA_RETENTION || 90} days</p>
              </div>
              <div className="py-2">
                <p className="text-xs text-muted-foreground mb-1">API Logs</p>
                <p className="text-sm font-medium">{currentConfig.API_LOGS_DATA_RETENTION || 30} days</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* API Keys */}
      <Card className="border shadow-none">
        <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
          <div>
            <CardTitle className="text-base">Address Validation</CardTitle>
            <CardDescription>Third-party API keys for address services</CardDescription>
          </div>
          <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => setEditSection('api_keys')}>
            <Pencil className="h-4 w-4" />
          </Button>
        </CardHeader>
        <CardContent>
          <div className="grid lg:grid-cols-2 gap-4">
            <div className="py-2">
              <p className="text-xs text-muted-foreground mb-1">Google Cloud API Key</p>
              <p className="text-sm font-medium">{currentConfig.GOOGLE_CLOUD_API_KEY ? '••••••••••••' : 'Not configured'}</p>
            </div>
            <div className="py-2">
              <p className="text-xs text-muted-foreground mb-1">Canada Post Address Complete</p>
              <p className="text-sm font-medium">{currentConfig.CANADAPOST_ADDRESS_COMPLETE_API_KEY ? '••••••••••••' : 'Not configured'}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Dynamic Carrier Config Sections */}
      {fieldsets
        .filter(fs => ![
          "Email Config",
          "Address Validation Service",
          "Data Retention",
          "Feature Flags",
          "Platform Config",
          "Registry Config",
          "Registry Plugins",
        ].includes(fs.name))
        .map(fs => {
          const sectionKey = `dynamic_${fs.name.toLowerCase().replace(/\s+/g, '_')}`;
          return (
            <Card key={fs.name} className="border shadow-none">
              <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
                <div>
                  <CardTitle className="text-base">{fs.name}</CardTitle>
                  <CardDescription>Carrier configuration settings</CardDescription>
                </div>
                <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => setEditSection(sectionKey)}>
                  <Pencil className="h-4 w-4" />
                </Button>
              </CardHeader>
              <CardContent>
                <div className="grid lg:grid-cols-2 gap-4">
                  {fs.keys.map(key => {
                    const schemaDef = schema.find(s => s.key === key);
                    const value = currentConfig[key];
                    const isBool = schemaDef?.value_type === 'bool';
                    return (
                      <div key={key} className="py-2">
                        <p className="text-xs text-muted-foreground mb-1">
                          {schemaDef?.description || key}
                        </p>
                        {isBool ? (
                          value ? (
                            <Check className="h-4 w-4 text-green-500" />
                          ) : (
                            <X className="h-4 w-4 text-muted-foreground" />
                          )
                        ) : (
                          <p className="text-sm font-medium">
                            {value !== null && value !== undefined && value !== '' ? String(value) : 'Not configured'}
                          </p>
                        )}
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          );
        })}

      {/* Plugin Registry */}
      {fieldsets
        .filter(fs => fs.name === "Registry Plugins")
        .map(fs => (
          <Card key={fs.name} className="border shadow-none">
            <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
              <div>
                <CardTitle className="text-base">Plugin Registry</CardTitle>
                <CardDescription>Enable or disable registered plugins</CardDescription>
              </div>
              <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => setEditSection('plugins')}>
                <Pencil className="h-4 w-4" />
              </Button>
            </CardHeader>
            <CardContent className="divide-y">
              {fs.keys.map(key => {
                const schemaDef = schema.find(s => s.key === key);
                return (
                  <SettingRow
                    key={key}
                    label={schemaDef?.description || key}
                    enabled={!!currentConfig[key]}
                  />
                );
              })}
            </CardContent>
          </Card>
        ))}

      <EditDialog
        section={editSection}
        onClose={() => setEditSection(null)}
        configs={currentConfig}
        onUpdate={handleUpdate}
        fieldsets={fieldsets}
        schema={schema}
      />
    </div>
  );
}

function EditDialog({
  section,
  onClose,
  configs,
  onUpdate,
  fieldsets,
  schema,
}: {
  section: EditSection;
  onClose: () => void;
  configs: ConfigData;
  onUpdate: (data: Partial<ConfigData>) => void;
  fieldsets: { name: string; keys: string[] }[];
  schema: { key: string; description: string; value_type: string; default_value: string | null }[];
}) {
  const [formData, setFormData] = useState<ConfigData>(configs);

  useEffect(() => {
    setFormData(configs);
  }, [configs, section]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const data: Partial<ConfigData> = {};

    switch (section) {
      case 'platform':
        data.APP_NAME = formData.APP_NAME;
        data.APP_WEBSITE = formData.APP_WEBSITE;
        break;
      case 'administration':
        data.ALLOW_SIGNUP = formData.ALLOW_SIGNUP;
        data.ALLOW_ADMIN_APPROVED_SIGNUP = formData.ALLOW_ADMIN_APPROVED_SIGNUP;
        data.AUDIT_LOGGING = formData.AUDIT_LOGGING;
        break;
      case 'email':
        data.EMAIL_USE_TLS = formData.EMAIL_USE_TLS;
        data.EMAIL_HOST_USER = formData.EMAIL_HOST_USER;
        data.EMAIL_HOST_PASSWORD = formData.EMAIL_HOST_PASSWORD;
        data.EMAIL_HOST = formData.EMAIL_HOST;
        data.EMAIL_PORT = formData.EMAIL_PORT;
        data.EMAIL_FROM_ADDRESS = formData.EMAIL_FROM_ADDRESS;
        break;
      case 'data_retention':
        data.ORDER_DATA_RETENTION = formData.ORDER_DATA_RETENTION;
        data.TRACKER_DATA_RETENTION = formData.TRACKER_DATA_RETENTION;
        data.SHIPMENT_DATA_RETENTION = formData.SHIPMENT_DATA_RETENTION;
        data.API_LOGS_DATA_RETENTION = formData.API_LOGS_DATA_RETENTION;
        break;
      case 'api_keys':
        data.GOOGLE_CLOUD_API_KEY = formData.GOOGLE_CLOUD_API_KEY;
        data.CANADAPOST_ADDRESS_COMPLETE_API_KEY = formData.CANADAPOST_ADDRESS_COMPLETE_API_KEY;
        break;
      case 'features':
        data.ALLOW_MULTI_ACCOUNT = formData.ALLOW_MULTI_ACCOUNT;
        data.ADMIN_DASHBOARD = formData.ADMIN_DASHBOARD;
        data.MULTI_ORGANIZATIONS = formData.MULTI_ORGANIZATIONS;
        data.DOCUMENTS_MANAGEMENT = formData.DOCUMENTS_MANAGEMENT;
        data.DATA_IMPORT_EXPORT = formData.DATA_IMPORT_EXPORT;
        data.PERSIST_SDK_TRACING = formData.PERSIST_SDK_TRACING;
        data.WORKFLOW_MANAGEMENT = formData.WORKFLOW_MANAGEMENT;
        data.ORDERS_MANAGEMENT = formData.ORDERS_MANAGEMENT;
        data.APPS_MANAGEMENT = formData.APPS_MANAGEMENT;
        data.SHIPPING_RULES = formData.SHIPPING_RULES;
        break;
      case 'plugins': {
        const pluginFieldset = fieldsets.find(fs => fs.name === "Registry Plugins");
        pluginFieldset?.keys.forEach(key => { data[key] = formData[key]; });
        break;
      }
      default:
        if (section?.startsWith('dynamic_')) {
          const fsName = section.replace('dynamic_', '').replace(/_/g, ' ');
          const fs = fieldsets.find(f => f.name.toLowerCase() === fsName);
          fs?.keys.forEach(key => { data[key] = formData[key]; });
        }
        break;
    }

    onUpdate(data);
  };

  const handleChange = (key: keyof ConfigData, value: any) => {
    setFormData(prev => ({ ...prev, [key]: value }));
  };

  const renderContent = () => {
    switch (section) {
      case 'administration':
        return (
          <div className="divide-y">
            <div className="flex items-center justify-between py-3">
              <div className="space-y-0.5">
                <Label>Allow Signup</Label>
                <p className="text-sm text-muted-foreground">Allow user signup</p>
              </div>
              <Switch
                checked={formData.ALLOW_SIGNUP}
                onCheckedChange={(checked) => handleChange('ALLOW_SIGNUP', checked)}
              />
            </div>
            <div className="flex items-center justify-between py-3">
              <div className="space-y-0.5">
                <Label>Admin Approved Signup</Label>
                <p className="text-sm text-muted-foreground">User signup requires admin approval</p>
              </div>
              <Switch
                checked={formData.ALLOW_ADMIN_APPROVED_SIGNUP}
                onCheckedChange={(checked) => handleChange('ALLOW_ADMIN_APPROVED_SIGNUP', checked)}
              />
            </div>
            <div className="flex items-center justify-between py-3">
              <div className="space-y-0.5">
                <Label>Audit Logging</Label>
                <p className="text-sm text-muted-foreground">Enable audit logging for system activities</p>
              </div>
              <Switch
                checked={formData.AUDIT_LOGGING}
                onCheckedChange={(checked) => handleChange('AUDIT_LOGGING', checked)}
              />
            </div>
          </div>
        );

      case 'email':
        return (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="grid gap-2">
                <Label htmlFor="EMAIL_HOST">Host</Label>
                <Input
                  id="EMAIL_HOST"
                  placeholder="smtp.example.com"
                  value={formData.EMAIL_HOST || ""}
                  onChange={(e) => handleChange("EMAIL_HOST", e.target.value)}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="EMAIL_PORT">Port</Label>
                <Input
                  id="EMAIL_PORT"
                  type="number"
                  placeholder="587"
                  value={formData.EMAIL_PORT || ""}
                  onChange={(e) => handleChange("EMAIL_PORT", Number(e.target.value))}
                />
              </div>
            </div>
            <div className="grid gap-2">
              <Label htmlFor="EMAIL_HOST_USER">Username</Label>
              <Input
                id="EMAIL_HOST_USER"
                type="email"
                placeholder="admin@example.com"
                value={formData.EMAIL_HOST_USER || ""}
                onChange={(e) => handleChange("EMAIL_HOST_USER", e.target.value)}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="EMAIL_HOST_PASSWORD">Password</Label>
              <Input
                id="EMAIL_HOST_PASSWORD"
                type="password"
                value={formData.EMAIL_HOST_PASSWORD || ""}
                onChange={(e) => handleChange("EMAIL_HOST_PASSWORD", e.target.value)}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="EMAIL_FROM_ADDRESS">From Address</Label>
              <Input
                id="EMAIL_FROM_ADDRESS"
                type="email"
                placeholder="noreply@example.com"
                value={formData.EMAIL_FROM_ADDRESS || ""}
                onChange={(e) => handleChange("EMAIL_FROM_ADDRESS", e.target.value)}
              />
            </div>
            <div className="flex items-center justify-between pt-2 border-t">
              <Label htmlFor="EMAIL_USE_TLS">Use TLS Encryption</Label>
              <Switch
                id="EMAIL_USE_TLS"
                checked={formData.EMAIL_USE_TLS}
                onCheckedChange={(checked) => handleChange("EMAIL_USE_TLS", checked)}
              />
            </div>
          </div>
        );

      case 'data_retention':
        return (
          <div className="grid grid-cols-2 gap-4">
            <div className="grid gap-2">
              <Label htmlFor="ORDER_DATA_RETENTION">Orders (days)</Label>
              <Input
                id="ORDER_DATA_RETENTION"
                type="number"
                min={1}
                value={formData.ORDER_DATA_RETENTION || ""}
                onChange={(e) => handleChange("ORDER_DATA_RETENTION", Number(e.target.value))}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="SHIPMENT_DATA_RETENTION">Shipments (days)</Label>
              <Input
                id="SHIPMENT_DATA_RETENTION"
                type="number"
                min={1}
                value={formData.SHIPMENT_DATA_RETENTION || ""}
                onChange={(e) => handleChange("SHIPMENT_DATA_RETENTION", Number(e.target.value))}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="TRACKER_DATA_RETENTION">Trackers (days)</Label>
              <Input
                id="TRACKER_DATA_RETENTION"
                type="number"
                min={1}
                value={formData.TRACKER_DATA_RETENTION || ""}
                onChange={(e) => handleChange("TRACKER_DATA_RETENTION", Number(e.target.value))}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="API_LOGS_DATA_RETENTION">API Logs (days)</Label>
              <Input
                id="API_LOGS_DATA_RETENTION"
                type="number"
                min={1}
                value={formData.API_LOGS_DATA_RETENTION || ""}
                onChange={(e) => handleChange("API_LOGS_DATA_RETENTION", Number(e.target.value))}
              />
            </div>
          </div>
        );

      case 'api_keys':
        return (
          <div className="space-y-4">
            <div className="grid gap-2">
              <Label htmlFor="GOOGLE_CLOUD_API_KEY">Google Cloud API Key</Label>
              <Input
                id="GOOGLE_CLOUD_API_KEY"
                type="text"
                placeholder="Enter API key"
                value={formData.GOOGLE_CLOUD_API_KEY || ""}
                onChange={(e) => handleChange("GOOGLE_CLOUD_API_KEY", e.target.value)}
              />
              <p className="text-xs text-muted-foreground">Used for address validation services</p>
            </div>
            <div className="grid gap-2">
              <Label htmlFor="CANADAPOST_ADDRESS_COMPLETE_API_KEY">Canada Post Address Complete</Label>
              <Input
                id="CANADAPOST_ADDRESS_COMPLETE_API_KEY"
                type="text"
                placeholder="Enter API key"
                value={formData.CANADAPOST_ADDRESS_COMPLETE_API_KEY || ""}
                onChange={(e) => handleChange("CANADAPOST_ADDRESS_COMPLETE_API_KEY", e.target.value)}
              />
              <p className="text-xs text-muted-foreground">Used for Canadian address autocomplete</p>
            </div>
          </div>
        );

      case 'features':
        return (
          <div className="divide-y max-h-[60vh] overflow-y-auto">
            <div className="flex items-center justify-between py-3">
              <div className="space-y-0.5">
                <Label>Multi Account</Label>
                <p className="text-sm text-muted-foreground">Allow users to have multiple accounts</p>
              </div>
              <Switch
                checked={formData.ALLOW_MULTI_ACCOUNT}
                onCheckedChange={(checked) => handleChange("ALLOW_MULTI_ACCOUNT", checked)}
              />
            </div>
            <div className="flex items-center justify-between py-3">
              <div className="space-y-0.5">
                <Label>Admin Dashboard</Label>
                <p className="text-sm text-muted-foreground">Enable admin dashboard access</p>
              </div>
              <Switch
                checked={formData.ADMIN_DASHBOARD}
                onCheckedChange={(checked) => handleChange("ADMIN_DASHBOARD", checked)}
              />
            </div>
            <div className="flex items-center justify-between py-3">
              <div className="space-y-0.5">
                <Label>Multi Organizations</Label>
                <p className="text-sm text-muted-foreground">Enable multi-organization support</p>
              </div>
              <Switch
                checked={formData.MULTI_ORGANIZATIONS}
                onCheckedChange={(checked) => handleChange("MULTI_ORGANIZATIONS", checked)}
              />
            </div>
            <div className="flex items-center justify-between py-3">
              <div className="space-y-0.5">
                <Label>Documents Management</Label>
                <p className="text-sm text-muted-foreground">Enable documents management</p>
              </div>
              <Switch
                checked={formData.DOCUMENTS_MANAGEMENT}
                onCheckedChange={(checked) => handleChange("DOCUMENTS_MANAGEMENT", checked)}
              />
            </div>
            <div className="flex items-center justify-between py-3">
              <div className="space-y-0.5">
                <Label>Data Import/Export</Label>
                <p className="text-sm text-muted-foreground">Enable data import/export</p>
              </div>
              <Switch
                checked={formData.DATA_IMPORT_EXPORT}
                onCheckedChange={(checked) => handleChange("DATA_IMPORT_EXPORT", checked)}
              />
            </div>
            <div className="flex items-center justify-between py-3">
              <div className="space-y-0.5">
                <Label>Persist SDK Tracing</Label>
                <p className="text-sm text-muted-foreground">Persist SDK tracing</p>
              </div>
              <Switch
                checked={formData.PERSIST_SDK_TRACING}
                onCheckedChange={(checked) => handleChange("PERSIST_SDK_TRACING", checked)}
              />
            </div>
            <div className="flex items-center justify-between py-3">
              <div className="space-y-0.5">
                <Label>Workflow Management</Label>
                <p className="text-sm text-muted-foreground">Enable workflow management</p>
              </div>
              <Switch
                checked={formData.WORKFLOW_MANAGEMENT}
                onCheckedChange={(checked) => handleChange("WORKFLOW_MANAGEMENT", checked)}
              />
            </div>
            <div className="flex items-center justify-between py-3">
              <div className="space-y-0.5">
                <Label>Orders Management</Label>
                <p className="text-sm text-muted-foreground">Enable orders management functionality</p>
              </div>
              <Switch
                checked={formData.ORDERS_MANAGEMENT}
                onCheckedChange={(checked) => handleChange("ORDERS_MANAGEMENT", checked)}
              />
            </div>
            <div className="flex items-center justify-between py-3">
              <div className="space-y-0.5">
                <Label>Apps Management</Label>
                <p className="text-sm text-muted-foreground">Enable apps management functionality</p>
              </div>
              <Switch
                checked={formData.APPS_MANAGEMENT}
                onCheckedChange={(checked) => handleChange("APPS_MANAGEMENT", checked)}
              />
            </div>
            <div className="flex items-center justify-between py-3">
              <div className="space-y-0.5">
                <Label>Shipping Rules</Label>
                <p className="text-sm text-muted-foreground">Enable shipping rules functionality</p>
              </div>
              <Switch
                checked={formData.SHIPPING_RULES}
                onCheckedChange={(checked) => handleChange("SHIPPING_RULES", checked)}
              />
            </div>
          </div>
        );

      case 'platform':
        return (
          <div className="space-y-4">
            <div className="grid gap-2">
              <Label htmlFor="APP_NAME">Platform Name</Label>
              <Input
                id="APP_NAME"
                placeholder="My Platform"
                value={formData.APP_NAME || ""}
                onChange={(e) => handleChange("APP_NAME", e.target.value)}
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="APP_WEBSITE">Platform Website</Label>
              <Input
                id="APP_WEBSITE"
                placeholder="https://example.com"
                value={formData.APP_WEBSITE || ""}
                onChange={(e) => handleChange("APP_WEBSITE", e.target.value)}
              />
            </div>
          </div>
        );

      case 'plugins': {
        const pluginFieldset = fieldsets.find(fs => fs.name === "Registry Plugins");
        if (!pluginFieldset) return null;
        return (
          <div className="divide-y max-h-[60vh] overflow-y-auto">
            {pluginFieldset.keys.map(key => {
              const schemaDef = schema.find(s => s.key === key);
              return (
                <div key={key} className="flex items-center justify-between py-3">
                  <div className="space-y-0.5">
                    <Label>{schemaDef?.description || key}</Label>
                  </div>
                  <Switch
                    checked={!!formData[key]}
                    onCheckedChange={(checked) => handleChange(key as keyof ConfigData, checked)}
                  />
                </div>
              );
            })}
          </div>
        );
      }

      default:
        if (section?.startsWith('dynamic_')) {
          const fsName = section.replace('dynamic_', '').replace(/_/g, ' ');
          const fs = fieldsets.find(f => f.name.toLowerCase() === fsName);
          if (!fs) return null;
          return (
            <div className="space-y-4 max-h-[60vh] overflow-y-auto">
              {fs.keys.map(key => {
                const schemaDef = schema.find(s => s.key === key);
                const valueType = schemaDef?.value_type || 'str';
                if (valueType === 'bool') {
                  return (
                    <div key={key} className="flex items-center justify-between py-3 border-b last:border-0">
                      <div className="space-y-0.5">
                        <Label>{schemaDef?.description || key}</Label>
                      </div>
                      <Switch
                        checked={!!formData[key]}
                        onCheckedChange={(checked) => handleChange(key as keyof ConfigData, checked)}
                      />
                    </div>
                  );
                }
                return (
                  <div key={key} className="grid gap-2">
                    <Label htmlFor={key}>{schemaDef?.description || key}</Label>
                    <Input
                      id={key}
                      type={valueType === 'int' ? 'number' : 'text'}
                      placeholder={schemaDef?.default_value || ''}
                      value={formData[key] ?? ''}
                      onChange={(e) => handleChange(
                        key as keyof ConfigData,
                        valueType === 'int' ? Number(e.target.value) : e.target.value
                      )}
                    />
                  </div>
                );
              })}
            </div>
          );
        }
        return null;
    }
  };

  const titles: Record<string, string> = {
    administration: 'Edit Administration Settings',
    email: 'Edit Email Settings',
    data_retention: 'Edit Data Retention Settings',
    api_keys: 'Edit API Keys',
    features: 'Edit Features',
    platform: 'Edit Platform Details',
    plugins: 'Edit Plugin Registry',
  };

  const getTitle = (s: string) => {
    if (titles[s]) return titles[s];
    if (s.startsWith('dynamic_')) {
      const fsName = s.replace('dynamic_', '').replace(/_/g, ' ');
      const fs = fieldsets.find(f => f.name.toLowerCase() === fsName);
      return `Edit ${fs?.name || 'Settings'}`;
    }
    return 'Edit Settings';
  };

  if (!section) return null;

  return (
    <Dialog open={!!section} onOpenChange={() => onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <form onSubmit={handleSubmit} className="space-y-6">
          <DialogHeader>
            <DialogTitle>{getTitle(section)}</DialogTitle>
            <DialogDescription>Update your platform settings.</DialogDescription>
          </DialogHeader>
          {renderContent()}
          <DialogFooter className="gap-2 sm:gap-0">
            <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
            <Button type="submit">Save Changes</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
