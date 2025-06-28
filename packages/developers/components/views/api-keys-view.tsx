"use client";

import React, { useState } from "react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@karrio/ui/components/ui/dialog";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@karrio/ui/components/ui/table";
import { Trash2, Plus, Copy, Eye, EyeOff, Calendar, MoreHorizontal } from "lucide-react";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@karrio/ui/components/ui/dropdown-menu";
import { useAPIKeys, useAPIKeyMutation } from "@karrio/hooks/api-keys";
import { useNotifier } from "@karrio/ui/core/components/notifier";
import { Checkbox } from "@karrio/ui/components/ui/checkbox";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Badge } from "@karrio/ui/components/ui/badge";
import { NotificationType } from "@karrio/types";
import { formatDateTimeLong } from "@karrio/lib";

type CreateFormData = {
  label: string;
  password: string;
  permissions: string[];
};

// Available permissions - these should match what's available in the system
const AVAILABLE_PERMISSIONS = [
  "manage_apps",
  "manage_carriers",
  "manage_orders",
  "manage_team",
  "manage_org_owner",
  "manage_webhooks",
  "manage_data",
  "manage_shipments",
  "manage_system",
  "manage_trackers",
  "manage_pickups"
];

// Helper function to format permission names for display
const formatPermissionName = (permission: string) => {
  return permission
    .replace(/^manage_/, '')
    .replace(/_/g, ' ')
    .replace(/\b\w/g, l => l.toUpperCase());
};

export function ApiKeysView() {
  const notifier = useNotifier();
  const { query } = useAPIKeys();
  const { createAPIKey, deleteAPIKey } = useAPIKeyMutation();
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [showSecrets, setShowSecrets] = useState<Record<string, boolean>>({});
  const [formData, setFormData] = useState<CreateFormData>({
    label: "",
    password: "",
    permissions: [],
  });

  const apiKeys = query.data?.api_keys || [];

  const handleCreateSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const result = await createAPIKey.mutateAsync(formData);
      if (result.create_api_key.errors && result.create_api_key.errors.length > 0) {
        const errorMessages = result.create_api_key.errors.map(e => e.messages.join(", ")).join("; ");
        notifier.notify({
          type: NotificationType.error,
          message: errorMessages,
        });
      } else {
        notifier.notify({
          type: NotificationType.success,
          message: "API key created successfully!",
        });
        setIsCreateOpen(false);
        setFormData({ label: "", password: "", permissions: [] });
      }
    } catch (error: any) {
      notifier.notify({
        type: NotificationType.error,
        message: error.message || "Failed to create API key",
      });
    }
  };

  const handleDelete = async (key: string) => {
    const password = prompt("Enter your password to delete this API key:");
    if (!password) return;

    try {
      const result = await deleteAPIKey.mutateAsync({ key, password });
      if (result.delete_api_key.errors && result.delete_api_key.errors.length > 0) {
        const errorMessages = result.delete_api_key.errors.map(e => e.messages.join(", ")).join("; ");
        notifier.notify({
          type: NotificationType.error,
          message: errorMessages,
        });
      } else {
        notifier.notify({
          type: NotificationType.success,
          message: "API key deleted successfully!",
        });
      }
    } catch (error: any) {
      notifier.notify({
        type: NotificationType.error,
        message: error.message || "Failed to delete API key",
      });
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    notifier.notify({
      type: NotificationType.success,
      message: "Copied to clipboard!",
    });
  };

  const toggleSecret = (key: string) => {
    setShowSecrets(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="h-full flex flex-col">
      <div className="px-2 sm:px-4 py-3 border-b border-slate-200">
        <div className="flex items-start sm:items-center justify-between flex-col sm:flex-row gap-3 sm:gap-0">
          <div>
            <h2 className="text-lg font-semibold">API Keys</h2>
            <p className="text-xs sm:text-sm text-muted-foreground mt-1">
              Manage your API keys for programmatic access
            </p>
          </div>
          <Dialog open={isCreateOpen} onOpenChange={setIsCreateOpen}>
            <DialogTrigger asChild>
              <Button size="sm" className="w-full sm:w-auto">
                <Plus className="h-4 w-4 mr-2" />
                Create API Key
              </Button>
            </DialogTrigger>
            <DialogContent className="p-4 pb-8 max-w-lg mx-2 sm:mx-auto">
              <DialogHeader>
                <DialogTitle>Create API Key</DialogTitle>
                <DialogDescription>
                  Create a new API key for programmatic access to your account.
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleCreateSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="label">Label</Label>
                  <Input
                    id="label"
                    value={formData.label}
                    onChange={(e) => setFormData(prev => ({ ...prev, label: e.target.value }))}
                    placeholder="Enter a descriptive label"
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="password">Password</Label>
                  <Input
                    id="password"
                    type="password"
                    value={formData.password}
                    onChange={(e) => setFormData(prev => ({ ...prev, password: e.target.value }))}
                    placeholder="Enter your account password"
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label>Permissions</Label>
                  <div className="space-y-2 max-h-48 overflow-y-auto">
                    {AVAILABLE_PERMISSIONS.map((permission) => (
                      <div key={permission} className="flex items-center space-x-2">
                        <Checkbox
                          id={permission}
                          checked={formData.permissions.includes(permission)}
                          onCheckedChange={(checked) => {
                            if (checked) {
                              setFormData(prev => ({
                                ...prev,
                                permissions: [...prev.permissions, permission]
                              }));
                            } else {
                              setFormData(prev => ({
                                ...prev,
                                permissions: prev.permissions.filter(p => p !== permission)
                              }));
                            }
                          }}
                        />
                        <Label htmlFor={permission} className="text-sm">
                          {formatPermissionName(permission)}
                        </Label>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="flex flex-col sm:flex-row justify-end space-y-2 sm:space-y-0 sm:space-x-2">
                  <Button type="button" variant="outline" onClick={() => setIsCreateOpen(false)} className="w-full sm:w-auto">
                    Cancel
                  </Button>
                  <Button type="submit" disabled={createAPIKey.isLoading} className="w-full sm:w-auto">
                    {createAPIKey.isLoading ? "Creating..." : "Create API Key"}
                  </Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      <div className="flex-1 overflow-auto">
        {apiKeys.length === 0 ? (
          <div className="text-center py-8 sm:py-12 px-4">
            <div className="text-slate-400 mb-4">
              <svg className="mx-auto h-10 w-10 sm:h-12 sm:w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-3.586l6.879-6.879A6 6 0 0119 9z" />
              </svg>
            </div>
            <h3 className="text-base sm:text-lg font-medium text-slate-900 mb-2">No API keys</h3>
            <p className="text-sm text-slate-500 mb-4">Get started by creating your first API key.</p>
            <Button onClick={() => setIsCreateOpen(true)} className="w-full sm:w-auto">
              <Plus className="h-4 w-4 mr-2" />
              Create API Key
            </Button>
          </div>
        ) : (
          <>
            {/* Desktop Table View */}
            <div className="hidden lg:block">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-[200px]">Label</TableHead>
                    <TableHead className="w-[100px]">Mode</TableHead>
                    <TableHead>API Key</TableHead>
                    <TableHead className="w-[200px]">Permissions</TableHead>
                    <TableHead className="w-[150px]">Created</TableHead>
                    <TableHead className="w-[50px]"></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {apiKeys.map((apiKey) => (
                    <TableRow key={apiKey.key}>
                      <TableCell className="font-medium">
                        {apiKey.label}
                      </TableCell>
                      <TableCell>
                        <Badge variant={apiKey.test_mode ? "secondary" : "default"}>
                          {apiKey.test_mode ? "Test" : "Live"}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <code className="flex-1 text-sm bg-slate-50 px-2 py-1 rounded font-mono max-w-[300px] truncate">
                            {showSecrets[apiKey.key] ? apiKey.key : `${apiKey.key.slice(0, 12)}...${apiKey.key.slice(-4)}`}
                          </code>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => toggleSecret(apiKey.key)}
                            className="h-7 w-7 p-0"
                          >
                            {showSecrets[apiKey.key] ? <EyeOff className="h-3 w-3" /> : <Eye className="h-3 w-3" />}
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => copyToClipboard(apiKey.key)}
                            className="h-7 w-7 p-0"
                          >
                            <Copy className="h-3 w-3" />
                          </Button>
                        </div>
                      </TableCell>
                      <TableCell>
                        {apiKey.permissions && apiKey.permissions.length > 0 ? (
                          <div className="flex flex-wrap gap-1">
                            {apiKey.permissions.slice(0, 2).map((permission) => (
                              <Badge key={permission} variant="outline" className="text-xs">
                                {formatPermissionName(permission)}
                              </Badge>
                            ))}
                            {apiKey.permissions.length > 2 && (
                              <Badge variant="outline" className="text-xs">
                                +{apiKey.permissions.length - 2} more
                              </Badge>
                            )}
                          </div>
                        ) : (
                          <span className="text-sm text-muted-foreground">No permissions</span>
                        )}
                      </TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        {formatDateTimeLong(apiKey.created)}
                      </TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" className="h-8 w-8 p-0">
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem
                              onClick={() => copyToClipboard(apiKey.key)}
                              className="text-sm"
                            >
                              <Copy className="mr-2 h-4 w-4" />
                              Copy Key
                            </DropdownMenuItem>
                            <DropdownMenuItem
                              onClick={() => handleDelete(apiKey.key)}
                              className="text-sm text-red-600 focus:text-red-600"
                            >
                              <Trash2 className="mr-2 h-4 w-4" />
                              Delete
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>

            {/* Mobile Card View */}
            <div className="lg:hidden p-2 sm:p-4 space-y-3">
              {apiKeys.map((apiKey) => (
                <div key={apiKey.key} className="border rounded-lg p-3 sm:p-4 bg-white">
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <h3 className="font-medium text-sm sm:text-base">{apiKey.label}</h3>
                      <Badge variant={apiKey.test_mode ? "secondary" : "default"} className="mt-1 text-xs">
                        {apiKey.test_mode ? "Test" : "Live"}
                      </Badge>
                    </div>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="h-8 w-8 p-0">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem
                          onClick={() => copyToClipboard(apiKey.key)}
                          className="text-sm"
                        >
                          <Copy className="mr-2 h-4 w-4" />
                          Copy Key
                        </DropdownMenuItem>
                        <DropdownMenuItem
                          onClick={() => handleDelete(apiKey.key)}
                          className="text-sm text-red-600 focus:text-red-600"
                        >
                          <Trash2 className="mr-2 h-4 w-4" />
                          Delete
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>

                  <div className="space-y-3">
                    <div>
                      <Label className="text-xs text-muted-foreground">API Key</Label>
                      <div className="flex items-center gap-2 mt-1">
                        <code className="flex-1 text-xs sm:text-sm bg-slate-50 px-2 py-1 rounded font-mono truncate">
                          {showSecrets[apiKey.key] ? apiKey.key : `${apiKey.key.slice(0, 12)}...${apiKey.key.slice(-4)}`}
                        </code>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => toggleSecret(apiKey.key)}
                          className="h-7 w-7 p-0 flex-shrink-0"
                        >
                          {showSecrets[apiKey.key] ? <EyeOff className="h-3 w-3" /> : <Eye className="h-3 w-3" />}
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => copyToClipboard(apiKey.key)}
                          className="h-7 w-7 p-0 flex-shrink-0"
                        >
                          <Copy className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>

                    <div>
                      <Label className="text-xs text-muted-foreground">Permissions</Label>
                      <div className="mt-1">
                        {apiKey.permissions && apiKey.permissions.length > 0 ? (
                          <div className="flex flex-wrap gap-1">
                            {apiKey.permissions.slice(0, 3).map((permission) => (
                              <Badge key={permission} variant="outline" className="text-xs">
                                {formatPermissionName(permission)}
                              </Badge>
                            ))}
                            {apiKey.permissions.length > 3 && (
                              <Badge variant="outline" className="text-xs">
                                +{apiKey.permissions.length - 3} more
                              </Badge>
                            )}
                          </div>
                        ) : (
                          <span className="text-xs text-muted-foreground">No permissions</span>
                        )}
                      </div>
                    </div>

                    <div>
                      <Label className="text-xs text-muted-foreground">Created</Label>
                      <p className="text-xs sm:text-sm mt-1">{formatDateTimeLong(apiKey.created)}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Tablet Horizontal Scroll View */}
            <div className="hidden sm:block lg:hidden overflow-x-auto">
              <div className="min-w-[700px]">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead className="w-[150px]">Label</TableHead>
                      <TableHead className="w-[80px]">Mode</TableHead>
                      <TableHead className="w-[250px]">API Key</TableHead>
                      <TableHead className="w-[150px]">Permissions</TableHead>
                      <TableHead className="w-[120px]">Created</TableHead>
                      <TableHead className="w-[50px]"></TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {apiKeys.map((apiKey) => (
                      <TableRow key={apiKey.key}>
                        <TableCell className="font-medium text-sm">
                          {apiKey.label}
                        </TableCell>
                        <TableCell>
                          <Badge variant={apiKey.test_mode ? "secondary" : "default"} className="text-xs">
                            {apiKey.test_mode ? "Test" : "Live"}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center gap-2">
                            <code className="flex-1 text-xs bg-slate-50 px-2 py-1 rounded font-mono max-w-[180px] truncate">
                              {showSecrets[apiKey.key] ? apiKey.key : `${apiKey.key.slice(0, 12)}...${apiKey.key.slice(-4)}`}
                            </code>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => toggleSecret(apiKey.key)}
                              className="h-7 w-7 p-0"
                            >
                              {showSecrets[apiKey.key] ? <EyeOff className="h-3 w-3" /> : <Eye className="h-3 w-3" />}
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => copyToClipboard(apiKey.key)}
                              className="h-7 w-7 p-0"
                            >
                              <Copy className="h-3 w-3" />
                            </Button>
                          </div>
                        </TableCell>
                        <TableCell>
                          {apiKey.permissions && apiKey.permissions.length > 0 ? (
                            <div className="flex flex-wrap gap-1">
                              {apiKey.permissions.slice(0, 1).map((permission) => (
                                <Badge key={permission} variant="outline" className="text-xs">
                                  {formatPermissionName(permission)}
                                </Badge>
                              ))}
                              {apiKey.permissions.length > 1 && (
                                <Badge variant="outline" className="text-xs">
                                  +{apiKey.permissions.length - 1} more
                                </Badge>
                              )}
                            </div>
                          ) : (
                            <span className="text-xs text-muted-foreground">No permissions</span>
                          )}
                        </TableCell>
                        <TableCell className="text-xs text-muted-foreground">
                          {formatDateTimeLong(apiKey.created)}
                        </TableCell>
                        <TableCell>
                          <DropdownMenu>
                            <DropdownMenuTrigger asChild>
                              <Button variant="ghost" className="h-8 w-8 p-0">
                                <MoreHorizontal className="h-4 w-4" />
                              </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent align="end">
                              <DropdownMenuItem
                                onClick={() => copyToClipboard(apiKey.key)}
                                className="text-sm"
                              >
                                <Copy className="mr-2 h-4 w-4" />
                                Copy Key
                              </DropdownMenuItem>
                              <DropdownMenuItem
                                onClick={() => handleDelete(apiKey.key)}
                                className="text-sm text-red-600 focus:text-red-600"
                              >
                                <Trash2 className="mr-2 h-4 w-4" />
                                Delete
                              </DropdownMenuItem>
                            </DropdownMenuContent>
                          </DropdownMenu>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
