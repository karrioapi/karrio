import React, { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { AlertTriangle, Save, X, Settings, FileText, Package, Globe } from "lucide-react";
import { Alert, AlertDescription } from "./ui/alert";
import {
  useWorkspaceConfig,
  useWorkspaceConfigMutation
} from "@karrio/hooks/workspace-config";
import { useUser } from "@karrio/hooks/user";
import { useUserMutation } from "@karrio/hooks/user";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { COUNTRY_OPTIONS, CURRENCY_OPTIONS } from "@karrio/types";
import { useNotifier } from "@karrio/ui/core/components/notifier";
import { NotificationType } from "@karrio/types";
import { useRouter } from "next/navigation";
import { Switch } from "./ui/switch";
import { Package as PackageIcon } from "lucide-react";

interface WorkspaceConfigFieldProps {
  label: string;
  description?: string;
  value: string | boolean;
  originalValue: string | boolean;
  onSave: () => void;
  onCancel: () => void;
  loading?: boolean;
  disabled?: boolean;
  children: React.ReactNode;
}

function WorkspaceConfigField({
  label,
  description,
  value,
  originalValue,
  onSave,
  onCancel,
  loading,
  disabled,
  children
}: WorkspaceConfigFieldProps) {
  const hasChanges = value !== originalValue;

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <div className="space-y-1">
          <Label className="text-sm font-medium">{label}</Label>
          {description && (
            <p className="text-sm text-muted-foreground">{description}</p>
          )}
        </div>
        {hasChanges && (
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={onCancel}
              disabled={loading}
            >
              <X className="h-3 w-3 mr-1" />
              Cancel
            </Button>
            <Button
              size="sm"
              onClick={onSave}
              disabled={loading}
            >
              <Save className="h-3 w-3 mr-1" />
              Save
            </Button>
          </div>
        )}
      </div>
      <div className="flex-1">
        {children}
      </div>
    </div>
  );
}

interface CloseAccountDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

function CloseAccountDialog({ open, onOpenChange }: CloseAccountDialogProps) {
  const mutation = useUserMutation();
  const { notify } = useNotifier();
  const [loading, setLoading] = React.useState(false);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);

    try {
      await mutation.closeAccount.mutateAsync();
      notify({
        type: NotificationType.success,
        message: "Account closed successfully"
      });
      // Redirect handled by mutation
    } catch (error: any) {
      notify({
        type: NotificationType.error,
        message: error.message || "Failed to close account"
      });
    } finally {
      setLoading(false);
    }
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm">
      <div className="fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 sm:rounded-lg">
        <div className="space-y-4">
          <div className="space-y-2">
            <h2 className="text-lg font-semibold">Close Account</h2>
            <p className="text-sm text-muted-foreground">
              This action cannot be undone. You will lose access to all your data and services.
            </p>
          </div>

          <Alert>
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>
              All your data, shipments, and configurations will be permanently deleted.
            </AlertDescription>
          </Alert>

          <form onSubmit={handleSubmit} className="flex justify-end gap-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={loading}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="destructive"
              disabled={loading}
            >
              {loading ? "Closing..." : "Close Account"}
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}

export function AccountSettings() {
  const router = useRouter();
  const { references } = useAPIMetadata();
  const { notify } = useNotifier();
  const [isCloseAccountOpen, setIsCloseAccountOpen] = useState(false);

  const { query } = useWorkspaceConfig();
  const { updateWorkspaceConfig } = useWorkspaceConfigMutation();
  const workspace_config = query.data?.workspace_config;

  const [formData, setFormData] = useState<any>({});
  const [editingFields, setEditingFields] = useState<Set<string>>(new Set());
  const [loadingFields, setLoadingFields] = useState<Set<string>>(new Set());

  useEffect(() => {
    if (workspace_config) {
      setFormData({
        default_currency: workspace_config.default_currency || '',
        default_country_code: workspace_config.default_country_code || '',
        default_label_type: workspace_config.default_label_type || '',
        default_weight_unit: workspace_config.default_weight_unit || '',
        default_dimension_unit: workspace_config.default_dimension_unit || '',
        state_tax_id: workspace_config.state_tax_id || '',
        federal_tax_id: workspace_config.federal_tax_id || '',
        customs_aes: workspace_config.customs_aes || '',
        customs_eel_pfc: workspace_config.customs_eel_pfc || '',
        customs_license_number: workspace_config.customs_license_number || '',
        customs_certificate_number: workspace_config.customs_certificate_number || '',
        customs_nip_number: workspace_config.customs_nip_number || '',
        customs_eori_number: workspace_config.customs_eori_number || '',
        customs_vat_registration_number: workspace_config.customs_vat_registration_number || '',
        insured_by_default: workspace_config.insured_by_default || false,
      });
    }
  }, [workspace_config]);

  const updateField = (field: string, value: any) => {
    setFormData((prev: any) => ({ ...prev, [field]: value }));
    setEditingFields(prev => new Set(prev).add(field));
  };

  const saveField = async (field: string) => {
    setLoadingFields(prev => new Set(prev).add(field));
    try {
      await updateWorkspaceConfig.mutateAsync({ [field]: formData[field] });
      setEditingFields(prev => {
        const next = new Set(prev);
        next.delete(field);
        return next;
      });
      notify({
        type: NotificationType.success,
        message: "Settings updated successfully"
      });
    } catch (error: any) {
      notify({
        type: NotificationType.error,
        message: error.message || "Failed to update settings"
      });
    } finally {
      setLoadingFields(prev => {
        const next = new Set(prev);
        next.delete(field);
        return next;
      });
    }
  };

  const cancelField = (field: string) => {
    setFormData((prev: any) => ({
      ...prev,
      [field]: workspace_config?.[field as keyof typeof workspace_config] || ''
    }));
    setEditingFields(prev => {
      const next = new Set(prev);
      next.delete(field);
      return next;
    });
  };

  // Define options for selects
  const CURRENCY_OPTIONS = ['USD', 'EUR', 'CAD', 'GBP', 'AUD', 'JPY'];
  const COUNTRY_OPTIONS = ['US', 'CA', 'GB', 'DE', 'FR', 'AU', 'JP'];
  const LABEL_TYPE_OPTIONS = ['PDF', 'ZPL', 'PNG'];
  const WEIGHT_UNIT_OPTIONS = ['KG', 'LB'];
  const DIMENSION_UNIT_OPTIONS = ['CM', 'IN'];

  return (
    <div className="space-y-6">
      {/* General Defaults */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings className="h-5 w-5" />
            General Defaults
          </CardTitle>
          <CardDescription>
            Set up preferences for your {references?.APP_NAME || "Karrio"} account.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="max-w-md space-y-6">
            <WorkspaceConfigField
              label="Default Currency"
              description="Currency used for pricing and billing"
              value={formData.default_currency}
              originalValue={workspace_config?.default_currency || ''}
              onSave={() => saveField('default_currency')}
              onCancel={() => cancelField('default_currency')}
              loading={loadingFields.has('default_currency')}
            >
              <Select
                value={formData.default_currency}
                onValueChange={(value) => updateField('default_currency', value)}
              >
                <SelectTrigger className="h-8">
                  <SelectValue placeholder="Select a currency" />
                </SelectTrigger>
                <SelectContent>
                  {CURRENCY_OPTIONS.map((currency) => (
                    <SelectItem key={currency} value={currency}>
                      {currency}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </WorkspaceConfigField>

            <WorkspaceConfigField
              label="Default Country"
              description="Default country for shipping addresses"
              value={formData.default_country_code}
              originalValue={workspace_config?.default_country_code || ''}
              onSave={() => saveField('default_country_code')}
              onCancel={() => cancelField('default_country_code')}
              loading={loadingFields.has('default_country_code')}
            >
              <Select
                value={formData.default_country_code}
                onValueChange={(value) => updateField('default_country_code', value)}
              >
                <SelectTrigger className="h-8">
                  <SelectValue placeholder="Select a country" />
                </SelectTrigger>
                <SelectContent>
                  {COUNTRY_OPTIONS.map((country) => (
                    <SelectItem key={country} value={country}>
                      {country}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </WorkspaceConfigField>

            <WorkspaceConfigField
              label="Default Label Type"
              description="Default format for shipping labels"
              value={formData.default_label_type}
              originalValue={workspace_config?.default_label_type || ''}
              onSave={() => saveField('default_label_type')}
              onCancel={() => cancelField('default_label_type')}
              loading={loadingFields.has('default_label_type')}
            >
              <Select
                value={formData.default_label_type}
                onValueChange={(value) => updateField('default_label_type', value)}
              >
                <SelectTrigger className="h-8">
                  <SelectValue placeholder="Select a label type" />
                </SelectTrigger>
                <SelectContent>
                  {LABEL_TYPE_OPTIONS.map((type) => (
                    <SelectItem key={type} value={type}>
                      {type}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </WorkspaceConfigField>

            <WorkspaceConfigField
              label="Default Weight Unit"
              description="Unit of measurement for package weights"
              value={formData.default_weight_unit}
              originalValue={workspace_config?.default_weight_unit || ''}
              onSave={() => saveField('default_weight_unit')}
              onCancel={() => cancelField('default_weight_unit')}
              loading={loadingFields.has('default_weight_unit')}
            >
              <Select
                value={formData.default_weight_unit}
                onValueChange={(value) => updateField('default_weight_unit', value)}
              >
                <SelectTrigger className="h-8">
                  <SelectValue placeholder="Select weight unit" />
                </SelectTrigger>
                <SelectContent>
                  {WEIGHT_UNIT_OPTIONS.map((unit) => (
                    <SelectItem key={unit} value={unit}>
                      {unit}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </WorkspaceConfigField>

            <WorkspaceConfigField
              label="Default Dimension Unit"
              description="Unit of measurement for package dimensions"
              value={formData.default_dimension_unit}
              originalValue={workspace_config?.default_dimension_unit || ''}
              onSave={() => saveField('default_dimension_unit')}
              onCancel={() => cancelField('default_dimension_unit')}
              loading={loadingFields.has('default_dimension_unit')}
            >
              <Select
                value={formData.default_dimension_unit}
                onValueChange={(value) => updateField('default_dimension_unit', value)}
              >
                <SelectTrigger className="h-8">
                  <SelectValue placeholder="Select dimension unit" />
                </SelectTrigger>
                <SelectContent>
                  {DIMENSION_UNIT_OPTIONS.map((unit) => (
                    <SelectItem key={unit} value={unit}>
                      {unit}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </WorkspaceConfigField>
          </div>
        </CardContent>
      </Card>

      {/* Tax Identifiers */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            Shipping Tax Identifiers
          </CardTitle>
          <CardDescription>
            Set up tax identifiers for your account.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="max-w-md space-y-6">
            <WorkspaceConfigField
              label="State Tax ID"
              value={formData.state_tax_id}
              originalValue={workspace_config?.state_tax_id || ''}
              onSave={() => saveField('state_tax_id')}
              onCancel={() => cancelField('state_tax_id')}
              loading={loadingFields.has('state_tax_id')}
            >
              <Input
                className="h-8"
                value={formData.state_tax_id}
                onChange={(e) => updateField('state_tax_id', e.target.value)}
                placeholder="Enter state tax ID"
              />
            </WorkspaceConfigField>

            <WorkspaceConfigField
              label="Federal Tax ID"
              value={formData.federal_tax_id}
              originalValue={workspace_config?.federal_tax_id || ''}
              onSave={() => saveField('federal_tax_id')}
              onCancel={() => cancelField('federal_tax_id')}
              loading={loadingFields.has('federal_tax_id')}
            >
              <Input
                className="h-8"
                value={formData.federal_tax_id}
                onChange={(e) => updateField('federal_tax_id', e.target.value)}
                placeholder="Enter federal tax ID"
              />
            </WorkspaceConfigField>
          </div>
        </CardContent>
      </Card>

      {/* Shipping Options */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Package className="h-5 w-5" />
            Shipping Options
          </CardTitle>
          <CardDescription>
            Configure default shipping preferences.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="max-w-md">
            <WorkspaceConfigField
              label="Insure Shipments by Default"
              description="Automatically add insurance to all shipments"
              value={formData.insured_by_default}
              originalValue={workspace_config?.insured_by_default || false}
              onSave={() => saveField('insured_by_default')}
              onCancel={() => cancelField('insured_by_default')}
              loading={loadingFields.has('insured_by_default')}
            >
              <div className="flex items-center space-x-2">
                <Switch
                  checked={formData.insured_by_default}
                  onCheckedChange={(checked) => updateField('insured_by_default', checked)}
                />
                <span className="text-sm text-muted-foreground">
                  {formData.insured_by_default ? 'Enabled' : 'Disabled'}
                </span>
              </div>
            </WorkspaceConfigField>
          </div>
        </CardContent>
      </Card>

      {/* Customs Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Globe className="h-5 w-5" />
            Customs Settings
          </CardTitle>
          <CardDescription>
            Configure customs and international shipping settings.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="max-w-md space-y-6">
            <WorkspaceConfigField
              label="AES"
              value={formData.customs_aes}
              originalValue={workspace_config?.customs_aes || ''}
              onSave={() => saveField('customs_aes')}
              onCancel={() => cancelField('customs_aes')}
              loading={loadingFields.has('customs_aes')}
            >
              <Input
                className="h-8"
                value={formData.customs_aes}
                onChange={(e) => updateField('customs_aes', e.target.value)}
                placeholder="Enter AES"
              />
            </WorkspaceConfigField>

            <WorkspaceConfigField
              label="EEL PFC"
              value={formData.customs_eel_pfc}
              originalValue={workspace_config?.customs_eel_pfc || ''}
              onSave={() => saveField('customs_eel_pfc')}
              onCancel={() => cancelField('customs_eel_pfc')}
              loading={loadingFields.has('customs_eel_pfc')}
            >
              <Input
                className="h-8"
                value={formData.customs_eel_pfc}
                onChange={(e) => updateField('customs_eel_pfc', e.target.value)}
                placeholder="Enter EEL PFC"
              />
            </WorkspaceConfigField>

            <WorkspaceConfigField
              label="License Number"
              value={formData.customs_license_number}
              originalValue={workspace_config?.customs_license_number || ''}
              onSave={() => saveField('customs_license_number')}
              onCancel={() => cancelField('customs_license_number')}
              loading={loadingFields.has('customs_license_number')}
            >
              <Input
                className="h-8"
                value={formData.customs_license_number}
                onChange={(e) => updateField('customs_license_number', e.target.value)}
                placeholder="Enter license number"
              />
            </WorkspaceConfigField>

            <WorkspaceConfigField
              label="Certificate Number"
              value={formData.customs_certificate_number}
              originalValue={workspace_config?.customs_certificate_number || ''}
              onSave={() => saveField('customs_certificate_number')}
              onCancel={() => cancelField('customs_certificate_number')}
              loading={loadingFields.has('customs_certificate_number')}
            >
              <Input
                className="h-8"
                value={formData.customs_certificate_number}
                onChange={(e) => updateField('customs_certificate_number', e.target.value)}
                placeholder="Enter certificate number"
              />
            </WorkspaceConfigField>

            <WorkspaceConfigField
              label="NIP Number"
              value={formData.customs_nip_number}
              originalValue={workspace_config?.customs_nip_number || ''}
              onSave={() => saveField('customs_nip_number')}
              onCancel={() => cancelField('customs_nip_number')}
              loading={loadingFields.has('customs_nip_number')}
            >
              <Input
                className="h-8"
                value={formData.customs_nip_number}
                onChange={(e) => updateField('customs_nip_number', e.target.value)}
                placeholder="Enter NIP number"
              />
            </WorkspaceConfigField>

            <WorkspaceConfigField
              label="EORI Number"
              value={formData.customs_eori_number}
              originalValue={workspace_config?.customs_eori_number || ''}
              onSave={() => saveField('customs_eori_number')}
              onCancel={() => cancelField('customs_eori_number')}
              loading={loadingFields.has('customs_eori_number')}
            >
              <Input
                className="h-8"
                value={formData.customs_eori_number}
                onChange={(e) => updateField('customs_eori_number', e.target.value)}
                placeholder="Enter EORI number"
              />
            </WorkspaceConfigField>

            <WorkspaceConfigField
              label="VAT Registration Number"
              value={formData.customs_vat_registration_number}
              originalValue={workspace_config?.customs_vat_registration_number || ''}
              onSave={() => saveField('customs_vat_registration_number')}
              onCancel={() => cancelField('customs_vat_registration_number')}
              loading={loadingFields.has('customs_vat_registration_number')}
            >
              <Input
                className="h-8"
                value={formData.customs_vat_registration_number}
                onChange={(e) => updateField('customs_vat_registration_number', e.target.value)}
                placeholder="Enter VAT registration number"
              />
            </WorkspaceConfigField>
          </div>
        </CardContent>
      </Card>

      {/* Close Account */}
      <Card className="border-destructive">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-destructive">
            <AlertTriangle className="h-5 w-5" />
            Close Account
          </CardTitle>
          <CardDescription>
            Permanently delete your account and all associated data.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="max-w-md">
            <Button
              variant="destructive"
              onClick={() => setIsCloseAccountOpen(true)}
              size="sm"
            >
              Close Account
            </Button>
          </div>
        </CardContent>
      </Card>

      <CloseAccountDialog
        open={isCloseAccountOpen}
        onOpenChange={setIsCloseAccountOpen}
      />
    </div>
  );
}
