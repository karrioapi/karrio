"use client";

import React from 'react';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@karrio/ui/components/ui/dropdown-menu";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@karrio/ui/components/ui/dialog";
import { Plus, Search, MoreHorizontal, Edit3, Trash2, Eye, Building2, DollarSign, Percent, Zap } from 'lucide-react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@karrio/ui/components/ui/table";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { useAddons, useAddonMutation } from "@karrio/hooks/admin-addons";
import { SurchargeTypeEnum } from "@karrio/types/graphql/admin/types";
import { Switch } from "@karrio/ui/components/ui/switch";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Label } from "@karrio/ui/components/ui/label";
import { useToast } from "@karrio/ui/hooks/use-toast";

// Import proper types from GraphQL schema
import {
  GetAddons_addons_edges_node as AddonType
} from "@karrio/types/graphql/admin/types";

export default function AddonsPage() {
  const [searchTerm, setSearchTerm] = React.useState('');
  const [statusFilter, setStatusFilter] = React.useState<string>('all');
  const [isCreateOpen, setIsCreateOpen] = React.useState(false);
  const { toast } = useToast();

  // Fetch addons data
  const { query, addons } = useAddons();
  const isLoading = query.isLoading;

  // Mutations
  const { createAddon } = useAddonMutation();

  const handleCreateAddon = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    try {
      await createAddon.mutateAsync({
        name: formData.get('name') as string,
        amount: parseFloat(formData.get('amount') as string),
        surcharge_type: formData.get('surcharge_type') as SurchargeTypeEnum,
        active: formData.get('active') === 'on',
        carriers: formData.get('carriers') ? (formData.get('carriers') as string).split(',').map(c => c.trim()) : [],
        services: formData.get('services') ? (formData.get('services') as string).split(',').map(s => s.trim()) : [],
      });

      toast({ title: "Addon created successfully" });
      setIsCreateOpen(false);
    } catch (error) {
      toast({ title: "Failed to create addon", variant: "destructive" });
    }
  };

  // Convert addons data to proper format
  const addonsList: AddonType[] = React.useMemo(() => {
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

  // Calculate statistics
  const stats = addonsList.reduce((acc, addon) => ({
    totalAddons: acc.totalAddons + 1,
    activeAddons: acc.activeAddons + (addon.active ? 1 : 0),
    totalAmount: acc.totalAmount + addon.amount,
  }), {
    totalAddons: 0,
    activeAddons: 0,
    totalAmount: 0,
  });

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
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Shippers Addons</h1>
          <p className="text-muted-foreground">
            Manage addons across all organizations and track commission revenue
          </p>
        </div>
        <Button onClick={() => setIsCreateOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          Create Addon
        </Button>
      </div>

      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Addons</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalAddons}</div>
            <p className="text-xs text-muted-foreground">
              {stats.activeAddons} active
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Commission Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${(stats.totalAmount * 0.025).toLocaleString(undefined, { minimumFractionDigits: 2 })}
            </div>
            <p className="text-xs text-muted-foreground">
              ~2.5% avg commission rate
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
            <Percent className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${stats.totalAmount.toLocaleString(undefined, { minimumFractionDigits: 2 })}
            </div>
            <p className="text-xs text-muted-foreground">
              Across all organizations
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Organizations</CardTitle>
            <Building2 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{addonsList.length}</div>
            <p className="text-xs text-muted-foreground">
              Using addons
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle>Addon Management</CardTitle>
          <CardDescription>
            Configure and manage shipping addons for marketplace organizations
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search addons..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-8"
                />
              </div>
            </div>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Filter by status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="active">Active</SelectItem>
                <SelectItem value="inactive">Inactive</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Addons Table */}
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Addon</TableHead>
                  <TableHead>Type & Amount</TableHead>
                  <TableHead>Coverage</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredAddons.map((addon) => (
                  <TableRow key={addon.id}>
                    <TableCell>
                      <div>
                        <div className="font-medium">{addon.name}</div>
                        <div className="text-sm text-muted-foreground">{addon.id}</div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        {addon.surcharge_type === 'PERCENTAGE' ? (
                          <Percent className="h-4 w-4 text-blue-500" />
                        ) : (
                          <DollarSign className="h-4 w-4 text-green-500" />
                        )}
                        <span className="font-medium">
                          {addon.surcharge_type === 'PERCENTAGE' ? `${addon.amount}%` : `$${addon.amount}`}
                        </span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex flex-wrap gap-1">
                        {addon.carriers?.slice(0, 2).map(carrier => (
                          <Badge key={carrier} variant="outline" className="text-xs">
                            {carrier.toUpperCase()}
                          </Badge>
                        ))}
                        {addon.carriers && addon.carriers.length > 2 && (
                          <Badge variant="outline" className="text-xs">
                            +{addon.carriers.length - 2}
                          </Badge>
                        )}
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant={addon.active ? "default" : "secondary"}>
                        {addon.active ? "Active" : "Inactive"}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" className="h-8 w-8 p-0">
                            <MoreHorizontal className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuLabel>Actions</DropdownMenuLabel>
                          <DropdownMenuItem>
                            <Eye className="mr-2 h-4 w-4" />
                            View Details
                          </DropdownMenuItem>
                          <DropdownMenuItem>
                            <Edit3 className="mr-2 h-4 w-4" />
                            Edit Addon
                          </DropdownMenuItem>
                          <DropdownMenuItem>
                            <Building2 className="mr-2 h-4 w-4" />
                            Manage Organizations
                          </DropdownMenuItem>
                          <DropdownMenuSeparator />
                          <DropdownMenuItem className="text-red-600">
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
          </div>

          {filteredAddons.length === 0 && (
            <div className="text-center py-6">
              <p className="text-muted-foreground">No addons found matching your filters.</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Create Addon Modal */}
      <Dialog open={isCreateOpen} onOpenChange={setIsCreateOpen}>
        <DialogContent className="sm:max-w-[500px]">
          <DialogHeader>
            <DialogTitle>Create New Addon</DialogTitle>
            <DialogDescription>
              Create a new shipping addon that can be applied to shipments across organizations.
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleCreateAddon} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Addon Name</Label>
              <Input
                id="name"
                name="name"
                placeholder="e.g., Insurance Fee, Handling Charge"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="amount">Amount</Label>
                <Input
                  id="amount"
                  name="amount"
                  type="number"
                  step="0.01"
                  placeholder="0.00"
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="surcharge_type">Type</Label>
                <Select name="surcharge_type" defaultValue={SurchargeTypeEnum.AMOUNT}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value={SurchargeTypeEnum.AMOUNT}>Fixed Amount</SelectItem>
                    <SelectItem value={SurchargeTypeEnum.PERCENTAGE}>Percentage</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="carriers">Carriers (comma-separated)</Label>
              <Input
                id="carriers"
                name="carriers"
                placeholder="e.g., fedex, ups, usps"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="services">Services (comma-separated)</Label>
              <Input
                id="services"
                name="services"
                placeholder="e.g., ground, express, priority"
              />
            </div>

            <div className="flex items-center space-x-2">
              <Switch id="active" name="active" defaultChecked />
              <Label htmlFor="active">Active</Label>
            </div>

            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={() => setIsCreateOpen(false)}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                disabled={createAddon.isLoading}
              >
                {createAddon.isLoading ? "Creating..." : "Create Addon"}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
