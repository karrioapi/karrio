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
    <div className="h-full flex flex-col bg-[#0f0c24]">
      <div className="px-4 py-3 border-b border-neutral-400">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-white">API Keys</h2>
            <p className="text-sm text-neutral-200 mt-1">
              Manage your API keys for programmatic access
            </p>
          </div>
          <Dialog open={isCreateOpen} onOpenChange={setIsCreateOpen}>
            <DialogTrigger asChild>
              <Button size="sm">
                <Plus className="h-4 w-4 mr-2" />
                Create API Key
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-lg mx-2 sm:mx-auto">
              <DialogHeader>
                <DialogTitle>Create API Key</DialogTitle>
                <DialogDescription>
                  Create a new API key for programmatic access to your account.
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleCreateSubmit} className="space-y-4 p-4 pb-8">
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

      <div className="flex-1 overflow-auto p-4">
        {apiKeys.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-neutral-500 mb-4">
              <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-3.586l6.879-6.879A6 6 0 0119 9z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-neutral-200 mb-2">No API keys</h3>
            <p className="text-neutral-400 mb-4">Get started by creating your first API key.</p>
            <Button onClick={() => setIsCreateOpen(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Create API Key
            </Button>
          </div>
        ) : (
          <div className="border-b border-neutral-800">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Label</TableHead>
                  <TableHead>Mode</TableHead>
                  <TableHead>API Key</TableHead>
                  <TableHead>Permissions</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead className="w-12"></TableHead>
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
                        <code className="text-sm bg-neutral-900 border border-neutral-800 text-neutral-200 px-2 py-1 rounded font-mono">
                          {showSecrets[apiKey.key] ? apiKey.key : `${apiKey.key.slice(0, 8)}...`}
                        </code>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => toggleSecret(apiKey.key)}
                        >
                          {showSecrets[apiKey.key] ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                        </Button>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="max-w-md">
                        {apiKey.permissions && apiKey.permissions.length > 0 ? (
                          <div className="flex flex-wrap gap-1">
                            {apiKey.permissions.slice(0, 2).map((permission) => (
                              <Badge key={permission} variant="secondary" className="text-xs">
                                {formatPermissionName(permission)}
                              </Badge>
                            ))}
                            {apiKey.permissions.length > 2 && (
                              <Badge variant="secondary" className="text-xs">
                                +{apiKey.permissions.length - 2}
                              </Badge>
                            )}
                          </div>
                        ) : (
                          <span className="text-xs text-neutral-400">No permissions</span>
                        )}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="text-sm text-neutral-400">
                        {formatDateTimeLong(apiKey.created)}
                      </div>
                    </TableCell>
                    <TableCell>
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                            <MoreHorizontal className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem onClick={() => copyToClipboard(apiKey.key)}>
                            <Copy className="h-4 w-4 mr-2" />
                            Copy API Key
                          </DropdownMenuItem>
                          <DropdownMenuItem
                            onClick={() => handleDelete(apiKey.key)}
                            className="text-destructive"
                          >
                            <Trash2 className="h-4 w-4 mr-2" />
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
        )}
      </div>
    </div>
  );
}
