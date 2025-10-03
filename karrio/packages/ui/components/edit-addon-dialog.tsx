"use client";

import React, { useEffect } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "./ui/dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Checkbox } from "./ui/checkbox";
import { StatusBadge } from "./status-badge";
import { Switch } from "./ui/switch";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { useAddonForm, AddonType } from "@karrio/hooks/admin-addons";
import { CreateAddonMutationInput, SurchargeTypeEnum } from "@karrio/types/graphql/admin";

interface EditAddonDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  addon: AddonType | null;
  onSubmit: (data: CreateAddonMutationInput & { id: string }) => Promise<void>;
}

export function EditAddonDialog({ open, onOpenChange, addon, onSubmit }: EditAddonDialogProps) {
  const { toast } = useToast();
  const {
    formData,
    setFormData,
    updateFormData,
    handleCarrierChange,
    handleServiceChange,
    toMutationInput,
    organizations,
    systemConnections,
    availableCarriers,
    availableServices,
  } = useAddonForm(addon || undefined);

  // Update form data when addon changes
  useEffect(() => {
    if (addon) {
      setFormData({
        name: addon.name,
        amount: addon.amount.toString(),
        surcharge_type: addon.surcharge_type as SurchargeTypeEnum,
        active: addon.active,
        carriers: addon.carriers || [],
        services: addon.services || [],
        carrier_accounts: addon.carrier_accounts?.map(acc => acc.id) || [],
        organizations: [] // Not available in current GraphQL schema
      });
    }
  }, [addon, setFormData]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!addon) return;
    
    try {
      const addonData = {
        id: addon.id,
        ...toMutationInput()
      };

      await onSubmit(addonData);
      onOpenChange(false);
    } catch (error) {
      toast({ 
        title: "Failed to update addon", 
        description: error instanceof Error ? error.message : "Unknown error",
        variant: "destructive" 
      });
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[700px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Edit Addon</DialogTitle>
          <DialogDescription>
            Update the shipping addon configuration and targeting.
          </DialogDescription>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <Tabs defaultValue="basic" className="w-full">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="basic">Basic Info</TabsTrigger>
              <TabsTrigger value="carriers">Carriers</TabsTrigger>
              <TabsTrigger value="accounts">Accounts</TabsTrigger>
              <TabsTrigger value="organizations">Organizations</TabsTrigger>
            </TabsList>
            
            <TabsContent value="basic" className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="edit-name">Addon Name *</Label>
                <Input
                  id="edit-name"
                  value={formData.name}
                  onChange={(e) => updateFormData({ name: e.target.value })}
                  placeholder="e.g., Insurance Fee, Handling Charge"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="edit-amount">Amount *</Label>
                  <Input
                    id="edit-amount"
                    type="number"
                    step="0.01"
                    value={formData.amount}
                    onChange={(e) => updateFormData({ amount: e.target.value })}
                    placeholder="0.00"
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="edit-surcharge_type">Type</Label>
                  <Select 
                    value={formData.surcharge_type} 
                    onValueChange={(value) => updateFormData({ surcharge_type: value as SurchargeTypeEnum })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value={SurchargeTypeEnum.AMOUNT}>Fixed Amount ($)</SelectItem>
                      <SelectItem value={SurchargeTypeEnum.PERCENTAGE}>Percentage (%)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <Switch 
                  id="edit-active" 
                  checked={formData.active}
                  onCheckedChange={(checked) => updateFormData({ active: checked })}
                />
                <Label htmlFor="edit-active">Active</Label>
              </div>
            </TabsContent>
            
            <TabsContent value="carriers" className="space-y-4">
              <div>
                <Label className="text-sm font-medium">Carriers</Label>
                <p className="text-sm text-muted-foreground">Select specific carriers to apply this addon to. Leave empty to apply to all carriers.</p>
              </div>
              
              <div className="grid grid-cols-2 gap-4 max-h-60 overflow-y-auto">
                {availableCarriers.map((carrier) => (
                  <div key={carrier} className="flex items-center space-x-2">
                    <Checkbox
                      id={`edit-carrier-${carrier}`}
                      checked={formData.carriers.includes(carrier)}
                      onCheckedChange={(checked) => handleCarrierChange(carrier, checked as boolean)}
                    />
                    <Label htmlFor={`edit-carrier-${carrier}`} className="text-sm font-normal capitalize">
                      {carrier.replace(/_/g, ' ')}
                    </Label>
                  </div>
                ))}
              </div>

              {formData.carriers.length > 0 && (
                <>
                  <div>
                    <Label className="text-sm font-medium">Services</Label>
                    <p className="text-sm text-muted-foreground">Select specific services for the selected carriers.</p>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4 max-h-60 overflow-y-auto">
                    {availableServices.map((service) => (
                      <div key={service} className="flex items-center space-x-2">
                        <Checkbox
                          id={`edit-service-${service}`}
                          checked={formData.services.includes(service)}
                          onCheckedChange={(checked) => handleServiceChange(service, checked as boolean)}
                        />
                        <Label htmlFor={`edit-service-${service}`} className="text-sm font-normal capitalize">
                          {service.replace(/_/g, ' ')}
                        </Label>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </TabsContent>
            
            <TabsContent value="accounts" className="space-y-4">
              <div>
                <Label className="text-sm font-medium">Carrier Accounts</Label>
                <p className="text-sm text-muted-foreground">Select specific carrier account connections to apply this addon to.</p>
              </div>
              
              <div className="space-y-2 max-h-60 overflow-y-auto">
                {systemConnections.map(({ node: connection }) => (
                  <div key={connection.id} className="flex items-center space-x-2 p-2 border rounded">
                    <Checkbox
                      id={`edit-account-${connection.id}`}
                      checked={formData.carrier_accounts.includes(connection.id)}
                      onCheckedChange={(checked) => {
                        updateFormData({
                          carrier_accounts: checked 
                            ? [...formData.carrier_accounts, connection.id]
                            : formData.carrier_accounts.filter(id => id !== connection.id)
                        });
                      }}
                    />
                    <div className="flex-1">
                      <Label htmlFor={`edit-account-${connection.id}`} className="text-sm font-medium">
                        {connection.display_name || connection.carrier_name}
                      </Label>
                      <p className="text-xs text-muted-foreground">{connection.carrier_id}</p>
                    </div>
                    <StatusBadge status={connection.active ? "active" : "inactive"} />
                  </div>
                ))}
              </div>
            </TabsContent>
            
            <TabsContent value="organizations" className="space-y-4">
              <div>
                <Label className="text-sm font-medium">Organizations</Label>
                <p className="text-sm text-muted-foreground">Select specific organizations to apply this addon to. Leave empty to apply to all organizations.</p>
              </div>
              
              <div className="space-y-2 max-h-60 overflow-y-auto">
                {organizations.map(({ node: org }) => (
                  <div key={org.id} className="flex items-center space-x-2 p-2 border rounded">
                    <Checkbox
                      id={`edit-org-${org.id}`}
                      checked={formData.organizations.includes(org.id)}
                      onCheckedChange={(checked) => {
                        updateFormData({
                          organizations: checked 
                            ? [...formData.organizations, org.id]
                            : formData.organizations.filter(id => id !== org.id)
                        });
                      }}
                    />
                    <div className="flex-1">
                      <Label htmlFor={`edit-org-${org.id}`} className="text-sm font-medium">
                        {org.name}
                      </Label>
                      <p className="text-xs text-muted-foreground">{org.slug}</p>
                    </div>
                    <StatusBadge status={org.is_active ? "active" : "inactive"} />
                  </div>
                ))}
              </div>
            </TabsContent>
          </Tabs>

          <div className="flex justify-end space-x-2 pt-4 border-t">
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button type="submit">
              Update Addon
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}