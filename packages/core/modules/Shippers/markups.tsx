"use client";

import React, { useState, useMemo } from 'react';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@karrio/ui/components/ui/dropdown-menu";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@karrio/ui/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@karrio/ui/components/ui/table";
import { Plus, Search, MoreHorizontal, Edit3, Trash2, DollarSign, Percent, Zap, AlertCircle } from 'lucide-react';
import { LineChart, Line, CartesianGrid, XAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { useMarkups, useMarkupMutation, useMarkupForm, MarkupType } from "@karrio/hooks/admin-markups";
import { MarkupTypeEnum } from "@karrio/types/graphql/admin";
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

interface CreateMarkupDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSubmit: (data: any) => Promise<void>;
}

function CreateMarkupDialog({ open, onOpenChange, onSubmit }: CreateMarkupDialogProps) {
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const {
    formData,
    updateFormData,
    handleCarrierChange,
    handleServiceChange,
    handleConnectionChange,
    resetForm,
    toMutationInput,
    availableCarriers,
    availableServices,
    systemConnections,
  } = useMarkupForm();

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
        title: "Error creating markup",
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
        <DialogHeader className="px-4 py-3 border-b sticky top-0 bg-background z-10">
          <DialogTitle>Create New Markup</DialogTitle>
          <DialogDescription>
            Configure a new markup that will be applied to shipping rates
          </DialogDescription>
        </DialogHeader>

        <div className="flex-1 overflow-y-auto px-4 py-3">
          <form id="create-markup-form" onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="sm:col-span-2">
                <Label htmlFor="name">Markup Name *</Label>
                <Input
                  id="name"
                  value={formData.name}
                  onChange={(e) => updateFormData({ name: e.target.value })}
                  placeholder="e.g., Fuel Surcharge, Handling Fee"
                  required
                />
              </div>

              <div>
                <Label htmlFor="markup_type">Charge Type *</Label>
                <Select
                  value={formData.markup_type}
                  onValueChange={(value) => updateFormData({ markup_type: value as MarkupTypeEnum })}
                >
                  <SelectTrigger id="markup_type">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value={MarkupTypeEnum.AMOUNT}>Fixed Amount ($)</SelectItem>
                    <SelectItem value={MarkupTypeEnum.PERCENTAGE}>Percentage (%)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="amount">
                  Amount * {formData.markup_type === MarkupTypeEnum.PERCENTAGE ? '(%)' : '($)'}
                </Label>
                <Input
                  id="amount"
                  type="number"
                  step="0.01"
                  value={formData.amount}
                  onChange={(e) => updateFormData({ amount: e.target.value })}
                  placeholder={formData.markup_type === MarkupTypeEnum.PERCENTAGE ? "5.00" : "10.00"}
                  required
                />
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <Label htmlFor="active">Active Status</Label>
                <p className="text-xs text-muted-foreground">Enable to apply this markup to rates</p>
              </div>
              <Switch
                id="active"
                checked={formData.active}
                onCheckedChange={(checked) => updateFormData({ active: checked })}
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="space-y-1">
                <Label htmlFor="is_visible">Visible to Users</Label>
                <p className="text-xs text-muted-foreground">Show this markup in rate breakdowns</p>
              </div>
              <Switch
                id="is_visible"
                checked={formData.is_visible}
                onCheckedChange={(checked) => updateFormData({ is_visible: checked })}
              />
            </div>

            <div>
              <Label>Carriers (leave empty for all carriers)</Label>
              <div className="grid grid-cols-3 gap-3 mt-2 max-h-40 overflow-y-auto border rounded-md p-3">
                {availableCarriers.map((carrier) => (
                  <div key={carrier} className="flex items-center space-x-2">
                    <Checkbox
                      id={`carrier-${carrier}`}
                      checked={formData.carrier_codes.includes(carrier)}
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

            {formData.carrier_codes.length > 0 && availableServices.length > 0 && (
              <div>
                <Label>Services (leave empty for all services)</Label>
                <div className="grid grid-cols-2 gap-3 mt-2 max-h-40 overflow-y-auto border rounded-md p-3">
                  {availableServices.map((service) => (
                    <div key={service} className="flex items-center space-x-2">
                      <Checkbox
                        id={`service-${service}`}
                        checked={formData.service_codes.includes(service)}
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

            {systemConnections.length > 0 && (
              <div>
                <Label>Connections (leave empty for all connections)</Label>
                <div className="grid grid-cols-1 gap-2 mt-2 max-h-40 overflow-y-auto border rounded-md p-3">
                  {systemConnections.map(({ node: connection }: any) => (
                    <div key={connection.id} className="flex items-center space-x-2">
                      <Checkbox
                        id={`connection-${connection.id}`}
                        checked={formData.connection_ids.includes(connection.id)}
                        onCheckedChange={(checked) => handleConnectionChange(connection.id, !!checked)}
                      />
                      <Label
                        htmlFor={`connection-${connection.id}`}
                        className="text-sm font-normal cursor-pointer flex-1"
                      >
                        {connection.display_name || connection.carrier_name} ({connection.carrier_id})
                      </Label>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </form>
        </div>

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
          <Button type="submit" form="create-markup-form" disabled={isSubmitting}>
            {isSubmitting ? "Creating..." : "Create Markup"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

interface EditMarkupDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  markup: MarkupType | null;
  onSubmit: (data: any) => Promise<void>;
}

function EditMarkupDialog({ open, onOpenChange, markup, onSubmit }: EditMarkupDialogProps) {
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const {
    formData,
    updateFormData,
    handleCarrierChange,
    handleServiceChange,
    handleConnectionChange,
    toMutationInput,
    availableCarriers,
    availableServices,
    systemConnections,
  } = useMarkupForm(markup || undefined);

  React.useEffect(() => {
    if (markup) {
      updateFormData({
        name: markup.name || "",
        amount: markup.amount?.toString() ?? "",
        active: !!markup.active,
        is_visible: markup.is_visible ?? true,
        markup_type: markup.markup_type as MarkupTypeEnum,
        carrier_codes: Array.isArray(markup.carrier_codes) ? markup.carrier_codes : [],
        service_codes: Array.isArray(markup.service_codes) ? markup.service_codes : [],
        connection_ids: Array.isArray(markup.connection_ids) ? markup.connection_ids : [],
      } as any);
    }
  }, [markup?.id]);

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
      await onSubmit({ ...toMutationInput(), id: markup?.id });
      onOpenChange(false);
    } catch (error: any) {
      toast({
        title: "Error updating markup",
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
        <DialogHeader className="px-4 py-3 border-b sticky top-0 bg-background z-10">
          <DialogTitle>Edit Markup</DialogTitle>
          <DialogDescription>
            Update markup configuration and settings
          </DialogDescription>
        </DialogHeader>

        <div className="flex-1 overflow-y-auto px-4 py-3">
          <form id="edit-markup-form" onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div className="col-span-2">
                <Label htmlFor="edit-name">Markup Name *</Label>
                <Input
                  id="edit-name"
                  value={formData.name}
                  onChange={(e) => updateFormData({ name: e.target.value })}
                  placeholder="e.g., Fuel Surcharge, Handling Fee"
                  required
                />
              </div>

              <div>
                <Label htmlFor="edit-markup_type">Charge Type *</Label>
                <Select
                  value={formData.markup_type}
                  onValueChange={(value) => updateFormData({ markup_type: value as MarkupTypeEnum })}
                >
                  <SelectTrigger id="edit-markup_type">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value={MarkupTypeEnum.AMOUNT}>Fixed Amount ($)</SelectItem>
                    <SelectItem value={MarkupTypeEnum.PERCENTAGE}>Percentage (%)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="edit-amount">
                  Amount * {formData.markup_type === MarkupTypeEnum.PERCENTAGE ? '(%)' : '($)'}
                </Label>
                <Input
                  id="edit-amount"
                  type="number"
                  step="0.01"
                  value={formData.amount}
                  onChange={(e) => updateFormData({ amount: e.target.value })}
                  placeholder={formData.markup_type === MarkupTypeEnum.PERCENTAGE ? "5.00" : "10.00"}
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

            <div className="flex items-center justify-between">
              <Label htmlFor="edit-is_visible">Visible to Users</Label>
              <Switch
                id="edit-is_visible"
                checked={formData.is_visible}
                onCheckedChange={(checked) => updateFormData({ is_visible: checked })}
              />
            </div>

            <div>
              <Label>Carriers (leave empty for all carriers)</Label>
              <div className="grid grid-cols-3 gap-3 mt-2 max-h-40 overflow-y-auto border rounded-md p-3">
                {availableCarriers.map((carrier) => (
                  <div key={carrier} className="flex items-center space-x-2">
                    <Checkbox
                      id={`edit-carrier-${carrier}`}
                      checked={formData.carrier_codes.includes(carrier)}
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

            {formData.carrier_codes.length > 0 && availableServices.length > 0 && (
              <div>
                <Label>Services (leave empty for all services)</Label>
                <div className="grid grid-cols-2 gap-3 mt-2 max-h-40 overflow-y-auto border rounded-md p-3">
                  {availableServices.map((service) => (
                    <div key={service} className="flex items-center space-x-2">
                      <Checkbox
                        id={`edit-service-${service}`}
                        checked={formData.service_codes.includes(service)}
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

            {systemConnections.length > 0 && (
              <div>
                <Label>Connections (leave empty for all connections)</Label>
                <div className="grid grid-cols-1 gap-2 mt-2 max-h-40 overflow-y-auto border rounded-md p-3">
                  {systemConnections.map(({ node: connection }: any) => (
                    <div key={connection.id} className="flex items-center space-x-2">
                      <Checkbox
                        id={`edit-connection-${connection.id}`}
                        checked={formData.connection_ids.includes(connection.id)}
                        onCheckedChange={(checked) => handleConnectionChange(connection.id, !!checked)}
                      />
                      <Label
                        htmlFor={`edit-connection-${connection.id}`}
                        className="text-sm font-normal cursor-pointer flex-1"
                      >
                        {connection.display_name || connection.carrier_name} ({connection.carrier_id})
                      </Label>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </form>
        </div>

        <DialogFooter className="px-4 py-3 border-t sticky bottom-0 bg-background">
          <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button type="submit" form="edit-markup-form" disabled={isSubmitting}>
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
  markup: MarkupType | null;
  onConfirm: () => Promise<void>;
}

function DeleteConfirmationDialog({ open, onOpenChange, markup, onConfirm }: DeleteConfirmationDialogProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const { toast } = useToast();

  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await onConfirm();
      onOpenChange(false);
      toast({ title: "Markup deleted successfully" });
    } catch (error: any) {
      toast({
        title: "Error deleting markup",
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
          <DialogTitle>Delete Markup</DialogTitle>
          <DialogDescription>
            Are you sure you want to delete this markup? This action cannot be undone.
          </DialogDescription>
        </DialogHeader>

        {markup && (
          <div className="space-y-4">
            <Alert>
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                You are about to delete <strong>{markup.name}</strong>.
                This will remove the markup from all organizations and cannot be reversed.
              </AlertDescription>
            </Alert>

            <div className="bg-gray-50 rounded-lg p-4 space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Name:</span>
                <span className="text-sm font-medium">{markup.name}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Amount:</span>
                <span className="text-sm font-medium">
                  {markup.markup_type === 'PERCENTAGE' ? `${markup.amount}%` : `$${markup.amount}`}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Status:</span>
                <StatusBadge status={markup.active ? "active" : "inactive"} />
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
            {isDeleting ? "Deleting..." : "Delete Markup"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default function MarkupsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [selectedMarkup, setSelectedMarkup] = useState<MarkupType | null>(null);
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [selectedTab, setSelectedTab] = useState<'overview' | 'markups'>("overview");

  const { toast } = useToast();

  const {
    query: { data: { usage } = {} },
    setFilter,
    filter,
    USAGE_FILTERS,
    DAYS_LIST,
    currentFilter,
  } = useAdminSystemUsage();

  const usageFilter = filter;
  const { query: markupsQuery, markups } = useMarkups({}, usageFilter);
  const isLoading = markupsQuery.isLoading;

  const { createMarkup, updateMarkup, deleteMarkup } = useMarkupMutation();

  const handleCreateMarkup = async (data: any) => {
    await createMarkup.mutateAsync(data);
    toast({ title: "Markup created successfully" });
    setIsCreateOpen(false);
  };

  const handleEditMarkup = async (data: any) => {
    await updateMarkup.mutateAsync(data);
    toast({ title: "Markup updated successfully" });
    setIsEditOpen(false);
    setSelectedMarkup(null);
  };

  const handleDeleteMarkup = async () => {
    if (!selectedMarkup) return;
    await deleteMarkup.mutateAsync({ id: selectedMarkup.id });
    setSelectedMarkup(null);
  };

  const markupsList: MarkupType[] = useMemo(() => {
    if (!markups?.edges) return [];
    return markups.edges.map(({ node }) => node);
  }, [markups]);

  const filteredMarkups = markupsList.filter(markup => {
    const matchesSearch = markup.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      markup.id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' ||
      (statusFilter === 'active' && markup.active) ||
      (statusFilter === 'inactive' && !markup.active);

    return matchesSearch && matchesStatus;
  });

  const stats = useMemo(() => {
    const totalMarkups = markupsList.length;
    const activeMarkups = markupsList.filter(markup => markup.active).length;
    const totalMarkupsCharges = usage?.total_addons_charges || 0;

    return {
      totalMarkups,
      activeMarkups,
      totalMarkupsCharges,
    };
  }, [markupsList, usage]);

  const chartData = DAYS_LIST[currentFilter() || "15 days"].map((day) => ({
    name: day,
    charges: usage?.addons_charges?.find(({ date }) => moment(date).format("MMM D") === day)?.amount || 0,
  }));

  const { query: sysConnQuery } = useSystemConnections({}, usageFilter);
  const systemConnections = useMemo(() => (sysConnQuery.data?.system_carrier_connections?.edges || []).map(({ node }: any) => node), [sysConnQuery.data?.system_carrier_connections?.edges]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading markups...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Markups</h1>
          <p className="text-sm text-gray-600 mt-1">
            ${stats.totalMarkupsCharges.toLocaleString()}
          </p>
        </div>
      </div>

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
              selectedTab === "markups"
                ? "border-purple-500 text-purple-600"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            )}
            onClick={() => setSelectedTab("markups")}
          >
            Markups
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
          {selectedTab === 'markups' && (
            <Button onClick={() => setIsCreateOpen(true)}>
              <Plus className="mr-2 h-4 w-4" />
              Create Markup
            </Button>
          )}
        </div>
      </div>

      {selectedTab === 'overview' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <Card className="border shadow-none">
              <CardContent className="p-4">
                <p className="text-sm text-gray-600">Active Markups</p>
                <p className="text-2xl font-semibold text-gray-900">{stats.activeMarkups} / {stats.totalMarkups}</p>
              </CardContent>
            </Card>
            <Card className="border shadow-none">
              <CardContent className="p-4">
                <p className="text-sm text-gray-600">Total Charges</p>
                <p className="text-2xl font-semibold text-gray-900">${stats.totalMarkupsCharges.toLocaleString()}</p>
              </CardContent>
            </Card>
            <Card className="border shadow-none">
              <CardContent className="p-4">
                <p className="text-sm text-gray-600">System Connections</p>
                <p className="text-2xl font-semibold text-gray-900">{sysConnQuery.data?.system_carrier_connections?.page_info?.count || 0}</p>
              </CardContent>
            </Card>
          </div>

          <div>
            <div className="flex items-center gap-4 mb-4">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-blue-500"></div>
                <span className="text-sm font-medium">${stats.totalMarkupsCharges.toLocaleString()} total markup charges</span>
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
                    <p className="text-sm text-gray-500">No markup charges data available</p>
                  </div>
                </div>
              )}
            </div>
          </div>

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
                        <div className="text-xs text-gray-500">Markups</div>
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

      {selectedTab === 'markups' && (
        <div className="space-y-6">
          <div>
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
              <h2 className="text-lg font-medium text-gray-900">Markup management</h2>
              <div className="flex flex-col sm:flex-row gap-2">
                <div className="flex h-9 w-full sm:w-[200px] items-center rounded-md border border-input bg-transparent shadow-sm">
                  <Search className="ml-3 h-4 w-4 text-muted-foreground flex-shrink-0" />
                  <input
                    placeholder="Search markups..."
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
              {filteredMarkups.length === 0 ? (
                <div className="text-center py-12">
                  <Zap className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                  <h3 className="text-lg font-medium text-gray-500 mb-2">
                    No markups found
                  </h3>
                  <p className="text-sm text-gray-400">
                    {searchTerm || statusFilter !== 'all'
                      ? "No markups match your current filters."
                      : "Get started by creating your first markup."
                    }
                  </p>
                  {!searchTerm && statusFilter === 'all' && (
                    <Button className="mt-4" onClick={() => setIsCreateOpen(true)}>
                      <Plus className="mr-2 h-4 w-4" />
                      Create Your First Markup
                    </Button>
                  )}
                </div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Markup</TableHead>
                      <TableHead>Type & Amount</TableHead>
                      <TableHead>Coverage</TableHead>
                      <TableHead>Visibility</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead className="text-right">Applied Count</TableHead>
                      <TableHead className="text-right">Total Charges</TableHead>
                      <TableHead className="w-12"></TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredMarkups.map((markup) => (
                      <TableRow key={markup.id}>
                        <TableCell>
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                              {markup.markup_type === 'PERCENTAGE' ? (
                                <Percent className="h-4 w-4 text-blue-600" />
                              ) : (
                                <DollarSign className="h-4 w-4 text-green-600" />
                              )}
                            </div>
                            <div>
                              <div className="font-medium text-gray-900">
                                {markup.name}
                              </div>
                              <div className="text-sm text-gray-500">
                                ID: {markup.id.slice(-8)}
                              </div>
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <span className="font-medium text-gray-900">
                            {markup.markup_type === 'PERCENTAGE' ? `${markup.amount}%` : `$${markup.amount}`}
                          </span>
                        </TableCell>
                        <TableCell>
                          <div className="flex flex-wrap gap-1">
                            {markup.carrier_codes && markup.carrier_codes.length > 0 ? (
                              <>
                                {markup.carrier_codes.slice(0, 2).map(carrier => (
                                  <span
                                    key={carrier}
                                    className="text-xs px-1.5 py-0.5 bg-gray-100 text-gray-700 rounded"
                                  >
                                    {carrier.toUpperCase()}
                                  </span>
                                ))}
                                {markup.carrier_codes.length > 2 && (
                                  <span className="text-xs px-1.5 py-0.5 text-gray-600">
                                    +{markup.carrier_codes.length - 2}
                                  </span>
                                )}
                              </>
                            ) : (
                              <span className="text-xs text-gray-500">All carriers</span>
                            )}
                          </div>
                        </TableCell>
                        <TableCell>
                          <span className={cn(
                            "text-xs px-2 py-1 rounded",
                            markup.is_visible ? "bg-blue-100 text-blue-700" : "bg-gray-100 text-gray-500"
                          )}>
                            {markup.is_visible ? "Visible" : "Hidden"}
                          </span>
                        </TableCell>
                        <TableCell>
                          <StatusBadge status={markup.active ? "active" : "inactive"} />
                        </TableCell>
                        <TableCell className="text-right text-sm text-gray-600">
                          {markup.usage?.total_shipments?.toLocaleString() || 0}
                        </TableCell>
                        <TableCell className="text-right font-medium text-gray-900">
                          ${markup.usage?.total_addons_charges?.toLocaleString() || 0}
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
                              <DropdownMenuItem onClick={() => {
                                setSelectedMarkup(markup);
                                setIsEditOpen(true);
                              }}>
                                <Edit3 className="mr-2 h-4 w-4" />
                                Edit Markup
                              </DropdownMenuItem>
                              <DropdownMenuSeparator />
                              <DropdownMenuItem
                                className="text-red-600"
                                onClick={() => {
                                  setSelectedMarkup(markup);
                                  setIsDeleteOpen(true);
                                }}
                              >
                                <Trash2 className="mr-2 h-4 w-4" />
                                Delete Markup
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

      <CreateMarkupDialog
        open={isCreateOpen}
        onOpenChange={setIsCreateOpen}
        onSubmit={handleCreateMarkup}
      />

      <EditMarkupDialog
        open={isEditOpen}
        onOpenChange={setIsEditOpen}
        markup={selectedMarkup}
        onSubmit={handleEditMarkup}
      />

      <DeleteConfirmationDialog
        open={isDeleteOpen}
        onOpenChange={setIsDeleteOpen}
        markup={selectedMarkup}
        onConfirm={handleDeleteMarkup}
      />
    </div>
  );
}
