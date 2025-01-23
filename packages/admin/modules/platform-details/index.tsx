"use client";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@karrio/insiders/components/ui/card";
import { Switch } from "@karrio/insiders/components/ui/switch";
import { Input } from "@karrio/insiders/components/ui/input";
import { Button } from "@karrio/insiders/components/ui/button";
import { Label } from "@karrio/insiders/components/ui/label";
import { useToast } from "@karrio/insiders/hooks/use-toast";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { trpc } from "@karrio/trpc/client";
import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@karrio/insiders/components/ui/dialog";

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
};

type EditSection = 'email' | 'administration' | 'data_retention' | 'api_keys' | null;

export default function PlatformDetails() {
  const { toast } = useToast();
  const { metadata } = useAPIMetadata();
  const utils = trpc.useContext();
  const { data: configs } = trpc.admin.configs.list.useQuery<ConfigResponse>();
  const [editSection, setEditSection] = useState<EditSection>(null);

  const { mutate: updateConfigs } = trpc.admin.configs.update.useMutation({
    onSuccess: () => {
      toast({ title: "Settings saved successfully" });
      utils.admin.configs.list.invalidate();
      setEditSection(null);
    },
    onError: (error) => {
      toast({
        title: "Failed to save settings",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const handleUpdate = (data: Partial<ConfigData>) => {
    updateConfigs({ data });
  };

  const currentConfig = configs ? {
    ...defaultConfig,
    ...Object.fromEntries(
      Object.entries(configs).map(([key, value]) => [key, value === null ? defaultConfig[key as keyof ConfigData] : value])
    )
  } as ConfigData : defaultConfig;

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold tracking-tight">
          Platform Overview
        </h1>
      </div>

      <div className="space-y-6">
        {/* Platform Config */}
        <Card>
          <CardHeader>
            <CardTitle>Platform Details</CardTitle>
            <p className="text-sm text-muted-foreground">
              Overview of your platform configuration and API endpoints.
            </p>
          </CardHeader>
          <CardContent>
            <div className="rounded-lg border bg-card text-card-foreground shadow-sm">
              <div className="p-4 space-y-3">
                <div>
                  <Label className="text-xs text-muted-foreground">Platform Name</Label>
                  <p className="text-sm font-medium">{metadata?.APP_NAME}</p>
                </div>
                <div>
                  <Label className="text-xs text-muted-foreground">Platform Website</Label>
                  <p className="text-sm font-medium">{metadata?.APP_WEBSITE}</p>
                </div>
                <div>
                  <Label className="text-xs text-muted-foreground">API Host</Label>
                  <p className="text-sm font-medium">{metadata?.HOST}</p>
                </div>
                <div>
                  <Label className="text-xs text-muted-foreground">GraphQL Endpoint</Label>
                  <p className="text-sm font-medium">{metadata?.GRAPHQL}</p>
                </div>
                <div>
                  <Label className="text-xs text-muted-foreground">OpenAPI Endpoint</Label>
                  <p className="text-sm font-medium">{metadata?.OPENAPI}</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Administration */}
        <Card>
          <CardHeader>
            <CardTitle>Administration</CardTitle>
            <p className="text-sm text-muted-foreground">
              Configure user access and platform behavior settings.
            </p>
          </CardHeader>
          <CardContent>
            <div className="rounded-lg border bg-card text-card-foreground shadow-sm">
              <div className="p-6 space-y-6">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Allow Signup</Label>
                    <p className="text-sm text-muted-foreground">Allow user signup</p>
                  </div>
                  <Switch checked={currentConfig.ALLOW_SIGNUP} disabled />
                </div>
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label>Admin Approved Signup</Label>
                    <p className="text-sm text-muted-foreground">User signup requires admin approval</p>
                  </div>
                  <Switch checked={currentConfig.ALLOW_ADMIN_APPROVED_SIGNUP} disabled />
                </div>
              </div>
            </div>
            <div className="mt-4 flex justify-end">
              <Button onClick={() => setEditSection('administration')}>Edit Administration Settings</Button>
            </div>
          </CardContent>
        </Card>

        {/* Email Config */}
        <Card>
          <CardHeader>
            <CardTitle>Email Configuration</CardTitle>
            <p className="text-sm text-muted-foreground">
              Configure SMTP settings for sending system emails and notifications.
            </p>
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
            <div className="mt-4 flex justify-end">
              <Button onClick={() => setEditSection('email')}>Edit Email Settings</Button>
            </div>
          </CardContent>
        </Card>

        {/* Data Retention */}
        <Card>
          <CardHeader>
            <CardTitle>Data Retention</CardTitle>
            <p className="text-sm text-muted-foreground">
              Set retention periods for different types of data before automatic cleanup.
            </p>
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
            <div className="mt-4 flex justify-end">
              <Button onClick={() => setEditSection('data_retention')}>Edit Retention Settings</Button>
            </div>
          </CardContent>
        </Card>

        {/* API Keys */}
        <Card>
          <CardHeader>
            <CardTitle>Address Validation & Autocomplete</CardTitle>
            <p className="text-sm text-muted-foreground">
              Configure third-party services for address validation and autocomplete functionality.
            </p>
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
            <div className="mt-4 flex justify-end">
              <Button onClick={() => setEditSection('api_keys')}>Edit API Keys</Button>
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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const data: Partial<ConfigData> = {};

    switch (section) {
      case 'administration':
        data.ALLOW_SIGNUP = formData.ALLOW_SIGNUP;
        data.ALLOW_ADMIN_APPROVED_SIGNUP = formData.ALLOW_ADMIN_APPROVED_SIGNUP;
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
          <div className="space-y-4">
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
          </div>
        );

      case 'email':
        return (
          <div className="space-y-4">
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
          <div className="space-y-4">
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
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="GOOGLE_CLOUD_API_KEY">Google Cloud API Key</Label>
              <Input
                id="GOOGLE_CLOUD_API_KEY"
                type="password"
                value={formData.GOOGLE_CLOUD_API_KEY || ""}
                onChange={(e) => handleChange("GOOGLE_CLOUD_API_KEY", e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="CANADAPOST_ADDRESS_COMPLETE_API_KEY">Canada Post Address Complete API Key</Label>
              <Input
                id="CANADAPOST_ADDRESS_COMPLETE_API_KEY"
                type="password"
                value={formData.CANADAPOST_ADDRESS_COMPLETE_API_KEY || ""}
                onChange={(e) => handleChange("CANADAPOST_ADDRESS_COMPLETE_API_KEY", e.target.value)}
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
  };

  if (!section) return null;

  return (
    <Dialog open={!!section} onOpenChange={() => onClose()}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{titles[section]}</DialogTitle>
          <DialogDescription>
            Update your platform settings.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          {renderContent()}
          <DialogFooter className="mt-6">
            <Button type="submit">Save Changes</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
