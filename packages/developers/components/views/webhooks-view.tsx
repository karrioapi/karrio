"use client";

import React, { useState } from "react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@karrio/ui/components/ui/dialog";
import { Trash2, Plus, Copy, Settings, Eye, EyeOff, CheckCircle, XCircle } from "lucide-react";
import { useWebhooks, useWebhookMutation } from "@karrio/hooks/webhook";
import { Card, CardContent, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
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

  const handleDelete = async (webhook: any) => {
    if (!confirm("Are you sure you want to delete this webhook?")) return;

    try {
      await deleteWebhook.mutateAsync({ id: webhook.id });
      notifier.notify({
        type: NotificationType.success,
        message: "Webhook deleted successfully"
      });
      query.refetch();
    } catch (error: any) {
      notifier.notify({
        type: NotificationType.error,
        message: error?.message || "Failed to delete webhook"
      });
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
    <div className="h-full flex flex-col">
      <div className="px-4 py-3 border-b border-slate-200">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-lg font-semibold">Webhooks</h2>
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
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Create New Webhook</DialogTitle>
                <DialogDescription>
                  Add a new webhook endpoint to receive event notifications
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleCreateSubmit} className="space-y-4 p-4 pb-8">
                <div>
                  <Label htmlFor="url">Endpoint URL</Label>
                  <Input
                    id="url"
                    type="url"
                    placeholder="https://your-domain.com/webhook"
                    value={formData.url}
                    onChange={(e) => setFormData(prev => ({ ...prev, url: e.target.value }))}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="description">Description</Label>
                  <Input
                    id="description"
                    placeholder="Optional description"
                    value={formData.description}
                    onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                  />
                </div>
                <div>
                  <Label>Events to Subscribe</Label>
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
                        <Label htmlFor={option.value} className="text-sm">
                          {option.label}
                        </Label>
                      </div>
                    ))}
                  </div>
                </div>
                <div>
                  <Label htmlFor="secret">Secret (Optional)</Label>
                  <Input
                    id="secret"
                    placeholder="Webhook secret for signature validation"
                    value={formData.secret}
                    onChange={(e) => setFormData(prev => ({ ...prev, secret: e.target.value }))}
                  />
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="disabled"
                    checked={formData.disabled}
                    onCheckedChange={(checked) => setFormData(prev => ({ ...prev, disabled: !!checked }))}
                  />
                  <Label htmlFor="disabled" className="text-sm">
                    Create as disabled
                  </Label>
                </div>
                <div className="flex justify-end space-x-2">
                  <Button type="button" variant="outline" onClick={() => setIsCreateOpen(false)}>
                    Cancel
                  </Button>
                  <Button type="submit" disabled={createWebhook.isLoading}>
                    {createWebhook.isLoading ? "Creating..." : "Create Webhook"}
                  </Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      <div className="flex-1 overflow-auto p-4">
        {query.isLoading ? (
          <div className="flex items-center justify-center h-full">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-slate-900"></div>
          </div>
        ) : webhooks.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-slate-400 mb-4">
              <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-slate-900 mb-2">No webhooks configured</h3>
            <p className="text-slate-500 mb-4">Create your first webhook to start receiving event notifications.</p>
            <Button onClick={() => setIsCreateOpen(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Create Webhook
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {webhooks.map((webhook) => (
              <Card key={webhook.id} className="flex flex-col justify-between">
                <CardHeader>
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0">
                      <CardTitle className="text-base font-medium flex items-center gap-2">
                        {getStatusIcon(webhook)}
                        <span className="truncate" title={webhook.url || ''}>{webhook.url}</span>
                      </CardTitle>
                      {webhook.description && (
                        <p className="text-sm text-slate-600 pt-2 truncate" title={webhook.description}>
                          {webhook.description}
                        </p>
                      )}
                    </div>
                    <div className="flex items-center flex-shrink-0">
                      <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => handleEdit(webhook)}>
                        <Settings className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="icon" className="h-8 w-8 text-red-600 hover:text-red-700" onClick={() => handleDelete(webhook)}>
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="text-sm space-y-4 py-4">
                  <div>
                    <Badge variant={webhook.disabled ? "destructive" : "default"}>
                      {webhook.disabled ? "Disabled" : "Active"}
                    </Badge>
                  </div>
                  {webhook.secret && (
                    <div>
                      <Label className="text-xs text-slate-600">Secret</Label>
                      <div className="flex items-center gap-2 mt-1">
                        <code className="flex-1 text-sm bg-slate-100 px-2 py-1 rounded font-mono truncate">
                          {showSecrets[webhook.id] ? webhook.secret : "••••••••••••••••"}
                        </code>
                        <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => toggleSecret(webhook.id)}>
                          {showSecrets[webhook.id] ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                        </Button>
                        <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => copyToClipboard(webhook.secret || "")}>
                          <Copy className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  )}
                  {webhook.enabled_events && webhook.enabled_events.length > 0 && (
                    <div>
                      <Label className="text-xs text-slate-600">Subscribed Events</Label>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {webhook.enabled_events.slice(0, 3).map((event: EventTypes) => (
                          <Badge key={event} variant="secondary" className="text-xs font-normal">
                            {event}
                          </Badge>
                        ))}
                        {webhook.enabled_events.length > 3 && (
                          <Badge variant="secondary" className="text-xs font-normal">
                            +{webhook.enabled_events.length - 3} more
                          </Badge>
                        )}
                      </div>
                    </div>
                  )}
                </CardContent>
                <div className="text-xs text-slate-500 p-4 pt-3 border-t">
                  Created: {formatDateTimeLong(webhook.created_at)}
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Edit Webhook Dialog */}
      <Dialog open={!!editingWebhook} onOpenChange={() => setEditingWebhook(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Webhook</DialogTitle>
            <DialogDescription>
              Update webhook endpoint configuration
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleUpdateSubmit} className="space-y-4 p-4 pb-8">
            <div>
              <Label htmlFor="edit-url">Endpoint URL</Label>
              <Input
                id="edit-url"
                type="url"
                value={formData.url}
                onChange={(e) => setFormData(prev => ({ ...prev, url: e.target.value }))}
                required
              />
            </div>
            <div>
              <Label htmlFor="edit-description">Description</Label>
              <Input
                id="edit-description"
                value={formData.description}
                onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
              />
            </div>
            <div>
              <Label>Events to Subscribe</Label>
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
                    <Label htmlFor={`edit-${option.value}`} className="text-sm">
                      {option.label}
                    </Label>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <Label htmlFor="edit-secret">Secret</Label>
              <Input
                id="edit-secret"
                value={formData.secret}
                onChange={(e) => setFormData(prev => ({ ...prev, secret: e.target.value }))}
              />
            </div>
            <div className="flex items-center space-x-2">
              <Checkbox
                id="edit-disabled"
                checked={formData.disabled}
                onCheckedChange={(checked) => setFormData(prev => ({ ...prev, disabled: !!checked }))}
              />
              <Label htmlFor="edit-disabled" className="text-sm">
                Disabled
              </Label>
            </div>
            <div className="flex justify-end space-x-2">
              <Button type="button" variant="outline" onClick={() => setEditingWebhook(null)}>
                Cancel
              </Button>
              <Button type="submit" disabled={updateWebhook.isLoading}>
                {updateWebhook.isLoading ? "Updating..." : "Update Webhook"}
              </Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
