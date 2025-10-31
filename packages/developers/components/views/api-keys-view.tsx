"use client";

import React, { useState } from "react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger, DialogPortal } from "@karrio/ui/components/ui/dialog";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@karrio/ui/components/ui/table";
import { Trash2, Plus, Copy, Eye, EyeOff, Calendar, MoreHorizontal } from "lucide-react";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger, DropdownMenuPortal } from "@karrio/ui/components/ui/dropdown-menu";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@karrio/ui/components/ui/tooltip";
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
    <div className="h-full flex flex-col bg-background">
      <div className="px-4 py-3 border-b border-border">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-foreground">API Keys</h2>
            <p className="text-sm text-muted-foreground mt-1">
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
            <DialogPortal container={typeof document !== 'undefined' ? document.getElementById('devtools-portal') as any : undefined}>
              <DialogContent className="devtools-theme dark max-w-lg mx-2 sm:mx-auto bg-popover border-border text-foreground">
                <DialogHeader className="bg-popover border-b border-border px-4 py-3 text-foreground">
                  <DialogTitle className="text-foreground">Create API Key</DialogTitle>
                  <DialogDescription className="text-muted-foreground">
                    Create a new API key for programmatic access to your account.
                  </DialogDescription>
                </DialogHeader>
                <form onSubmit={handleCreateSubmit} className="space-y-4 p-4 pb-8">
                  <div className="space-y-2">
                    <Label htmlFor="label" className="text-muted-foreground">Label</Label>
                    <Input
                      id="label"
                      value={formData.label}
                      onChange={(e) => setFormData(prev => ({ ...prev, label: e.target.value }))}
                      placeholder="Enter a descriptive label"
                      required
                      className="bg-input border-border text-foreground placeholder:text-muted-foreground"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="password" className="text-muted-foreground">Password</Label>
                    <Input
                      id="password"
                      type="password"
                      value={formData.password}
                      onChange={(e) => setFormData(prev => ({ ...prev, password: e.target.value }))}
                      placeholder="Enter your account password"
                      required
                      className="bg-input border-border text-foreground placeholder:text-muted-foreground"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label className="text-muted-foreground">Permissions</Label>
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
                          <Label htmlFor={permission} className="text-sm text-muted-foreground">
                            {formatPermissionName(permission)}
                          </Label>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="flex flex-col sm:flex-row justify-end space-y-2 sm:space-y-0 sm:space-x-2">
                    <Button type="button" variant="outline" onClick={() => setIsCreateOpen(false)} className="w-full sm:w-auto !text-foreground !bg-card !border-border hover:!bg-primary/10 hover:!text-primary">
                      Cancel
                    </Button>
                    <Button type="submit" disabled={createAPIKey.isLoading} className="w-full sm:w-auto">
                      {createAPIKey.isLoading ? "Creating..." : "Create API Key"}
                    </Button>
                  </div>
                </form>
              </DialogContent>
            </DialogPortal>
          </Dialog>
        </div>
      </div>

      <div className="flex-1 overflow-auto p-4">
        {apiKeys.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-muted-foreground mb-4">
              <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-3.586l6.879-6.879A6 6 0 0119 9z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-foreground mb-2">No API keys</h3>
            <p className="text-muted-foreground mb-4">Get started by creating your first API key.</p>
            <Button onClick={() => setIsCreateOpen(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Create API Key
            </Button>
          </div>
        ) : (
          <div className="border-b border-border text-foreground overflow-x-auto sm:overflow-x-visible" style={{ touchAction: 'pan-x', WebkitOverflowScrolling: 'touch', overscrollBehaviorX: 'contain' }}>
            <div className="inline-block w-full min-w-[900px] sm:min-w-0 align-top">
              <Table className="w-full table-auto">
                <TableHeader>
                  <TableRow>
                    <TableHead className="text-foreground">Label</TableHead>
                    <TableHead className="text-foreground">Mode</TableHead>
                    <TableHead className="text-foreground">API Key</TableHead>
                    <TableHead className="text-foreground">Permissions</TableHead>
                    <TableHead className="text-foreground">Created</TableHead>
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
                          <code className="text-sm bg-muted border border-border text-foreground px-2 py-1 rounded font-mono">
                            {showSecrets[apiKey.key] ? apiKey.key : `${apiKey.key.slice(0, 8)}...`}
                          </code>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => toggleSecret(apiKey.key)}
                          >
                            {showSecrets[apiKey.key] ? <EyeOff className="h-4 w-4 text-muted-foreground" /> : <Eye className="h-4 w-4 text-muted-foreground" />}
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
                                <>
                                  <div className="hidden sm:block">
                                    <TooltipProvider>
                                      <Tooltip>
                                        <TooltipTrigger asChild>
                                          <Badge variant="secondary" className="text-xs cursor-default">
                                            +{apiKey.permissions.length - 2}
                                          </Badge>
                                        </TooltipTrigger>
                                        <TooltipContent side="bottom" sideOffset={6} className="bg-popover text-foreground border border-border">
                                          <div className="max-w-xs text-xs space-y-1">
                                            {apiKey.permissions.slice(2).map((permission: string) => (
                                              <div key={permission}>{formatPermissionName(permission)}</div>
                                            ))}
                                          </div>
                                        </TooltipContent>
                                      </Tooltip>
                                    </TooltipProvider>
                                  </div>
                                  <div className="sm:hidden">
                                    <DropdownMenu>
                                      <DropdownMenuTrigger asChild>
                                        <Button variant="secondary" size="sm" className="h-5 px-2 text-xs">
                                          +{apiKey.permissions.length - 2}
                                        </Button>
                                      </DropdownMenuTrigger>
                                      <DropdownMenuPortal container={typeof document !== 'undefined' ? document.getElementById('devtools-portal') as any : undefined}>
                                        <DropdownMenuContent side="bottom" align="start" className="devtools-theme dark bg-popover text-foreground border-border">
                                          <div className="max-w-xs text-xs space-y-1 px-2 py-1">
                                            {apiKey.permissions.slice(2).map((permission: string) => (
                                              <div key={permission}>{formatPermissionName(permission)}</div>
                                            ))}
                                          </div>
                                        </DropdownMenuContent>
                                      </DropdownMenuPortal>
                                    </DropdownMenu>
                                  </div>
                                </>
                              )}
                            </div>
                          ) : (
                            <span className="text-xs text-muted-foreground">No permissions</span>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="text-sm text-muted-foreground">
                          {formatDateTimeLong(apiKey.created)}
                        </div>
                      </TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="lg" className="h-8 w-8 p-0">
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuPortal container={typeof document !== 'undefined' ? document.getElementById('devtools-portal') as any : undefined}>
                            <DropdownMenuContent align="end" className="devtools-theme dark bg-popover text-foreground border-border">
                              <DropdownMenuItem onClick={() => copyToClipboard(apiKey.key)} className="text-foreground focus:bg-primary/20 focus:text-foreground">
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
                          </DropdownMenuPortal>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
