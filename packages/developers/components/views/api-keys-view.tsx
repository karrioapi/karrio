"use client";

import React, { useState } from "react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger, DialogPortal } from "@karrio/ui/components/ui/dialog";
import { Trash2, Plus, Copy, Eye, EyeOff, MoreHorizontal, Check, Key, ShieldCheck } from "lucide-react";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger, DropdownMenuPortal, DropdownMenuSeparator } from "@karrio/ui/components/ui/dropdown-menu";
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
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<string | null>(null);
  const [deletePassword, setDeletePassword] = useState("");
  const [showSecrets, setShowSecrets] = useState<Record<string, boolean>>({});
  const [copiedKey, setCopiedKey] = useState<string | null>(null);
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

  const handleDeleteConfirm = async () => {
    if (!deleteTarget || !deletePassword) return;
    try {
      const result = await deleteAPIKey.mutateAsync({ key: deleteTarget, password: deletePassword });
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
        setIsDeleteOpen(false);
        setDeleteTarget(null);
        setDeletePassword("");
      }
    } catch (error: any) {
      notifier.notify({
        type: NotificationType.error,
        message: error.message || "Failed to delete API key",
      });
    }
  };

  const copyToClipboard = (key: string) => {
    navigator.clipboard.writeText(key);
    setCopiedKey(key);
    notifier.notify({
      type: NotificationType.success,
      message: "API key copied to clipboard",
    });
    setTimeout(() => setCopiedKey(null), 2000);
  };

  const toggleSecret = (key: string) => {
    setShowSecrets(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const openDeleteDialog = (key: string) => {
    setDeleteTarget(key);
    setDeletePassword("");
    setIsDeleteOpen(true);
  };

  const toggleAllPermissions = (checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      permissions: checked ? [...AVAILABLE_PERMISSIONS] : [],
    }));
  };

  return (
    <div className="h-full flex flex-col bg-background">
      {/* Header */}
      <div className="px-4 py-4 border-b border-border">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-foreground">API Keys</h2>
            <p className="text-sm text-muted-foreground mt-0.5">
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
                <form onSubmit={handleCreateSubmit} className="space-y-4 p-4 pb-6">
                  <div className="space-y-2">
                    <Label htmlFor="label" className="text-muted-foreground text-xs font-medium">KEY NAME</Label>
                    <Input
                      id="label"
                      value={formData.label}
                      onChange={(e) => setFormData(prev => ({ ...prev, label: e.target.value }))}
                      placeholder="e.g. Production API Key"
                      required
                      className="bg-input border-border text-foreground placeholder:text-muted-foreground"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="password" className="text-muted-foreground text-xs font-medium">ACCOUNT PASSWORD</Label>
                    <Input
                      id="password"
                      type="password"
                      value={formData.password}
                      onChange={(e) => setFormData(prev => ({ ...prev, password: e.target.value }))}
                      placeholder="Enter your password to confirm"
                      required
                      className="bg-input border-border text-foreground placeholder:text-muted-foreground"
                    />
                  </div>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Label className="text-muted-foreground text-xs font-medium">PERMISSIONS</Label>
                      <Button
                        type="button"
                        variant="link"
                        size="sm"
                        className="text-xs text-primary p-0 h-auto"
                        onClick={() => toggleAllPermissions(formData.permissions.length !== AVAILABLE_PERMISSIONS.length)}
                      >
                        {formData.permissions.length === AVAILABLE_PERMISSIONS.length ? "Deselect all" : "Select all"}
                      </Button>
                    </div>
                    <div className="grid grid-cols-2 gap-2 max-h-48 overflow-y-auto p-1">
                      {AVAILABLE_PERMISSIONS.map((permission) => (
                        <div key={permission} className="flex items-center space-x-2 py-1">
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
                          <Label htmlFor={permission} className="text-sm text-muted-foreground cursor-pointer">
                            {formatPermissionName(permission)}
                          </Label>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="flex justify-end space-x-2 pt-2">
                    <Button type="button" variant="outline" onClick={() => setIsCreateOpen(false)} className="!text-foreground !bg-card !border-border hover:!bg-primary/10 hover:!text-primary">
                      Cancel
                    </Button>
                    <Button type="submit" disabled={createAPIKey.isLoading}>
                      {createAPIKey.isLoading ? "Creating..." : "Create API Key"}
                    </Button>
                  </div>
                </form>
              </DialogContent>
            </DialogPortal>
          </Dialog>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto p-4">
        {apiKeys.length === 0 ? (
          <div className="text-center py-16">
            <div className="mx-auto w-14 h-14 rounded-full bg-primary/10 flex items-center justify-center mb-4">
              <Key className="h-7 w-7 text-primary" />
            </div>
            <h3 className="text-lg font-medium text-foreground mb-2">No API keys yet</h3>
            <p className="text-sm text-muted-foreground mb-6 max-w-sm mx-auto">
              Create an API key to authenticate your requests and start integrating with the API.
            </p>
            <Button onClick={() => setIsCreateOpen(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Create your first API Key
            </Button>
          </div>
        ) : (
          <div className="space-y-3">
            {apiKeys.map((apiKey) => (
              <div
                key={apiKey.key}
                className="bg-card border border-border rounded-lg p-4 hover:border-primary/30 transition-colors"
              >
                <div className="flex items-start justify-between gap-3">
                  {/* Left: Key info */}
                  <div className="flex-1 min-w-0 space-y-2">
                    {/* Name + Mode */}
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium text-foreground truncate">
                        {apiKey.label}
                      </span>
                      <Badge
                        variant={apiKey.test_mode ? "secondary" : "default"}
                        className="text-xs flex-shrink-0"
                      >
                        {apiKey.test_mode ? "Test" : "Live"}
                      </Badge>
                    </div>

                    {/* Token */}
                    <div className="flex items-center gap-2">
                      <code className="text-xs bg-muted border border-border text-foreground px-2.5 py-1 rounded font-mono">
                        {showSecrets[apiKey.key] ? apiKey.key : `${apiKey.key.slice(0, 12)}...${apiKey.key.slice(-4)}`}
                      </code>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="text-muted-foreground hover:text-foreground"
                        onClick={() => toggleSecret(apiKey.key)}
                      >
                        {showSecrets[apiKey.key] ? <EyeOff className="h-[18px] w-[18px]" /> : <Eye className="h-[18px] w-[18px]" />}
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="text-muted-foreground hover:text-foreground"
                        onClick={() => copyToClipboard(apiKey.key)}
                      >
                        {copiedKey === apiKey.key ? (
                          <Check className="h-[18px] w-[18px] text-green-400" />
                        ) : (
                          <Copy className="h-[18px] w-[18px]" />
                        )}
                      </Button>
                    </div>

                    {/* Permissions + Created */}
                    <div className="flex items-center gap-3 flex-wrap">
                      {apiKey.permissions && apiKey.permissions.length > 0 ? (
                        <div className="flex items-center gap-1">
                          <ShieldCheck className="h-3 w-3 text-muted-foreground" />
                          <span className="text-xs text-muted-foreground">
                            {apiKey.permissions.length === AVAILABLE_PERMISSIONS.length
                              ? "Full access"
                              : `${apiKey.permissions.length} permission${apiKey.permissions.length !== 1 ? 's' : ''}`}
                          </span>
                        </div>
                      ) : (
                        <span className="text-xs text-muted-foreground">No permissions</span>
                      )}
                      <span className="text-xs text-muted-foreground/50">|</span>
                      <span className="text-xs text-muted-foreground">
                        Created {formatDateTimeLong(apiKey.created)}
                      </span>
                    </div>
                  </div>

                  {/* Right: Actions */}
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="icon" className="flex-shrink-0 text-muted-foreground hover:text-foreground">
                        <MoreHorizontal className="h-5 w-5" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuPortal container={typeof document !== 'undefined' ? document.getElementById('devtools-portal') as any : undefined}>
                      <DropdownMenuContent align="end" className="devtools-theme dark bg-popover text-foreground border-border">
                        <DropdownMenuItem
                          onClick={() => copyToClipboard(apiKey.key)}
                          className="text-foreground focus:bg-primary/20 focus:text-foreground"
                        >
                          <Copy className="h-4 w-4 mr-2" />
                          Copy API Key
                        </DropdownMenuItem>
                        <DropdownMenuSeparator className="bg-border" />
                        <DropdownMenuItem
                          onClick={() => openDeleteDialog(apiKey.key)}
                          className="text-red-400 focus:bg-red-500/20 focus:text-red-400"
                        >
                          <Trash2 className="h-4 w-4 mr-2" />
                          Delete Key
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenuPortal>
                  </DropdownMenu>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Delete Confirmation Dialog */}
      <Dialog open={isDeleteOpen} onOpenChange={setIsDeleteOpen}>
        <DialogPortal container={typeof document !== 'undefined' ? document.getElementById('devtools-portal') as any : undefined}>
          <DialogContent className="devtools-theme dark max-w-sm mx-2 sm:mx-auto bg-popover border-border text-foreground">
            <DialogHeader className="bg-popover border-b border-border px-4 py-3 text-foreground">
              <DialogTitle className="text-foreground">Delete API Key</DialogTitle>
              <DialogDescription className="text-muted-foreground">
                This action cannot be undone. Enter your password to confirm.
              </DialogDescription>
            </DialogHeader>
            <div className="p-4 space-y-4">
              <div className="space-y-2">
                <Label htmlFor="delete-password" className="text-muted-foreground text-xs font-medium">PASSWORD</Label>
                <Input
                  id="delete-password"
                  type="password"
                  value={deletePassword}
                  onChange={(e) => setDeletePassword(e.target.value)}
                  placeholder="Enter your account password"
                  className="bg-input border-border text-foreground placeholder:text-muted-foreground"
                  onKeyDown={(e) => e.key === 'Enter' && handleDeleteConfirm()}
                />
              </div>
              <div className="flex justify-end space-x-2">
                <Button
                  variant="outline"
                  onClick={() => setIsDeleteOpen(false)}
                  className="!text-foreground !bg-card !border-border hover:!bg-primary/10 hover:!text-primary"
                >
                  Cancel
                </Button>
                <Button
                  variant="destructive"
                  onClick={handleDeleteConfirm}
                  disabled={!deletePassword || deleteAPIKey.isLoading}
                >
                  {deleteAPIKey.isLoading ? "Deleting..." : "Delete Key"}
                </Button>
              </div>
            </div>
          </DialogContent>
        </DialogPortal>
      </Dialog>
    </div>
  );
}
