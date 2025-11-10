"use client";

import React, { useState, useMemo } from 'react';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@karrio/ui/components/ui/dropdown-menu";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@karrio/ui/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@karrio/ui/components/ui/table";
import { Plus, Search, MoreHorizontal, Edit3, Trash2, DollarSign, Percent, Zap, AlertCircle } from 'lucide-react';
import { LineChart, Line, CartesianGrid, XAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { useAddons, useAddonMutation, useAddonForm, AddonType } from "@karrio/hooks/admin-addons";
import { SurchargeTypeEnum } from "@karrio/types/graphql/admin";
import { Card, CardContent } from "@karrio/ui/components/ui/card";
import { StatusBadge } from "@karrio/ui/components/status-badge";
import { Button } from "@karrio/ui/components/ui/button";
import { Label } from "@karrio/ui/components/ui/label";
import { Input } from "@karrio/ui/components/ui/input";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { useAdminSystemUsage } from "@karrio/hooks/admin-usage";
import { Checkbox } from "@karrio/ui/components/ui/checkbox";
import { Switch } from "@karrio/ui/components/ui/switch";
import { Alert, AlertDescription } from "@karrio/ui/components/ui/alert";
import { SelectField } from "@karrio/ui/core/components";
import { cn } from "@karrio/ui/lib/utils";
import { useSystemConnections } from "@karrio/hooks/admin-system-connections";
import { CarrierImage } from "@karrio/ui/core/components/carrier-image";
import moment from "moment";

interface CreateAddonDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSubmit: (data: any) => Promise<void>;
}

function CreateAddonDialog({ open, onOpenChange, onSubmit }: CreateAddonDialogProps) {
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const {
    formData,
    updateFormData,
    handleCarrierChange,
    handleServiceChange,
    resetForm,
    toMutationInput,
    availableCarriers,
    availableServices,
  } = useAddonForm();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.name || !formData.amount) {
      toast({
        title: "Validation Error",
        description: "Please fill in all required fields",
        variant: "destructive",
      });
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(toMutationInput());
      resetForm();
      onOpenChange(false);
    } catch (error: any) {
      toast({
        title: "Error creating addon",
        description: error.message || "An error occurred",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[700px] max-h-[90vh] p-0 flex flex-col">
        {/* Sticky Header */}
        <DialogHeader className="px-4 py-3 border-b sticky top-0 bg-background z-10">
          <DialogTitle>Create New Addon</DialogTitle>
          <DialogDescription>
            Configure a new addon that will be available across all organizations
          </DialogDescription>
        </DialogHeader>

        {/* Scrollable Body */}
        <div className="flex-1 overflow-y-auto px-4 py-3">
          <form id="create-addon-form" onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="sm:col-span-2">
                <Label htmlFor="name">Addon Name *</Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => updateFormData({ name: e.target.value })}
                  placeholder="e.g., Fuel Surcharge, Handling Fee"
                  required
                />
              </div>

              <div>
                <Label htmlFor="surcharge_type">Charge Type *</Label>
                <Select
                  value={formData.surcharge_type}
                  onValueChange={(value) => updateFormData({ surcharge_type: value as SurchargeTypeEnum })}
                >
                  <SelectTrigger id="surcharge_type">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value={SurchargeTypeEnum.AMOUNT}>Fixed Amount ($)</SelectItem>
                    <SelectItem value={SurchargeTypeEnum.PERCENTAGE}>Percentage (%)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="amount">
                  Amount * {formData.surcharge_type === SurchargeTypeEnum.PERCENTAGE ? '(%)' : '($)'}
                </Label>
                <Input
                  id="amount"
                  type="number"
                  step="0.01"
                  value={formData.amount}
                  onChange={(e) => updateFormData({ amount: e.target.value })}
                  placeholder={formData.surcharge_type === SurchargeTypeEnum.PERCENTAGE ? "5.00" : "10.00"}
                  required
                />
              </div>
            </div>

            <div className="flex items-center justify-between">
              <Label htmlFor="active">Active Status</Label>
              <Switch
                id="active"
                checked={formData.active}
                onCheckedChange={(checked) => updateFormData({ active: checked })}
              />
            </div>

            <div>
              <Label>Carriers (leave empty for all carriers)</Label>
              <div className="grid grid-cols-3 gap-3 mt-2 max-h-40 overflow-y-auto border rounded-md p-3">
                {availableCarriers.map((carrier) => (
                  <div key={carrier} className="flex items-center space-x-2">
                    <Checkbox
                      id={`carrier-${carrier}`}
                      checked={formData.carriers.includes(carrier)}
                      onCheckedChange={(checked) => handleCarrierChange(carrier, !!checked)}
                    />
                    <Label
                      htmlFor={`carrier-${carrier}`}
                      className="text-sm font-normal cursor-pointer"
                    >
                      {carrier.toUpperCase()}
                    </Label>
                  </div>
                ))}
              </div>
            </div>

            {formData.carriers.length > 0 && availableServices.length > 0 && (
              <div>
                <Label>Services (leave empty for all services)</Label>
                <div className="grid grid-cols-2 gap-3 mt-2 max-h-40 overflow-y-auto border rounded-md p-3">
                  {availableServices.map((service) => (
                    <div key={service} className="flex items-center space-x-2">
                      <Checkbox
                        id={`service-${service}`}
                        checked={formData.services.includes(service)}
                        onCheckedChange={(checked) => handleServiceChange(service, !!checked)}
                      />
                      <Label
                        htmlFor={`service-${service}`}
                        className="text-sm font-normal cursor-pointer"
                      >
                        {service.replace(/_/g, ' ')}
                      </Label>
                    </div>
                  ))}
                </div>
              </div>
            )}

          </form>
        </div>

        {/* Sticky Footer */}
        <DialogFooter className="px-4 py-3 border-t sticky bottom-0 bg-background">
          <Button
            type="button"
            variant="outline"
            onClick={() => {
              resetForm();
              onOpenChange(false);
            }}
          >
            Cancel
          </Button>
          <Button type="submit" form="create-addon-form" disabled={isSubmitting}>
            {isSubmitting ? "Creating..." : "Create Addon"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

interface EditAddonDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  addon: AddonType | null;
  onSubmit: (data: any) => Promise<void>;
}

function EditAddonDialog({ open, onOpenChange, addon, onSubmit }: EditAddonDialogProps) {
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const {
    formData,
    updateFormData,
    handleCarrierChange,
    handleServiceChange,
    toMutationInput,
    availableCarriers,
    availableServices,
  } = useAddonForm(addon || undefined);

  // Ensure form is populated when an addon is provided/changed
  React.useEffect(() => {
    if (addon) {
      updateFormData({
        name: addon.name || "",
        amount: (addon.amount as any)?.toString?.() ?? "",
        active: !!addon.active,
        surcharge_type: addon.surcharge_type as SurchargeTypeEnum,
        carriers: Array.isArray(addon.carriers) ? addon.carriers : [],
        services: Array.isArray(addon.services) ? addon.services : [],
      } as any);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [addon?.id]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.name || !formData.amount) {
      toast({
        title: "Validation Error",
        description: "Please fill in all required fields",
        variant: "destructive",
      });
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit({ ...toMutationInput(), id: addon?.id });
      onOpenChange(false);
    } catch (error: any) {
      toast({
        title: "Error updating addon",
        description: error.message || "An error occurred",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[700px] max-h-[90vh] p-0 flex flex-col">
        {/* Sticky Header */}
        <DialogHeader className="px-4 py-3 border-b sticky top-0 bg-background z-10">
          <DialogTitle>Edit Addon</DialogTitle>
          <DialogDescription>
            Update addon configuration and settings
          </DialogDescription>
        </DialogHeader>

        {/* Scrollable Body */}
        <div className="flex-1 overflow-y-auto px-4 py-3">
          <form id="edit-addon-form" onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div className="col-span-2">
                <Label htmlFor="edit-name">Addon Name *</Label>
                <Input
                  id="edit-name"
                  value={formData.name}
                  onChange={(e) => updateFormData({ name: e.target.value })}
                  placeholder="e.g., Fuel Surcharge, Handling Fee"
                  required
                />
              </div>

              <div>
                <Label htmlFor="edit-surcharge_type">Charge Type *</Label>
                <Select
                  value={formData.surcharge_type}
                  onValueChange={(value) => updateFormData({ surcharge_type: value as SurchargeTypeEnum })}
                >
                  <SelectTrigger id="edit-surcharge_type">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value={SurchargeTypeEnum.AMOUNT}>Fixed Amount ($)</SelectItem>
                    <SelectItem value={SurchargeTypeEnum.PERCENTAGE}>Percentage (%)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="edit-amount">
                  Amount * {formData.surcharge_type === SurchargeTypeEnum.PERCENTAGE ? '(%)' : '($)'}
                </Label>
                <Input
                  id="edit-amount"
                  type="number"
                  step="0.01"
                  value={formData.amount}
                  onChange={(e) => updateFormData({ amount: e.target.value })}
                  placeholder={formData.surcharge_type === SurchargeTypeEnum.PERCENTAGE ? "5.00" : "10.00"}
                  required
                />
              </div>
            </div>

            <div className="flex items-center justify-between">
              <Label htmlFor="edit-active">Active Status</Label>
              <Switch
                id="edit-active"
                checked={formData.active}
                onCheckedChange={(checked) => updateFormData({ active: checked })}
              />
            </div>

            <div>
              <Label>Carriers (leave empty for all carriers)</Label>
              <div className="grid grid-cols-3 gap-3 mt-2 max-h-40 overflow-y-auto border rounded-md p-3">
                {availableCarriers.map((carrier) => (
                  <div key={carrier} className="flex items-center space-x-2">
                    <Checkbox
                      id={`edit-carrier-${carrier}`}
                      checked={formData.carriers.includes(carrier)}
                      onCheckedChange={(checked) => handleCarrierChange(carrier, !!checked)}
                    />
                    <Label
                      htmlFor={`edit-carrier-${carrier}`}
                      className="text-sm font-normal cursor-pointer"
                    >
                      {carrier.toUpperCase()}
                    </Label>
                  </div>
                ))}
              </div>
            </div>

            {formData.carriers.length > 0 && availableServices.length > 0 && (
              <div>
                <Label>Services (leave empty for all services)</Label>
                <div className="grid grid-cols-2 gap-3 mt-2 max-h-40 overflow-y-auto border rounded-md p-3">
                  {availableServices.map((service) => (
                    <div key={service} className="flex items-center space-x-2">
                      <Checkbox
                        id={`edit-service-${service}`}
                        checked={formData.services.includes(service)}
                        onCheckedChange={(checked) => handleServiceChange(service, !!checked)}
                      />
                      <Label
                        htmlFor={`edit-service-${service}`}
                        className="text-sm font-normal cursor-pointer"
                      >
                        {service.replace(/_/g, ' ')}
                      </Label>
                    </div>
                  ))}
                </div>
              </div>
            )}

          </form>
        </div>

        {/* Sticky Footer */}
        <DialogFooter className="px-4 py-3 border-t sticky bottom-0 bg-background">
          <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button type="submit" form="edit-addon-form" disabled={isSubmitting}>
            {isSubmitting ? "Saving..." : "Save Changes"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

interface DeleteConfirmationDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  addon: AddonType | null;
  onConfirm: () => Promise<void>;
}

function DeleteConfirmationDialog({ open, onOpenChange, addon, onConfirm }: DeleteConfirmationDialogProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const { toast } = useToast();

  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await onConfirm();
      onOpenChange(false);
      toast({ title: "Addon deleted successfully" });
    } catch (error: any) {
      toast({
        title: "Error deleting addon",
        description: error.message || "An error occurred",
        variant: "destructive",
      });
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Delete Addon</DialogTitle>
          <DialogDescription>
            Are you sure you want to delete this addon? This action cannot be undone.
          </DialogDescription>
        </DialogHeader>

        {addon && (
          <div className="space-y-4">
            <Alert>
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                You are about to delete <strong>{addon.name}</strong>.
                This will remove the addon from all organizations and cannot be reversed.
              </AlertDescription>
            </Alert>

            <div className="bg-gray-50 rounded-lg p-4 space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Name:</span>
                <span className="text-sm font-medium">{addon.name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Amount:</span>
                <span className="text-sm font-medium">
                  {addon.surcharge_type === SurchargeTypeEnum.PERCENTAGE ? `${addon.amount}%` : `$${addon.amount}`}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Status:</span>
                <StatusBadge status={addon.active ? "active" : "inactive"} />
              </div>
            </div>
          </div>
        )}

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button
            variant="destructive"
            onClick={handleDelete}
            disabled={isDeleting}
          >
            {isDeleting ? "Deleting..." : "Delete Addon"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default function AddonsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [selectedAddon, setSelectedAddon] = useState<AddonType | null>(null);
  const [isEditOpen, setIsEditOpen] = useState(false);
  // Removed view dialog per spec
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [selectedTab, setSelectedTab] = useState<'overview' | 'addons'>("overview");

  const { toast } = useToast();

  // Fetch data with usage and shipment filters
  const {
    query: { data: { usage } = {} },
    setFilter,
    filter,
    USAGE_FILTERS,
    DAYS_LIST,
    currentFilter,
  } = useAdminSystemUsage();

  // Create filters for addon queries
  const usageFilter = filter;

  const { query: addonsQuery, addons } = useAddons({}, usageFilter);
  const isLoading = addonsQuery.isLoading;

  // Mutations
  const { createAddon, updateAddon, deleteAddon } = useAddonMutation();

  const handleCreateAddon = async (data: any) => {
    await createAddon.mutateAsync(data);
    toast({ title: "Addon created successfully" });
    setIsCreateOpen(false);
  };

  const handleEditAddon = async (data: any) => {
    await updateAddon.mutateAsync(data);
    toast({ title: "Addon updated successfully" });
    setIsEditOpen(false);
    setSelectedAddon(null);
  };

  const handleDeleteAddon = async () => {
    if (!selectedAddon) return;
    await deleteAddon.mutateAsync({ id: selectedAddon.id });
    setSelectedAddon(null);
  };

  // Convert addons data to proper format
  const addonsList: AddonType[] = useMemo(() => {
    if (!addons?.edges) return [];
    return addons.edges.map(({ node }) => node);
  }, [addons]);

  const filteredAddons = addonsList.filter(addon => {
    const matchesSearch = addon.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      addon.id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' ||
      (statusFilter === 'active' && addon.active) ||
      (statusFilter === 'inactive' && !addon.active);

    return matchesSearch && matchesStatus;
  });

  // Calculate real statistics from API
  const stats = useMemo(() => {
    const totalAddons = addonsList.length;
    const activeAddons = addonsList.filter(addon => addon.active).length;
    const totalAddonsCharges = usage?.total_addons_charges || 0;

    return {
      totalAddons,
      activeAddons,
      totalAddonsCharges,
    };
  }, [addonsList, usage]);

  // Generate chart data for addons charges over time using real timeline data
  const chartData = DAYS_LIST[currentFilter() || "15 days"].map((day) => ({
    name: day,
    charges: usage?.addons_charges?.find(({ date }) => moment(date).format("MMM D") === day)?.amount || 0,
  }));

  // System connections for overview page
  const { query: sysConnQuery } = useSystemConnections({}, usageFilter);
  const systemConnections = useMemo(() => (sysConnQuery.data?.system_carrier_connections?.edges || []).map(({ node }: any) => node), [sysConnQuery.data?.system_carrier_connections?.edges]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading addons...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Addons</h1>
          <p className="text-sm text-gray-600 mt-1">
            ${stats.totalAddonsCharges.toLocaleString()}
          </p>
        </div>
      </div>

      {/* Tab Navigation with Period Filter */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between border-b border-gray-200 gap-4">
        <nav className="flex space-x-8 overflow-x-auto">
          <button
            className={cn(
              "whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors",
              selectedTab === "overview"
                ? "border-purple-500 text-purple-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            )}
            onClick={() => setSelectedTab("overview")}
          >
            Overview
          </button>
          <button
            className={cn(
              "whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium transition-colors",
              selectedTab === "addons"
                ? "border-purple-500 text-purple-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            )}
            onClick={() => setSelectedTab("addons")}
          >
            Addons
          </button>
        </nav>

        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 py-4">
          <SelectField
            className="is-small"
            value={JSON.stringify(filter)}
            onChange={(e) => setFilter(JSON.parse(e.target.value))}
            style={{ minWidth: "140px" }}
          >
            {Object.entries(USAGE_FILTERS).map(([key, value]) => (
              <option key={key} value={JSON.stringify(value)}>
                {key}
              </option>
            ))}
          </SelectField>
          {selectedTab === 'addons' && (
            <Button onClick={() => setIsCreateOpen(true)}>
              <Plus className="mr-2 h-4 w-4" />
              Create Addon
            </Button>
          )}
        </div>
      </div>

      {/* Overview Tab */}
      {selectedTab === 'overview' && (
        <div className="space-y-6">
          {/* Summary Stats */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <Card className="border shadow-none">
              <CardContent className="p-4">
                <p className="text-sm text-gray-600">Active Addons</p>
                <p className="text-2xl font-semibold text-gray-900">{stats.activeAddons} / {stats.totalAddons}</p>
              </CardContent>
            </Card>
            <Card className="border shadow-none">
              <CardContent className="p-4">
                <p className="text-sm text-gray-600">Total Charges</p>
                <p className="text-2xl font-semibold text-gray-900">${stats.totalAddonsCharges.toLocaleString()}</p>
              </CardContent>
            </Card>
            <Card className="border shadow-none">
              <CardContent className="p-4">
                <p className="text-sm text-gray-600">System Accounts</p>
                <p className="text-2xl font-semibold text-gray-900">{sysConnQuery.data?.system_carrier_connections?.page_info?.count || 0}</p>
              </CardContent>
            </Card>
          </div>

          {/* Chart */}
          <div>
            <div className="flex items-center gap-4 mb-4">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-blue-500"></div>
                <span className="text-sm font-medium">${stats.totalAddonsCharges.toLocaleString()} total addon charges</span>
              </div>
            </div>
            <div style={{ width: "100%", height: "300px" }}>
              {usage?.total_addons_charges ? (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                    <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} />
                    <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '6px', color: 'white', fontSize: '12px' }} formatter={(value: any) => [`$${value.toLocaleString()}`, 'Charges']} />
                    <Line type="linear" dataKey="charges" stroke="#3b82f6" strokeWidth={2} dot={false} name="charges" />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-full bg-gray-50 rounded">
                  <div className="text-center">
                    <Zap className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                    <p className="text-sm text-gray-500">No addon charges data available</p>
                  </div>
                </div>
              )}
            </div>
            <div className="text-right mt-2">
              <span className="text-xs text-gray-500">Updated today {new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })}</span>
            </div>
          </div>

          {/* System Connections List */}
          <div className="space-y-3">
            <h3 className="text-lg font-medium text-gray-900">System Connections</h3>
            {(systemConnections || []).length === 0 ? (
              <div className="text-sm text-gray-500">No system connections</div>
            ) : (
              <div className="space-y-3">
                {systemConnections.map((connection: any) => (
                  <div key={connection.id} className="group relative flex flex-col sm:flex-row items-start sm:items-center justify-between p-4 rounded-lg border border-gray-200 bg-white gap-3">
                    <div className="flex items-start sm:items-center gap-3 flex-1 w-full sm:w-auto">
                      <div className="flex-shrink-0">
                        <CarrierImage
                          carrier_name={connection.credentials?.custom_carrier_name || connection.carrier_name}
                          width={48} height={48}
                          className="rounded-lg"
                          text_color={connection.config?.text_color}
                          background={connection.config?.brand_color}
                        />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex flex-col sm:flex-row sm:items-center gap-2 mb-1">
                          <div className="font-medium text-gray-900 text-base">{connection.display_name || connection.carrier_name}</div>
                          <div className="flex items-center gap-2">
                            <StatusBadge status={connection.active ? "active" : "inactive"} />
                            {connection.test_mode && <StatusBadge status="test" />}
                          </div>
                        </div>
                        <div className="text-sm text-gray-600 font-mono">{connection.carrier_id || connection.id}</div>
                      </div>
                    </div>
                    {/* Usage stats */}
                    <div className="grid grid-cols-3 gap-4 sm:gap-6 text-center sm:text-right w-full sm:w-auto">
                      <div>
                        <div className="text-xs text-gray-500">Shipments</div>
                        <div className="text-sm font-medium text-gray-900">{(connection.usage?.total_shipments || 0).toLocaleString()}</div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-500">Shipping Spend</div>
                        <div className="text-sm font-medium text-gray-900">${(connection.usage?.total_shipping_spend || 0).toLocaleString()}</div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-500">Addons</div>
                        <div className="text-sm font-medium text-gray-900">${(connection.usage?.total_addons_charges || 0).toLocaleString()}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Addons Tab */}
      {selectedTab === 'addons' && (
        <div className="space-y-6">
          {/* Addons Management Table */}
          <div>
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
              <h2 className="text-lg font-medium text-gray-900">Addon management</h2>
              <div className="flex flex-col sm:flex-row gap-2">
                <div className="flex h-9 w-full sm:w-[200px] items-center rounded-md border border-input bg-transparent shadow-sm">
                  <Search className="ml-3 h-4 w-4 text-muted-foreground flex-shrink-0" />
                  <input
                    placeholder="Search addons..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="flex-1 bg-transparent border-0 px-3 py-2 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-0"
                  />
                </div>
                <Select value={statusFilter} onValueChange={setStatusFilter}>
                  <SelectTrigger className="w-full sm:w-[140px]">
                    <SelectValue placeholder="Filter by status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Status</SelectItem>
                    <SelectItem value="active">Active</SelectItem>
                    <SelectItem value="inactive">Inactive</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="border-b">
              {filteredAddons.length === 0 ? (
                <div className="text-center py-12">
                  <Zap className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                  <h3 className="text-lg font-medium text-gray-500 mb-2">
                    No addons found
                  </h3>
                  <p className="text-sm text-gray-400">
                    {searchTerm || statusFilter !== 'all'
                      ? "No addons match your current filters."
                      : "Get started by creating your first addon."
                    }
                  </p>
                  {!searchTerm && statusFilter === 'all' && (
                    <Button className="mt-4" onClick={() => setIsCreateOpen(true)}>
                      <Plus className="mr-2 h-4 w-4" />
                      Create Your First Addon
                    </Button>
                  )}
                </div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Addon</TableHead>
                      <TableHead>Type & Amount</TableHead>
                      <TableHead>Coverage</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead className="text-right">Applied Count</TableHead>
                      <TableHead className="text-right">Total Charges</TableHead>
                      <TableHead className="w-12"></TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredAddons.map((addon) => (
                      <TableRow key={addon.id}>
                        <TableCell>
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                              {addon.surcharge_type === SurchargeTypeEnum.PERCENTAGE ? (
                                <Percent className="h-4 w-4 text-blue-600" />
                              ) : (
                                <DollarSign className="h-4 w-4 text-green-600" />
                              )}
                            </div>
                            <div>
                              <div className="font-medium text-gray-900">
                                {addon.name}
                              </div>
                              <div className="text-sm text-gray-500">
                                ID: {addon.id.slice(-8)}
                              </div>
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <span className="font-medium text-gray-900">
                            {addon.surcharge_type === SurchargeTypeEnum.PERCENTAGE ? `${addon.amount}%` : `$${addon.amount}`}
                          </span>
                        </TableCell>
                        <TableCell>
                          <div className="flex flex-wrap gap-1">
                            {addon.carriers && addon.carriers.length > 0 ? (
                              <>
                                {addon.carriers.slice(0, 2).map(carrier => (
                                  <span
                                    key={carrier}
                                    className="text-xs px-1.5 py-0.5 bg-gray-100 text-gray-700 rounded"
                                  >
                                    {carrier.toUpperCase()}
                                  </span>
                                ))}
                                {addon.carriers.length > 2 && (
                                  <span className="text-xs px-1.5 py-0.5 text-gray-600">
                                    +{addon.carriers.length - 2}
                                  </span>
                                )}
                              </>
                            ) : (
                              <span className="text-xs text-gray-500">All carriers</span>
                            )}
                          </div>
                        </TableCell>
                        <TableCell>
                          <StatusBadge status={addon.active ? "active" : "inactive"} />
                        </TableCell>
                        <TableCell className="text-right text-sm text-gray-600">
                          {/* Show total shipments using this addon across carrier accounts */}
                          {addon.usage?.total_shipments?.toLocaleString() || 0}
                        </TableCell>
                        <TableCell className="text-right font-medium text-gray-900">
                          {/* Show total addon charges across carrier accounts */}
                          ${addon.usage?.total_addons_charges?.toLocaleString() || 0}
                        </TableCell>
                        <TableCell>
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button variant="ghost" size="icon" className="h-8 w-8 p-0 hover:bg-muted">
                                <MoreHorizontal className="h-4 w-4" />
                                <span className="sr-only">Open menu</span>
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end">
                              <DropdownMenuLabel>Actions</DropdownMenuLabel>
                              {/* View action removed */}
                              <DropdownMenuItem onClick={() => {
                                setSelectedAddon(addon);
                                setIsEditOpen(true);
                              }}>
                                <Edit3 className="mr-2 h-4 w-4" />
                                Edit Addon
                              </DropdownMenuItem>
                              <DropdownMenuSeparator />
                              <DropdownMenuItem
                                className="text-red-600"
                                onClick={() => {
                                  setSelectedAddon(addon);
                                  setIsDeleteOpen(true);
                                }}
                              >
                                <Trash2 className="mr-2 h-4 w-4" />
                                Delete Addon
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Create Addon Dialog */}
      <CreateAddonDialog
        open={isCreateOpen}
        onOpenChange={setIsCreateOpen}
        onSubmit={handleCreateAddon}
      />

      {/* Edit Addon Dialog */}
      <EditAddonDialog
        open={isEditOpen}
        onOpenChange={setIsEditOpen}
        addon={selectedAddon}
        onSubmit={handleEditAddon}
      />

      {/* Delete Confirmation Dialog */}
      <DeleteConfirmationDialog
        open={isDeleteOpen}
        onOpenChange={setIsDeleteOpen}
        addon={selectedAddon}
        onConfirm={handleDeleteAddon}
      />

      {/* View Addon Dialog removed per spec */}
    </div>
  );
}
