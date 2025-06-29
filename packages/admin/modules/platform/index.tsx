"use client";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@karrio/ui/components/ui/card";
import { Switch } from "@karrio/ui/components/ui/switch";
import { Input } from "@karrio/ui/components/ui/input";
import { Button } from "@karrio/ui/components/ui/button";
import { Label } from "@karrio/ui/components/ui/label";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useConfigs, useConfigMutation } from "@karrio/hooks/admin-platform";
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
};

type ConfigResponse = {
  EMAIL_USE_TLS: boolean | null;
  EMAIL_HOST_USER: string | null;
  EMAIL_HOST_PASSWORD: string | null;
  EMAIL_HOST: string | null;
  EMAIL_PORT: number | null;
  EMAIL_FROM_ADDRESS: string | null;
  GOOGLE_CLOUD_API_KEY: string | null;
  CANADAPOST_ADDRESS_COMPLETE_API_KEY: string | null;
  ORDER_DATA_RETENTION: number | null;
  TRACKER_DATA_RETENTION: number | null;
  SHIPMENT_DATA_RETENTION: number | null;
  API_LOGS_DATA_RETENTION: number | null;
  APP_NAME: string | null;
  APP_WEBSITE: string | null;
  ALLOW_SIGNUP: boolean | null;
  ALLOW_ADMIN_APPROVED_SIGNUP: boolean | null;
  DOCUMENTS_MANAGEMENT: boolean | null;
  DATA_IMPORT_EXPORT: boolean | null;
  PERSIST_SDK_TRACING: boolean | null;
  WORKFLOW_MANAGEMENT: boolean | null;
  AUDIT_LOGGING: boolean | null;
  ALLOW_MULTI_ACCOUNT: boolean | null;
  ADMIN_DASHBOARD: boolean | null;
  ORDERS_MANAGEMENT: boolean | null;
  APPS_MANAGEMENT: boolean | null;
  MULTI_ORGANIZATIONS: boolean | null;
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
};

type EditSection = 'email' | 'administration' | 'data_retention' | 'api_keys' | 'features' | 'platform' | null;

export default function PlatformDetails() {
  const { toast } = useToast();
  const { metadata } = useAPIMetadata();
  const { query, configs } = useConfigs();
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

  const currentConfig = configs ? {
    ...defaultConfig,
    ...Object.fromEntries(
      Object.entries(configs).map(([key, value]) => [key, value === null ? defaultConfig[key as keyof ConfigData] : value])
    )
  } as ConfigData : defaultConfig;

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-semibold tracking-tight">
          Platform Overview
        </h1>
      </div>

      <div className="space-y-8">
        {/* Platform Config */}
        <Card>
          <CardHeader className="space-y-2">
            <CardTitle>Platform Details</CardTitle>
            <p className="text-sm text-muted-foreground">
              Overview of your platform configuration and API endpoints.
            </p>
          </CardHeader>
          <CardContent>
            <div className="rounded-lg border bg-card text-card-foreground shadow-sm mb-6">
              <div className="p-6 space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <Label className="text-xs text-muted-foreground">Platform Name</Label>
                    <p className="text-sm font-medium mt-1">{currentConfig.APP_NAME || metadata?.APP_NAME}</p>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => setEditSection('platform')}
                  >
                    <Pencil className="h-4 w-4" />
                  </Button>
                </div>
                <div>
                  <Label className="text-xs text-muted-foreground">Platform Website</Label>
                  <div className="flex items-center gap-2 mt-1 group">
                    <p className="text-sm font-medium">{currentConfig.APP_WEBSITE || metadata?.APP_WEBSITE}</p>
                    <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6"
                        onClick={() => {
                          navigator.clipboard.writeText(currentConfig.APP_WEBSITE || metadata?.APP_WEBSITE || "");
                          toast({ title: "Copied to clipboard" });
                        }}
                      >
                        <Copy className="h-3.5 w-3.5" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6"
                        onClick={() => window.open(currentConfig.APP_WEBSITE || metadata?.APP_WEBSITE, '_blank')}
                      >
                        <ExternalLink className="h-3.5 w-3.5" />
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="rounded-lg border bg-card text-card-foreground shadow-sm">
              <div className="p-6 space-y-4">
                <div>
                  <Label className="text-xs text-muted-foreground">API Host</Label>
                  <div className="flex items-center gap-2 mt-1 group">
                    <p className="text-sm font-medium">{metadata?.HOST}</p>
                    <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6"
                        onClick={() => {
                          navigator.clipboard.writeText(metadata?.HOST || "");
                          toast({ title: "Copied to clipboard" });
                        }}
                      >
                        <Copy className="h-3.5 w-3.5" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6"
                        onClick={() => window.open(metadata?.HOST, '_blank')}
                      >
                        <ExternalLink className="h-3.5 w-3.5" />
                      </Button>
                    </div>
                  </div>
                </div>
                <div>
                  <Label className="text-xs text-muted-foreground">GraphQL Endpoint</Label>
                  <div className="flex items-center gap-2 mt-1 group">
                    <p className="text-sm font-medium">{metadata?.GRAPHQL}</p>
                    <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6"
                        onClick={() => {
                          navigator.clipboard.writeText(metadata?.GRAPHQL || "");
                          toast({ title: "Copied to clipboard" });
                        }}
                      >
                        <Copy className="h-3.5 w-3.5" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6"
                        onClick={() => window.open(metadata?.GRAPHQL, '_blank')}
                      >
                        <ExternalLink className="h-3.5 w-3.5" />
                      </Button>
                    </div>
                  </div>
                </div>
                <div>
                  <Label className="text-xs text-muted-foreground">OpenAPI Endpoint</Label>
                  <div className="flex items-center gap-2 mt-1 group">
                    <p className="text-sm font-medium">{metadata?.OPENAPI}</p>
                    <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6"
                        onClick={() => {
                          navigator.clipboard.writeText(metadata?.OPENAPI || "");
                          toast({ title: "Copied to clipboard" });
                        }}
                      >
                        <Copy className="h-3.5 w-3.5" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6"
                        onClick={() => window.open(metadata?.OPENAPI, '_blank')}
                      >
                        <ExternalLink className="h-3.5 w-3.5" />
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Administration */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
            <div className="space-y-2">
              <CardTitle>Administration</CardTitle>
              <p className="text-sm text-muted-foreground">
                Configure user access and platform behavior settings.
              </p>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setEditSection('administration')}
            >
              <Pencil className="h-4 w-4" />
            </Button>
          </CardHeader>
          <CardContent>
            <div className="rounded-lg border bg-card text-card-foreground shadow-sm">
              <div className="p-6 space-y-6">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Allow Signup</Label>
                    <p className="text-sm text-muted-foreground">Allow user signup</p>
                  </div>
                  {currentConfig.ALLOW_SIGNUP ? (
                    <Check className="h-4 w-4 text-green-500" />
                  ) : (
                    <X className="h-4 w-4 text-muted-foreground" />
                  )}
                </div>
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Admin Approved Signup</Label>
                    <p className="text-sm text-muted-foreground">User signup requires admin approval</p>
                  </div>
                  {currentConfig.ALLOW_ADMIN_APPROVED_SIGNUP ? (
                    <Check className="h-4 w-4 text-green-500" />
                  ) : (
                    <X className="h-4 w-4 text-muted-foreground" />
                  )}
                </div>
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Audit Logging</Label>
                    <p className="text-sm text-muted-foreground">Enable audit logging for system activities</p>
                  </div>
                  {currentConfig.AUDIT_LOGGING ? (
                    <Check className="h-4 w-4 text-green-500" />
                  ) : (
                    <X className="h-4 w-4 text-muted-foreground" />
                  )}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Features */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <div>
              <CardTitle>Features</CardTitle>
              <p className="text-sm text-muted-foreground">
                Configure platform features and capabilities.
              </p>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setEditSection('features')}
            >
              <Pencil className="h-4 w-4" />
            </Button>
          </CardHeader>
          <CardContent>
            <div className="rounded-lg border bg-card text-card-foreground shadow-sm">
              <div className="p-6 space-y-6">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Multi Account</Label>
                    <p className="text-sm text-muted-foreground">Allow users to have multiple accounts</p>
                  </div>
                  {currentConfig.ALLOW_MULTI_ACCOUNT ? (
                    <Check className="h-4 w-4 text-green-500" />
                  ) : (
                    <X className="h-4 w-4 text-muted-foreground" />
                  )}
                </div>
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Admin Dashboard</Label>
                    <p className="text-sm text-muted-foreground">Enable admin dashboard access</p>
                  </div>
                  {currentConfig.ADMIN_DASHBOARD ? (
                    <Check className="h-4 w-4 text-green-500" />
                  ) : (
                    <X className="h-4 w-4 text-muted-foreground" />
                  )}
                </div>
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Multi Organizations</Label>
                    <p className="text-sm text-muted-foreground">Enable multi-organization support</p>
                  </div>
                  {currentConfig.MULTI_ORGANIZATIONS ? (
                    <Check className="h-4 w-4 text-green-500" />
                  ) : (
                    <X className="h-4 w-4 text-muted-foreground" />
                  )}
                </div>
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Documents Management</Label>
                    <p className="text-sm text-muted-foreground">Enable documents management</p>
                  </div>
                  {currentConfig.DOCUMENTS_MANAGEMENT ? (
                    <Check className="h-4 w-4 text-green-500" />
                  ) : (
                    <X className="h-4 w-4 text-muted-foreground" />
                  )}
                </div>
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Data Import/Export</Label>
                    <p className="text-sm text-muted-foreground">Enable data import/export</p>
                  </div>
                  {currentConfig.DATA_IMPORT_EXPORT ? (
                    <Check className="h-4 w-4 text-green-500" />
                  ) : (
                    <X className="h-4 w-4 text-muted-foreground" />
                  )}
                </div>
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Persist SDK Tracing</Label>
                    <p className="text-sm text-muted-foreground">Persist SDK tracing</p>
                  </div>
                  {currentConfig.PERSIST_SDK_TRACING ? (
                    <Check className="h-4 w-4 text-green-500" />
                  ) : (
                    <X className="h-4 w-4 text-muted-foreground" />
                  )}
                </div>
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Workflow Management</Label>
                    <p className="text-sm text-muted-foreground">Enable workflow management</p>
                  </div>
                  {currentConfig.WORKFLOW_MANAGEMENT ? (
                    <Check className="h-4 w-4 text-green-500" />
                  ) : (
                    <X className="h-4 w-4 text-muted-foreground" />
                  )}
                </div>
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Orders Management</Label>
                    <p className="text-sm text-muted-foreground">Enable orders management functionality</p>
                  </div>
                  {currentConfig.ORDERS_MANAGEMENT ? (
                    <Check className="h-4 w-4 text-green-500" />
                  ) : (
                    <X className="h-4 w-4 text-muted-foreground" />
                  )}
                </div>
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Apps Management</Label>
                    <p className="text-sm text-muted-foreground">Enable apps management functionality</p>
                  </div>
                  {currentConfig.APPS_MANAGEMENT ? (
                    <Check className="h-4 w-4 text-green-500" />
                  ) : (
                    <X className="h-4 w-4 text-muted-foreground" />
                  )}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Email Config */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <div>
              <CardTitle>Email Configuration</CardTitle>
              <p className="text-sm text-muted-foreground">
                Configure SMTP settings for sending system emails and notifications.
              </p>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setEditSection('email')}
            >
              <Pencil className="h-4 w-4" />
            </Button>
          </CardHeader>
          <CardContent>
            <div className="rounded-lg border bg-card text-card-foreground shadow-sm">
              <div className="p-6 space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label>Email Host</Label>
                    <p className="text-sm text-muted-foreground">{currentConfig.EMAIL_HOST || 'Not configured'}</p>
                  </div>
                  <div>
                    <Label>Email Port</Label>
                    <p className="text-sm text-muted-foreground">{currentConfig.EMAIL_PORT || 'Not configured'}</p>
                  </div>
                  <div>
                    <Label>Email User</Label>
                    <p className="text-sm text-muted-foreground">{currentConfig.EMAIL_HOST_USER || 'Not configured'}</p>
                  </div>
                  <div>
                    <Label>From Address</Label>
                    <p className="text-sm text-muted-foreground">{currentConfig.EMAIL_FROM_ADDRESS || 'Not configured'}</p>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Data Retention */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <div>
              <CardTitle>Data Retention</CardTitle>
              <p className="text-sm text-muted-foreground">
                Set retention periods for different types of data before automatic cleanup.
              </p>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setEditSection('data_retention')}
            >
              <Pencil className="h-4 w-4" />
            </Button>
          </CardHeader>
          <CardContent>
            <div className="rounded-lg border bg-card text-card-foreground shadow-sm">
              <div className="p-6 space-y-6">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label>Orders Retention</Label>
                    <p className="text-sm text-muted-foreground">{currentConfig.ORDER_DATA_RETENTION || 90} days</p>
                  </div>
                  <div>
                    <Label>Shipments Retention</Label>
                    <p className="text-sm text-muted-foreground">{currentConfig.SHIPMENT_DATA_RETENTION || 90} days</p>
                  </div>
                  <div>
                    <Label>API Logs Retention</Label>
                    <p className="text-sm text-muted-foreground">{currentConfig.API_LOGS_DATA_RETENTION || 30} days</p>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* API Keys */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <div>
              <CardTitle>Address Validation & Autocomplete</CardTitle>
              <p className="text-sm text-muted-foreground">
                Configure third-party services for address validation and autocomplete functionality.
              </p>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setEditSection('api_keys')}
            >
              <Pencil className="h-4 w-4" />
            </Button>
          </CardHeader>
          <CardContent>
            <div className="rounded-lg border bg-card text-card-foreground shadow-sm">
              <div className="p-6 space-y-6">
                <div>
                  <Label>Google Cloud API Key</Label>
                  <p className="text-sm text-muted-foreground">
                    {currentConfig.GOOGLE_CLOUD_API_KEY ? '••••••••' : 'Not configured'}
                  </p>
                </div>
                <div>
                  <Label>Canada Post Address Complete API Key</Label>
                  <p className="text-sm text-muted-foreground">
                    {currentConfig.CANADAPOST_ADDRESS_COMPLETE_API_KEY ? '••••••••' : 'Not configured'}
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <EditDialog
        section={editSection}
        onClose={() => setEditSection(null)}
        configs={currentConfig}
        onUpdate={handleUpdate}
      />
    </div>
  );
}

function EditDialog({
  section,
  onClose,
  configs,
  onUpdate
}: {
  section: EditSection;
  onClose: () => void;
  configs: ConfigData;
  onUpdate: (data: Partial<ConfigData>) => void;
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
          <div className="space-y-4 p-4 pb-8">
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Allow Signup</Label>
                <p className="text-sm text-muted-foreground">Allow user signup</p>
              </div>
              <Switch
                checked={formData.ALLOW_SIGNUP}
                onCheckedChange={(checked) => handleChange('ALLOW_SIGNUP', checked)}
              />
            </div>
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Admin Approved Signup</Label>
                <p className="text-sm text-muted-foreground">User signup requires admin approval</p>
              </div>
              <Switch
                checked={formData.ALLOW_ADMIN_APPROVED_SIGNUP}
                onCheckedChange={(checked) => handleChange('ALLOW_ADMIN_APPROVED_SIGNUP', checked)}
              />
            </div>
            <div className="flex items-center justify-between">
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
          <div className="space-y-4 p-4 pb-8">
            <div className="space-y-2">
              <Label htmlFor="EMAIL_HOST">Email Host</Label>
              <Input
                id="EMAIL_HOST"
                placeholder="smtp.example.com"
                value={formData.EMAIL_HOST || ""}
                onChange={(e) => handleChange("EMAIL_HOST", e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="EMAIL_PORT">Email Port</Label>
              <Input
                id="EMAIL_PORT"
                type="number"
                placeholder="587"
                value={formData.EMAIL_PORT || ""}
                onChange={(e) => handleChange("EMAIL_PORT", Number(e.target.value))}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="EMAIL_HOST_USER">Email User</Label>
              <Input
                id="EMAIL_HOST_USER"
                type="email"
                placeholder="admin@example.com"
                value={formData.EMAIL_HOST_USER || ""}
                onChange={(e) => handleChange("EMAIL_HOST_USER", e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="EMAIL_HOST_PASSWORD">Email Password</Label>
              <Input
                id="EMAIL_HOST_PASSWORD"
                type="password"
                value={formData.EMAIL_HOST_PASSWORD || ""}
                onChange={(e) => handleChange("EMAIL_HOST_PASSWORD", e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="EMAIL_FROM_ADDRESS">From Address</Label>
              <Input
                id="EMAIL_FROM_ADDRESS"
                type="email"
                placeholder="noreply@example.com"
                value={formData.EMAIL_FROM_ADDRESS || ""}
                onChange={(e) => handleChange("EMAIL_FROM_ADDRESS", e.target.value)}
              />
            </div>
            <div className="flex items-center space-x-2">
              <Switch
                id="EMAIL_USE_TLS"
                checked={formData.EMAIL_USE_TLS}
                onCheckedChange={(checked) => handleChange("EMAIL_USE_TLS", checked)}
              />
              <Label htmlFor="EMAIL_USE_TLS">Use TLS</Label>
            </div>
          </div>
        );

      case 'data_retention':
        return (
          <div className="space-y-4 p-4 pb-8">
            <div className="space-y-2">
              <Label htmlFor="ORDER_DATA_RETENTION">Orders Retention (days)</Label>
              <Input
                id="ORDER_DATA_RETENTION"
                type="number"
                min={1}
                value={formData.ORDER_DATA_RETENTION || ""}
                onChange={(e) => handleChange("ORDER_DATA_RETENTION", Number(e.target.value))}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="SHIPMENT_DATA_RETENTION">Shipments Retention (days)</Label>
              <Input
                id="SHIPMENT_DATA_RETENTION"
                type="number"
                min={1}
                value={formData.SHIPMENT_DATA_RETENTION || ""}
                onChange={(e) => handleChange("SHIPMENT_DATA_RETENTION", Number(e.target.value))}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="API_LOGS_DATA_RETENTION">API Logs Retention (days)</Label>
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
          <div className="space-y-4 p-4 pb-8">
            <div className="space-y-2">
              <Label htmlFor="GOOGLE_CLOUD_API_KEY">Google Cloud API Key</Label>
              <Input
                id="GOOGLE_CLOUD_API_KEY"
                type="text"
                value={formData.GOOGLE_CLOUD_API_KEY || ""}
                onChange={(e) => handleChange("GOOGLE_CLOUD_API_KEY", e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="CANADAPOST_ADDRESS_COMPLETE_API_KEY">Canada Post Address Complete API Key</Label>
              <Input
                id="CANADAPOST_ADDRESS_COMPLETE_API_KEY"
                type="text"
                value={formData.CANADAPOST_ADDRESS_COMPLETE_API_KEY || ""}
                onChange={(e) => handleChange("CANADAPOST_ADDRESS_COMPLETE_API_KEY", e.target.value)}
              />
            </div>
          </div>
        );

      case 'features':
        return (
          <div className="space-y-4 p-4 pb-8">
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Multi Account</Label>
                <p className="text-sm text-muted-foreground">Allow users to have multiple accounts</p>
              </div>
              <Switch
                checked={formData.ALLOW_MULTI_ACCOUNT}
                onCheckedChange={(checked) => handleChange("ALLOW_MULTI_ACCOUNT", checked)}
              />
            </div>
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Admin Dashboard</Label>
                <p className="text-sm text-muted-foreground">Enable admin dashboard access</p>
              </div>
              <Switch
                checked={formData.ADMIN_DASHBOARD}
                onCheckedChange={(checked) => handleChange("ADMIN_DASHBOARD", checked)}
              />
            </div>
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Multi Organizations</Label>
                <p className="text-sm text-muted-foreground">Enable multi-organization support</p>
              </div>
              <Switch
                checked={formData.MULTI_ORGANIZATIONS}
                onCheckedChange={(checked) => handleChange("MULTI_ORGANIZATIONS", checked)}
              />
            </div>
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Documents Management</Label>
                <p className="text-sm text-muted-foreground">Enable documents management</p>
              </div>
              <Switch
                checked={formData.DOCUMENTS_MANAGEMENT}
                onCheckedChange={(checked) => handleChange("DOCUMENTS_MANAGEMENT", checked)}
              />
            </div>
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Data Import/Export</Label>
                <p className="text-sm text-muted-foreground">Enable data import/export</p>
              </div>
              <Switch
                checked={formData.DATA_IMPORT_EXPORT}
                onCheckedChange={(checked) => handleChange("DATA_IMPORT_EXPORT", checked)}
              />
            </div>
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Persist SDK Tracing</Label>
                <p className="text-sm text-muted-foreground">Persist SDK tracing</p>
              </div>
              <Switch
                checked={formData.PERSIST_SDK_TRACING}
                onCheckedChange={(checked) => handleChange("PERSIST_SDK_TRACING", checked)}
              />
            </div>
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Workflow Management</Label>
                <p className="text-sm text-muted-foreground">Enable workflow management</p>
              </div>
              <Switch
                checked={formData.WORKFLOW_MANAGEMENT}
                onCheckedChange={(checked) => handleChange("WORKFLOW_MANAGEMENT", checked)}
              />
            </div>
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Orders Management</Label>
                <p className="text-sm text-muted-foreground">Enable orders management functionality</p>
              </div>
              <Switch
                checked={formData.ORDERS_MANAGEMENT}
                onCheckedChange={(checked) => handleChange("ORDERS_MANAGEMENT", checked)}
              />
            </div>
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>Apps Management</Label>
                <p className="text-sm text-muted-foreground">Enable apps management functionality</p>
              </div>
              <Switch
                checked={formData.APPS_MANAGEMENT}
                onCheckedChange={(checked) => handleChange("APPS_MANAGEMENT", checked)}
              />
            </div>
          </div>
        );

      case 'platform':
        return (
          <div className="space-y-4 p-4 pb-8">
            <div className="space-y-2">
              <Label htmlFor="APP_NAME">Platform Name</Label>
              <Input
                id="APP_NAME"
                placeholder="My Platform"
                value={formData.APP_NAME || ""}
                onChange={(e) => handleChange("APP_NAME", e.target.value)}
              />
            </div>
            <div className="space-y-2">
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

      default:
        return null;
    }
  };

  const titles = {
    administration: 'Edit Administration Settings',
    email: 'Edit Email Settings',
    data_retention: 'Edit Data Retention Settings',
    api_keys: 'Edit API Keys',
    features: 'Edit Features',
    platform: 'Edit Platform Details',
  };

  if (!section) return null;

  return (
    <Dialog open={!!section} onOpenChange={() => onClose()}>
      <DialogContent className="sm:max-w-[500px] bg-background">
        <DialogHeader className="space-y-2">
          <DialogTitle>{titles[section]}</DialogTitle>
          <DialogDescription>
            Update your platform settings.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="mt-4">
          {renderContent()}
          <DialogFooter className="mt-8">
            <Button type="submit">Save Changes</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
