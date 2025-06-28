"use client";

import { useState, useRef, useCallback, useMemo } from "react";
import { useAPIToken, useAPITokenMutation } from "@karrio/hooks/api-token";
import { useAPIKeys, useAPIKeyMutation, APIKeyType } from "@karrio/hooks/api-keys";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { Button } from "@karrio/ui/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Separator } from "@karrio/ui/components/ui/separator";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@karrio/ui/components/ui/dialog";
import { useToast } from "@karrio/ui/hooks/use-toast";
import { Copy, Key, AlertTriangle, Shield, Calendar, Plus, Trash2, MoreHorizontal } from "lucide-react";
import { useUser } from "@karrio/hooks/user";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@karrio/ui/components/ui/dropdown-menu";
import { Checkbox } from "@karrio/ui/components/ui/checkbox";
import { formatDistanceToNow } from "date-fns";

// Permission descriptions mapping
const PERMISSION_DESCRIPTIONS: Record<string, { label: string; description: string }> = {
  manage_apps: { label: "Manage Apps", description: "Create, update, and delete applications" },
  manage_team: { label: "Manage Team", description: "Invite and manage team members" },
  manage_data: { label: "Manage Data", description: "Create, read, update, and delete data" },
  manage_carriers: { label: "Manage Carriers", description: "Configure carrier connections" },
  manage_orders: { label: "Manage Orders", description: "Create and manage orders" },
  manage_pickups: { label: "Manage Pickups", description: "Create and manage pickup requests" },
  manage_trackers: { label: "Manage Trackers", description: "Track and monitor shipments" },
  manage_shipments: { label: "Manage Shipments", description: "Create and manage shipments" },
  manage_webhooks: { label: "Manage Webhooks", description: "Configure webhook endpoints" },
  manage_org_owner: { label: "Manage Organization", description: "Full organization management" },
  manage_system: { label: "Manage System", description: "System-level configuration" },
};

type CreateFormData = {
  label: string;
  password: string;
  permissions: string[];
};

const DEFAULT_FORM_DATA: CreateFormData = {
  label: "",
  password: "",
  permissions: [],
};

export default function APIKeyPage() {
  const { toast } = useToast();
  const { references, metadata } = useAPIMetadata();
  const {
    query: { data: { token } = {}, ...query },
  } = useAPIToken();
  const { updateToken } = useAPITokenMutation();
  const { query: { data: { user } = {} } } = useUser();
  const { query: apiKeysQuery } = useAPIKeys();
  const apiKeyMutation = useAPIKeyMutation();

  // Form state with direct useState for better performance
  const [formData, setFormData] = useState<CreateFormData>(DEFAULT_FORM_DATA);
  const [isCreating, setIsCreating] = useState(false);

  const passwordRef = useRef<HTMLInputElement>(null);
  const deletePasswordRef = useRef<HTMLInputElement>(null);
  const tokenInputRef = useRef<HTMLInputElement>(null);
  const [isRevealed, setIsRevealed] = useState(false);
  const [showRegenerateDialog, setShowRegenerateDialog] = useState(false);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [selectedKeyForDelete, setSelectedKeyForDelete] = useState<APIKeyType | null>(null);
  const [isRegenerating, setIsRegenerating] = useState(false);

  const apiKeys = apiKeysQuery.data?.api_keys || [];

  const copyToClipboard = useCallback(async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      toast({
        title: "Copied",
        description: "API key copied to clipboard",
      });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to copy to clipboard",
      });
    }
  }, [toast]);

  const handleRegenerate = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    if (!passwordRef.current?.value || !token?.key) return;

    setIsRegenerating(true);
    try {
      await updateToken.mutateAsync({
        refresh: true,
        key: token.key,
        password: passwordRef.current.value
      });

      toast({
        title: "Success",
        description: "API key regenerated successfully",
      });

      setShowRegenerateDialog(false);
      setIsRevealed(false);
      if (passwordRef.current) passwordRef.current.value = "";
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to regenerate API key",
      });
    } finally {
      setIsRegenerating(false);
    }
  }, [updateToken, token?.key, toast]);

  const handleCreateApiKey = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.label || !formData.password) return;

    setIsCreating(true);
    try {
      const { create_api_key: { api_key, errors } } = await apiKeyMutation.createAPIKey.mutateAsync(formData);

      if (errors && errors.length > 0) {
        const errorMessages = errors.map(e => e.messages.join(", ")).join("; ");
        toast({
          variant: "destructive",
          title: "Error",
          description: errorMessages,
        });
      } else {
        toast({
          title: "Success",
          description: "API key created successfully!",
        });
        setShowCreateDialog(false);
        setFormData(DEFAULT_FORM_DATA);
        apiKeysQuery.refetch?.();
      }
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Error",
        description: error.message || "Failed to create API key",
      });
    } finally {
      setIsCreating(false);
    }
  }, [formData, apiKeyMutation, toast, apiKeysQuery]);

  const handleOpenCreateDialog = useCallback(() => {
    setFormData(DEFAULT_FORM_DATA);
    setShowCreateDialog(true);
  }, []);

  const handleDialogOpenChange = useCallback((open: boolean) => {
    if (!open) {
      setFormData(DEFAULT_FORM_DATA);
      setShowCreateDialog(false);
    }
  }, []);

  const handleCloseCreateDialog = useCallback(() => {
    setFormData(DEFAULT_FORM_DATA);
    setShowCreateDialog(false);
  }, []);

  const handleDeleteApiKey = useCallback(async () => {
    if (!selectedKeyForDelete || !deletePasswordRef.current?.value) return;

    try {
      const { delete_api_key: { errors } } = await apiKeyMutation.deleteAPIKey.mutateAsync({
        key: selectedKeyForDelete.key,
        password: deletePasswordRef.current.value
      });

      if (errors && errors.length > 0) {
        const errorMessages = errors.map(e => e.messages.join(", ")).join("; ");
        toast({
          variant: "destructive",
          title: "Error",
          description: errorMessages,
        });
      } else {
        toast({
          title: "Success",
          description: "API key deleted successfully!",
        });
        setShowDeleteDialog(false);
        setSelectedKeyForDelete(null);
        if (deletePasswordRef.current) deletePasswordRef.current.value = "";
        apiKeysQuery.refetch?.();
      }
    } catch (error: any) {
      toast({
        variant: "destructive",
        title: "Error",
        description: error.message || "Failed to delete API key",
      });
    }
  }, [selectedKeyForDelete, apiKeyMutation, toast, apiKeysQuery]);

  const maskKey = useCallback((key: string) => {
    if (!key || key.length <= 8) return "••••••••••••••••••••••••";
    return `${key.slice(0, 8)}${"•".repeat(16)}${key.slice(-8)}`;
  }, []);

  // Build available permissions based on user's permissions
  const availablePermissions = useMemo(() => {
    const userPermissions = user?.permissions || [];
    return userPermissions.map(permission => ({
      id: permission,
      label: PERMISSION_DESCRIPTIONS[permission]?.label || permission.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
      description: PERMISSION_DESCRIPTIONS[permission]?.description || `Manage ${permission.replace('manage_', '').replace(/_/g, ' ')}`
    }));
  }, [user?.permissions]);

  const formatPermissions = useCallback((permissions: string[]) => {
    if (!permissions || permissions.length === 0) return "No permissions";
    return permissions.map(p => {
      const perm = availablePermissions.find(ap => ap.id === p);
      return perm ? perm.label : (PERMISSION_DESCRIPTIONS[p]?.label || p);
    }).join(", ");
  }, [availablePermissions]);

  // Optimized form handlers
  const handleLabelChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, label: e.target.value }));
  }, []);

  const handlePasswordChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, password: e.target.value }));
  }, []);

  const handlePermissionChange = useCallback((permissionId: string, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      permissions: checked
        ? [...prev.permissions, permissionId]
        : prev.permissions.filter(p => p !== permissionId)
    }));
  }, []);

  return (
    <>
      <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
        <span className="title is-4">Developers</span>
        <div>
          <Button
            onClick={handleOpenCreateDialog}
            className="bg-blue-600 hover:bg-blue-700 text-white"
          >
            <Plus className="h-4 w-4 mr-2" />
            Create API Key
          </Button>
        </div>
      </header>

      <div className="tabs">
        <ul>
          <li className={`is-capitalized has-text-weight-semibold`}>
            <AppLink href="/developers" shallow={false} prefetch={false}>
              <span>Overview</span>
            </AppLink>
          </li>
          <li className={`is-capitalized has-text-weight-semibold is-active`}>
            <AppLink href="/developers/apikeys" shallow={false} prefetch={false}>
              <span>API Keys</span>
            </AppLink>
          </li>
          {metadata?.APPS_MANAGEMENT && (
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/developers/apps" shallow={false} prefetch={false}>
                <span>Apps</span>
              </AppLink>
            </li>
          )}
          <li className={`is-capitalized has-text-weight-semibold`}>
            <AppLink href="/developers/webhooks" shallow={false} prefetch={false}>
              <span>Webhooks</span>
            </AppLink>
          </li>
          <li className={`is-capitalized has-text-weight-semibold`}>
            <AppLink href="/developers/events" shallow={false} prefetch={false}>
              <span>Events</span>
            </AppLink>
          </li>
          <li className={`is-capitalized has-text-weight-semibold`}>
            <AppLink href="/developers/logs" shallow={false} prefetch={false}>
              <span>Logs</span>
            </AppLink>
          </li>
        </ul>
      </div>

      <div className="mt-6 space-y-4">
        {/* Security Notice */}
        <div className="rounded-lg border border-amber-200 bg-amber-50 p-4">
          <div className="flex items-start gap-3">
            <AlertTriangle className="h-5 w-5 text-amber-600 mt-0.5 flex-shrink-0" />
            <div>
              <h3 className="text-sm font-medium text-amber-800">Keep your API keys secure</h3>
              <p className="text-sm text-amber-700 mt-1">
                API keys provide access to your account data. Keep them secure and regenerate them if compromised.{" "}
                <a
                  href={`${references?.OPENAPI}/#section/Authentication`}
                  target="_blank"
                  rel="noreferrer"
                  className="underline hover:no-underline"
                >
                  Learn more
                </a>
              </p>
            </div>
          </div>
        </div>

        {/* API Keys List */}
        <div className="space-y-4">
          {apiKeysQuery.isLoading ? (
            <div className="text-center py-12 text-gray-500">
              <Key className="h-8 w-8 mx-auto mb-3 opacity-50" />
              <p>Loading API keys...</p>
            </div>
          ) : apiKeys.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <Key className="h-12 w-12 mx-auto mb-4 opacity-30" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No API keys yet</h3>
              <p className="text-gray-600 mb-6">Create your first API key to start using the Karrio API</p>
              <Button onClick={handleOpenCreateDialog} className="bg-blue-600 hover:bg-blue-700 text-white">
                <Plus className="h-4 w-4 mr-2" />
                Create your first API key
              </Button>
            </div>
          ) : (
            <div className="space-y-4">
              {apiKeys.map((apiKey) => (
                <div
                  key={apiKey.key}
                  className="rounded-lg border border-gray-200 bg-white p-6 transition-all duration-200 hover:border-gray-300 hover:shadow-sm"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="space-y-2">
                      <div className="flex items-center gap-3">
                        <h3 className="text-lg font-semibold text-gray-900">{apiKey.label}</h3>
                        {apiKey.test_mode && (
                          <Badge variant="secondary" className="bg-yellow-100 text-yellow-800 border-yellow-200">
                            Test Mode
                          </Badge>
                        )}
                      </div>
                      <div className="flex items-center gap-4 text-sm text-gray-600">
                        <div className="flex items-center gap-1">
                          <Calendar className="h-4 w-4" />
                          <span>Created {formatDistanceToNow(new Date(apiKey.created), { addSuffix: true })}</span>
                        </div>
                        <div className="flex items-center gap-1">
                          <Shield className="h-4 w-4" />
                          <span>{apiKey.permissions.length} permissions</span>
                        </div>
                      </div>
                      <p className="text-sm text-gray-500 max-w-2xl">
                        {formatPermissions(apiKey.permissions)}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => copyToClipboard(apiKey.key)}
                        className="text-gray-500 hover:text-gray-700"
                      >
                        <Copy className="h-4 w-4" />
                      </Button>
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="sm" className="text-gray-500 hover:text-gray-700">
                            <MoreHorizontal className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem
                            className="text-red-600 focus:text-red-600"
                            onClick={() => {
                              setSelectedKeyForDelete(apiKey);
                              setShowDeleteDialog(true);
                            }}
                          >
                            <Trash2 className="h-4 w-4 mr-2" />
                            Delete
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </div>
                  </div>

                  <div className="bg-gray-50 rounded-md p-3">
                    <div className="flex items-center justify-between mb-2">
                      <Label className="text-xs font-medium text-gray-700 uppercase tracking-wide">
                        Secret Key
                      </Label>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => copyToClipboard(apiKey.key)}
                        className="text-xs text-gray-500 hover:text-gray-700 h-auto p-1"
                      >
                        Click to copy
                      </Button>
                    </div>
                    <code className="text-sm font-mono text-gray-900 break-all">
                      {maskKey(apiKey.key)}
                    </code>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Regenerate Dialog */}
      <Dialog open={showRegenerateDialog} onOpenChange={setShowRegenerateDialog}>
        <DialogContent className="sm:max-w-md p-4 pb-8">
          <form onSubmit={handleRegenerate}>
            <DialogHeader>
              <DialogTitle>Regenerate API Key</DialogTitle>
              <DialogDescription>
                This will create a new API key and invalidate the current one. Any applications using the current key will need to be updated.
              </DialogDescription>
            </DialogHeader>

            <div className="space-y-4 py-4">
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                <div className="flex items-start gap-2">
                  <AlertTriangle className="h-4 w-4 text-yellow-600 mt-0.5" />
                  <div className="text-sm">
                    <p className="font-medium text-yellow-900">Warning</p>
                    <p className="text-yellow-800">
                      This action will disable your current API key and generate a new one.
                      Any webhook endpoints will remain active.
                    </p>
                  </div>
                </div>
              </div>

              <Separator />

              <div className="space-y-2">
                <Label htmlFor="confirm-email">Email</Label>
                <Input
                  id="confirm-email"
                  value={user?.email || ""}
                  disabled
                  className="bg-muted"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="confirm-password">Password</Label>
                <Input
                  id="confirm-password"
                  type="password"
                  placeholder="Enter your password to confirm"
                  ref={passwordRef}
                  required
                  disabled={isRegenerating}
                />
              </div>
            </div>

            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={() => setShowRegenerateDialog(false)}
                disabled={isRegenerating}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                variant="destructive"
                disabled={isRegenerating}
              >
                {isRegenerating ? "Regenerating..." : "Regenerate Key"}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Create API Key Dialog */}
      <Dialog open={showCreateDialog} onOpenChange={handleDialogOpenChange}>
        <DialogContent className="sm:max-w-2xl p-4 pb-8">
          <form onSubmit={handleCreateApiKey}>
            <DialogHeader>
              <DialogTitle>Create API Key</DialogTitle>
              <DialogDescription>
                Create a new API key with specific permissions to access your account.
              </DialogDescription>
            </DialogHeader>

            <div className="space-y-6 py-6">
              <div className="space-y-2">
                <Label htmlFor="key-name" className="text-sm font-medium">
                  Name <span className="text-red-500">*</span>
                </Label>
                <Input
                  id="key-name"
                  placeholder="e.g., Production API Key"
                  value={formData.label}
                  onChange={handleLabelChange}
                  required
                  className="w-full"
                />
                <p className="text-xs text-gray-500">
                  Choose a descriptive name to help you identify this key later
                </p>
              </div>

              <div className="space-y-4">
                <Label className="text-sm font-medium">Permissions</Label>
                <div className="space-y-3 max-h-64 overflow-y-auto border rounded-lg p-4">
                  {availablePermissions.map((permission) => (
                    <div key={permission.id} className="flex items-start space-x-3">
                      <Checkbox
                        id={permission.id}
                        checked={formData.permissions.includes(permission.id)}
                        onCheckedChange={(checked) => handlePermissionChange(permission.id, checked as boolean)}
                        className="mt-1"
                      />
                      <div className="grid gap-1 leading-none flex-1">
                        <label
                          htmlFor={permission.id}
                          className="text-sm font-medium leading-tight cursor-pointer"
                        >
                          {permission.label}
                        </label>
                        <p className="text-xs text-gray-500 leading-tight">
                          {permission.description}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
                <p className="text-xs text-gray-500">
                  Select the permissions this API key should have. You can always create a new key with different permissions.
                </p>
              </div>

              <Separator />

              <div className="space-y-2">
                <Label htmlFor="create-password" className="text-sm font-medium">
                  Confirm with password <span className="text-red-500">*</span>
                </Label>
                <Input
                  id="create-password"
                  type="password"
                  placeholder="Enter your password"
                  value={formData.password}
                  onChange={handlePasswordChange}
                  required
                  className="w-full"
                />
              </div>
            </div>

            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={handleCloseCreateDialog}
                disabled={isCreating}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                disabled={isCreating || !formData.label || !formData.password}
                className="bg-blue-600 hover:bg-blue-700"
              >
                {isCreating ? "Creating..." : "Create API Key"}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Delete API Key Dialog */}
      <Dialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <DialogContent className="sm:max-w-md p-4 pb-8">
          <DialogHeader>
            <DialogTitle>Delete API Key</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete "{selectedKeyForDelete?.label}"? This action cannot be undone.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 py-4">
            <div className="bg-red-50 border border-red-200 rounded-lg p-3">
              <div className="flex items-start gap-2">
                <AlertTriangle className="h-4 w-4 text-red-600 mt-0.5" />
                <div className="text-sm">
                  <p className="font-medium text-red-900">This action is irreversible</p>
                  <p className="text-red-800">
                    Any applications using this API key will immediately lose access.
                  </p>
                </div>
              </div>
            </div>

            <Separator />

            <div className="space-y-2">
              <Label htmlFor="delete-password">Confirm with password</Label>
              <Input
                id="delete-password"
                type="password"
                placeholder="Enter your password"
                ref={deletePasswordRef}
                required
              />
            </div>
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => setShowDeleteDialog(false)}
            >
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={handleDeleteApiKey}
            >
              Delete API Key
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <div className="p-6"></div>
    </>
  );
}
