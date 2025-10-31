"use client";

import React, { useState } from "react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger, DialogPortal } from "@karrio/ui/components/ui/dialog";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger, DropdownMenuPortal } from "@karrio/ui/components/ui/dropdown-menu";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@karrio/ui/components/ui/tooltip";
import { Trash2, Plus, Copy, Settings, Eye, EyeOff, CheckCircle, XCircle, MoreHorizontal } from "lucide-react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@karrio/ui/components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { ConfirmationDialog } from "@karrio/ui/components/confirmation-dialog";
import { useWebhooks, useWebhookMutation } from "@karrio/hooks/webhook";
import { useNotifier } from "@karrio/ui/core/components/notifier";
import { Checkbox } from "@karrio/ui/components/ui/checkbox";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Badge } from "@karrio/ui/components/ui/badge";
import { formatDateTimeLong } from "@karrio/lib";
import { NotificationType } from "@karrio/types";
import { EventTypes } from "@karrio/types";

interface CreateWebhookFormData {
  url: string;
  description: string;
  enabled_events: EventTypes[];
  disabled: boolean;
  secret: string;
}

export function WebhooksView() {
  const notifier = useNotifier();
  const { query } = useWebhooks();
  const { createWebhook, updateWebhook, deleteWebhook } = useWebhookMutation();
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [editingWebhook, setEditingWebhook] = useState<any>(null);
  const [showSecrets, setShowSecrets] = useState<Record<string, boolean>>({});
  const [formData, setFormData] = useState<CreateWebhookFormData>({
    url: "",
    description: "",
    enabled_events: [],
    disabled: false,
    secret: "",
  });

  const webhooks = query.data?.webhooks?.edges?.map(edge => edge.node) || [];

  const handleCreateSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createWebhook.mutateAsync(formData);
      notifier.notify({
        type: NotificationType.success,
        message: "Webhook created successfully"
      });
      setIsCreateOpen(false);
      setFormData({
        url: "",
        description: "",
        enabled_events: [],
        disabled: false,
        secret: "",
      });
      query.refetch();
    } catch (error: any) {
      notifier.notify({
        type: NotificationType.error,
        message: error?.message || "Failed to create webhook"
      });
    }
  };

  const handleUpdateSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingWebhook) return;

    try {
      await updateWebhook.mutateAsync({
        id: editingWebhook.id,
        ...formData
      });
      notifier.notify({
        type: NotificationType.success,
        message: "Webhook updated successfully"
      });
      setEditingWebhook(null);
      query.refetch();
    } catch (error: any) {
      notifier.notify({
        type: NotificationType.error,
        message: error?.message || "Failed to update webhook"
      });
    }
  };

  const [confirmOpen, setConfirmOpen] = useState(false);
  const [pendingDelete, setPendingDelete] = useState<any>(null);
  const askDelete = (webhook: any) => { setPendingDelete(webhook); setConfirmOpen(true); };
  const handleDeleteConfirmed = async () => {
    if (!pendingDelete) return;
    try {
      await deleteWebhook.mutateAsync({ id: pendingDelete.id });
      notifier.notify({ type: NotificationType.success, message: "Webhook deleted successfully" });
      query.refetch();
    } catch (error: any) {
      notifier.notify({ type: NotificationType.error, message: error?.message || "Failed to delete webhook" });
    } finally {
      setPendingDelete(null);
    }
  };

  const handleEdit = (webhook: any) => {
    setEditingWebhook(webhook);
    setFormData({
      url: webhook.url || "",
      description: webhook.description || "",
      enabled_events: webhook.enabled_events || [],
      disabled: webhook.disabled || false,
      secret: webhook.secret || "",
    });
  };

  const toggleSecret = (webhookId: string) => {
    setShowSecrets(prev => ({
      ...prev,
      [webhookId]: !prev[webhookId]
    }));
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    notifier.notify({
      type: NotificationType.success,
      message: "Copied to clipboard"
    });
  };

  const getStatusIcon = (webhook: any) => {
    if (webhook.disabled) {
      return <XCircle className="h-4 w-4 text-red-600" />;
    }
    return <CheckCircle className="h-4 w-4 text-green-600" />;
  };

  const eventTypeOptions = [
    { value: EventTypes.order_created, label: "Order Created" },
    { value: EventTypes.order_updated, label: "Order Updated" },
    { value: EventTypes.order_fulfilled, label: "Order Fulfilled" },
    { value: EventTypes.order_cancelled, label: "Order Cancelled" },
    { value: EventTypes.shipment_purchased, label: "Shipment Purchased" },
    { value: EventTypes.shipment_cancelled, label: "Shipment Cancelled" },
    { value: EventTypes.shipment_fulfilled, label: "Shipment Fulfilled" },
    { value: EventTypes.tracker_created, label: "Tracker Created" },
    { value: EventTypes.tracker_updated, label: "Tracker Updated" },
  ];

  return (
    <div className="h-full flex flex-col bg-background">
      <div className="px-4 py-3 border-b border-border">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-lg font-semibold text-foreground">Webhooks</h2>
            <p className="text-sm text-muted-foreground mt-1">
              Manage webhook endpoints and event subscriptions
            </p>
          </div>
          <Dialog open={isCreateOpen} onOpenChange={setIsCreateOpen}>
            <DialogTrigger asChild>
              <Button size="sm">
                <Plus className="h-4 w-4 mr-2" />
                Create Webhook
              </Button>
            </DialogTrigger>
            <DialogPortal container={typeof document !== 'undefined' ? document.getElementById('devtools-portal') as any : undefined}>
              <DialogContent className="devtools-theme dark bg-popover border-border text-foreground">
                <DialogHeader className="bg-popover border-b border-border px-4 py-3">
                  <DialogTitle className="text-foreground">Create New Webhook</DialogTitle>
                  <DialogDescription className="text-muted-foreground">
                    Add a new webhook endpoint to receive event notifications
                  </DialogDescription>
                </DialogHeader>
                <form onSubmit={handleCreateSubmit} className="space-y-4 p-4 pb-8">
                  <div>
                    <Label htmlFor="url" className="text-muted-foreground">Endpoint URL</Label>
                    <Input
                      id="url"
                      type="url"
                      placeholder="https://your-domain.com/webhook"
                      value={formData.url}
                      onChange={(e) => setFormData(prev => ({ ...prev, url: e.target.value }))}
                      required
                      className="bg-input border-border text-foreground placeholder:text-muted-foreground"
                    />
                  </div>
                  <div>
                    <Label htmlFor="description" className="text-muted-foreground">Description</Label>
                    <Input
                      id="description"
                      placeholder="Optional description"
                      value={formData.description}
                      onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                      className="bg-input border-border text-foreground placeholder:text-muted-foreground"
                    />
                  </div>
                  <div>
                    <Label className="text-muted-foreground">Events to Subscribe</Label>
                    <div className="grid grid-cols-2 gap-2 mt-2">
                      {eventTypeOptions.map((option) => (
                        <div key={option.value} className="flex items-center space-x-2">
                          <Checkbox
                            id={option.value}
                            checked={formData.enabled_events.includes(option.value)}
                            onCheckedChange={(checked) => {
                              if (checked) {
                                setFormData(prev => ({
                                  ...prev,
                                  enabled_events: [...prev.enabled_events, option.value]
                                }));
                              } else {
                                setFormData(prev => ({
                                  ...prev,
                                  enabled_events: prev.enabled_events.filter(e => e !== option.value)
                                }));
                              }
                            }}
                          />
                          <Label htmlFor={option.value} className="text-sm text-muted-foreground">
                            {option.label}
                          </Label>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div>
                    <Label htmlFor="secret" className="text-muted-foreground">Secret (Optional)</Label>
                    <Input
                      id="secret"
                      placeholder="Webhook secret for signature validation"
                      value={formData.secret}
                      onChange={(e) => setFormData(prev => ({ ...prev, secret: e.target.value }))}
                      className="bg-input border-border text-foreground placeholder:text-muted-foreground"
                    />
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="disabled"
                      checked={formData.disabled}
                      onCheckedChange={(checked) => setFormData(prev => ({ ...prev, disabled: !!checked }))}
                    />
                    <Label htmlFor="disabled" className="text-sm text-muted-foreground">
                      Create as disabled
                    </Label>
                  </div>
                  <div className="flex justify-end space-x-2">
                    <Button type="button" variant="outline" onClick={() => setIsCreateOpen(false)} className="!text-foreground !bg-card !border-border hover:!bg-primary/10 hover:!border-primary hover:!text-primary">
                      Cancel
                    </Button>
                    <Button type="submit" disabled={createWebhook.isLoading}>
                      {createWebhook.isLoading ? "Creating..." : "Create Webhook"}
                    </Button>
                  </div>
                </form>
              </DialogContent>
            </DialogPortal>
          </Dialog>
        </div>
      </div>

      <div className="flex-1 overflow-auto p-4">
        {query.isLoading ? (
          <div className="flex items-center justify-center h-full">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-400"></div>
          </div>
        ) : webhooks.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-muted-foreground mb-4">
              <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-foreground mb-2">No webhooks configured</h3>
            <p className="text-muted-foreground mb-4">Create your first webhook to start receiving event notifications.</p>
            <Button onClick={() => setIsCreateOpen(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Create Webhook
            </Button>
          </div>
        ) : (
          <div className="border-b border-border overflow-x-auto sm:overflow-x-visible" style={{ touchAction: 'pan-x', WebkitOverflowScrolling: 'touch', overscrollBehaviorX: 'contain' }}>
            <div className="inline-block w-full min-w-[900px] sm:min-w-0 align-top">
              <Table className="w-full table-auto">
                <TableHeader>
                  <TableRow>
                    <TableHead className="text-foreground">Endpoint</TableHead>
                    <TableHead className="text-foreground">Status</TableHead>
                    <TableHead className="text-foreground">Events</TableHead>
                    <TableHead className="text-foreground">Created</TableHead>
                    <TableHead className="w-12 text-foreground"></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {webhooks.map((webhook) => (
                    <TableRow key={webhook.id}>
                      <TableCell className="font-medium">
                        <div className="space-y-1">
                          <div className="flex items-center gap-2">
                            {getStatusIcon(webhook)}
                            <span className="truncate text-sm text-foreground">{webhook.url}</span>
                          </div>
                          {webhook.description && (
                            <p className="text-xs text-muted-foreground truncate">
                              {webhook.description}
                            </p>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge variant={webhook.disabled ? "destructive" : "default"}>
                          {webhook.disabled ? "Disabled" : "Active"}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="max-w-md">
                          {webhook.enabled_events && webhook.enabled_events.length > 0 ? (
                            <div className="flex flex-wrap gap-1">
                              {webhook.enabled_events.slice(0, 2).map((event: EventTypes) => (
                                <Badge key={event} variant="secondary" className="text-xs">
                                  {event}
                                </Badge>
                              ))}
                              {webhook.enabled_events.length > 2 && (
                                <>
                                  <div className="hidden sm:block">
                                    <TooltipProvider>
                                      <Tooltip>
                                        <TooltipTrigger asChild>
                                          <Badge variant="secondary" className="text-xs cursor-default">
                                            +{webhook.enabled_events.length - 2}
                                          </Badge>
                                        </TooltipTrigger>
                                        <TooltipContent side="bottom" sideOffset={6} className="devtools-theme dark bg-popover text-foreground border border-border">
                                          <div className="max-w-xs text-xs space-y-1">
                                            {webhook.enabled_events.slice(2).map((event: EventTypes) => (
                                              <div key={event}>{event}</div>
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
                                          +{webhook.enabled_events.length - 2}
                                        </Button>
                                      </DropdownMenuTrigger>
                                      <DropdownMenuPortal container={typeof document !== 'undefined' ? document.getElementById('devtools-portal') as any : undefined}>
                                        <DropdownMenuContent side="bottom" align="start" className="devtools-theme dark bg-popover text-foreground border border-border">
                                          <div className="max-w-xs text-xs space-y-1 px-2 py-1">
                                            {webhook.enabled_events.slice(2).map((event: EventTypes) => (
                                              <div key={event}>{event}</div>
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
                            <span className="text-xs text-muted-foreground">No events</span>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="text-sm text-muted-foreground">
                          {formatDateTimeLong(webhook.created_at)}
                        </div>
                      </TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="icon" className="h-8 w-8 p-0 text-muted-foreground">
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuPortal container={typeof document !== 'undefined' ? document.getElementById('devtools-portal') as any : undefined}>
                            <DropdownMenuContent align="end" className="devtools-theme dark bg-popover text-foreground border-border">
                              <DropdownMenuItem onClick={() => handleEdit(webhook)} className="text-foreground focus:bg-primary/20 focus:text-foreground">
                                <Settings className="h-4 w-4 mr-2" />
                                Configure
                              </DropdownMenuItem>
                              {webhook.secret && (
                                <DropdownMenuItem onClick={() => copyToClipboard(webhook.secret || "")} className="text-foreground focus:bg-primary/20 focus:text-foreground">
                                  <Copy className="h-4 w-4 mr-2" />
                                  Copy Secret
                                </DropdownMenuItem>
                              )}
                              <DropdownMenuItem onClick={() => copyToClipboard(webhook.url || "")} className="text-foreground focus:bg-primary/20 focus:text-foreground">
                                <Copy className="h-4 w-4 mr-2" />
                                Copy URL
                              </DropdownMenuItem>
                              <DropdownMenuItem
                                onClick={() => handleDeleteConfirmed()}
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

      {/* Edit Webhook Dialog */}
      <Dialog open={!!editingWebhook} onOpenChange={() => setEditingWebhook(null)}>
        <DialogPortal container={typeof document !== 'undefined' ? document.getElementById('devtools-portal') as any : undefined}>
          <DialogContent className="devtools-theme dark bg-popover border-border text-foreground">
            <DialogHeader className="bg-popover border-b border-border px-4 py-3">
              <DialogTitle className="text-foreground">Edit Webhook</DialogTitle>
              <DialogDescription className="text-muted-foreground">
                Update webhook endpoint configuration
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleUpdateSubmit} className="space-y-4 p-4 pb-8">
              <div>
                <Label htmlFor="edit-url" className="text-muted-foreground">Endpoint URL</Label>
                <Input
                  id="edit-url"
                  type="url"
                  value={formData.url}
                  onChange={(e) => setFormData(prev => ({ ...prev, url: e.target.value }))}
                  required
                  className="bg-input border-border text-foreground placeholder:text-muted-foreground"
                />
              </div>
              <div>
                <Label htmlFor="edit-description" className="text-muted-foreground">Description</Label>
                <Input
                  id="edit-description"
                  value={formData.description}
                  onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                  className="bg-input border-border text-foreground placeholder:text-muted-foreground"
                />
              </div>
              <div>
                <Label className="text-muted-foreground">Events to Subscribe</Label>
                <div className="grid grid-cols-2 gap-2 mt-2">
                  {eventTypeOptions.map((option) => (
                    <div key={option.value} className="flex items-center space-x-2">
                      <Checkbox
                        id={`edit-${option.value}`}
                        checked={formData.enabled_events.includes(option.value)}
                        onCheckedChange={(checked) => {
                          if (checked) {
                            setFormData(prev => ({
                              ...prev,
                              enabled_events: [...prev.enabled_events, option.value]
                            }));
                          } else {
                            setFormData(prev => ({
                              ...prev,
                              enabled_events: prev.enabled_events.filter(e => e !== option.value)
                            }));
                          }
                        }}
                      />
                      <Label htmlFor={`edit-${option.value}`} className="text-sm text-muted-foreground">
                        {option.label}
                      </Label>
                    </div>
                  ))}
                </div>
              </div>
              <div>
                <Label htmlFor="edit-secret" className="text-muted-foreground">Secret</Label>
                <Input
                  id="edit-secret"
                  value={formData.secret}
                  onChange={(e) => setFormData(prev => ({ ...prev, secret: e.target.value }))}
                  className="bg-input border-border text-foreground placeholder:text-muted-foreground"
                />
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="edit-disabled"
                  checked={formData.disabled}
                  onCheckedChange={(checked) => setFormData(prev => ({ ...prev, disabled: !!checked }))}
                />
                <Label htmlFor="edit-disabled" className="text-sm text-muted-foreground">
                  Disabled
                </Label>
              </div>
              <div className="flex justify-end space-x-2">
                <Button type="button" variant="outline" onClick={() => setEditingWebhook(null)} className="!text-foreground !bg-card !border-border hover:!bg-primary/10 hover:!border-primary hover:!text-primary">
                  Cancel
                </Button>
                <Button type="submit" disabled={updateWebhook.isLoading}>
                  {updateWebhook.isLoading ? "Updating..." : "Update Webhook"}
                </Button>
              </div>
            </form>
          </DialogContent>
        </DialogPortal>
      </Dialog>
    </div>
  );
}
