"use client";
import React, { useState, useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Button } from "@karrio/ui/components/ui/button";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Switch } from "@karrio/ui/components/ui/switch";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@karrio/ui/components/ui/select";
import { CheckCircle2, Clock, AlertTriangle, Zap, Bell, Save, RotateCcw } from "lucide-react";
import { Separator } from "@karrio/ui/components/ui/separator";
import { Textarea } from "@karrio/ui/components/ui/textarea";
import type { AppConfigurationContext } from "../../types";

export default function ShippingTasksConfiguration({
  app,
  context,
  karrio,
  onConfigChange,
  onSave,
  onCancel,
}: AppConfigurationContext) {
  // Initialize state from current configuration
  const [config, setConfig] = useState({
    default_priority: app.installation?.metafields?.find(m => m.key === 'default_priority')?.value || 'medium',
    task_categories: app.installation?.metafields?.find(m => m.key === 'task_categories')?.value || 'Pickup, Delivery, Documentation, Customer Service',
    auto_archive_days: parseInt(app.installation?.metafields?.find(m => m.key === 'auto_archive_days')?.value) || 30,
    enable_notifications: app.installation?.metafields?.find(m => m.key === 'enable_notifications')?.value === 'true' || true,
    daily_task_limit: parseInt(app.installation?.metafields?.find(m => m.key === 'daily_task_limit')?.value) || 10,
    workspace_name: app.installation?.metafields?.find(m => m.key === 'workspace_name')?.value || '',
  });

  const [isLoading, setIsLoading] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);

  // Priority options with icons and descriptions
  const priorityOptions = [
    { value: 'low', label: 'Low Priority', icon: '🟢', description: 'Non-urgent tasks' },
    { value: 'medium', label: 'Medium Priority', icon: '🟡', description: 'Standard tasks' },
    { value: 'high', label: 'High Priority', icon: '🟠', description: 'Important tasks' },
    { value: 'urgent', label: 'Urgent', icon: '🔴', description: 'Critical tasks' },
  ];

  // Track changes to enable/disable save button
  useEffect(() => {
    const currentConfig = {
      default_priority: app.installation?.metafields?.find(m => m.key === 'default_priority')?.value || 'medium',
      task_categories: app.installation?.metafields?.find(m => m.key === 'task_categories')?.value || 'Pickup, Delivery, Documentation, Customer Service',
      auto_archive_days: parseInt(app.installation?.metafields?.find(m => m.key === 'auto_archive_days')?.value) || 30,
      enable_notifications: app.installation?.metafields?.find(m => m.key === 'enable_notifications')?.value === 'true' || true,
      daily_task_limit: parseInt(app.installation?.metafields?.find(m => m.key === 'daily_task_limit')?.value) || 10,
      workspace_name: app.installation?.metafields?.find(m => m.key === 'workspace_name')?.value || '',
    };

    const hasChanged = JSON.stringify(config) !== JSON.stringify(currentConfig);
    setHasChanges(hasChanged);
  }, [config, app.installation?.metafields]);

  const handleConfigChange = (key: string, value: any) => {
    setConfig(prev => ({
      ...prev,
      [key]: value
    }));
    onConfigChange(key, value);
  };

  const handleSave = async () => {
    setIsLoading(true);
    try {
      // Convert boolean to string for backend compatibility
      const configToSave = {
        ...config,
        enable_notifications: config.enable_notifications.toString(),
        auto_archive_days: config.auto_archive_days.toString(),
        daily_task_limit: config.daily_task_limit.toString(),
      };

      // Update all config values
      Object.entries(configToSave).forEach(([key, value]) => {
        onConfigChange(key, value);
      });

      await onSave();
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    const originalConfig = {
      default_priority: app.installation?.metafields?.find(m => m.key === 'default_priority')?.value || 'medium',
      task_categories: app.installation?.metafields?.find(m => m.key === 'task_categories')?.value || 'Pickup, Delivery, Documentation, Customer Service',
      auto_archive_days: parseInt(app.installation?.metafields?.find(m => m.key === 'auto_archive_days')?.value) || 30,
      enable_notifications: app.installation?.metafields?.find(m => m.key === 'enable_notifications')?.value === 'true' || true,
      daily_task_limit: parseInt(app.installation?.metafields?.find(m => m.key === 'daily_task_limit')?.value) || 10,
      workspace_name: app.installation?.metafields?.find(m => m.key === 'workspace_name')?.value || '',
    };
    setConfig(originalConfig);
  };

  // Parse categories for display
  const categories = config.task_categories.split(',').map(c => c.trim()).filter(Boolean);

  return (
    <div className="flex flex-col h-full relative">
      {/* Scrollable Content */}
      <div className="grid gap-6 pb-32 p-4">
        {/* Workspace Settings */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Zap className="h-5 w-5" />
              Workspace Settings
            </CardTitle>
            <CardDescription>
              Personalize your task workspace
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="workspace_name">Workspace Display Name</Label>
              <Input
                id="workspace_name"
                value={config.workspace_name}
                onChange={(e) => handleConfigChange('workspace_name', e.target.value)}
                placeholder={`${context.user?.name || 'My'} Shipping Workspace`}
              />
              <p className="text-xs text-muted-foreground">
                Custom name to display in the task list header
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Task Behavior */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5" />
              Task Behavior
            </CardTitle>
            <CardDescription>
              Configure how tasks are created and prioritized
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Default Priority */}
            <div className="space-y-3">
              <Label>Default Task Priority</Label>
              <Select
                value={config.default_priority}
                onValueChange={(value) => handleConfigChange('default_priority', value)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {priorityOptions.map((option) => (
                    <SelectItem key={option.value} value={option.value}>
                      <div className="flex items-center gap-2">
                        <span>{option.icon}</span>
                        <div>
                          <div className="font-medium">{option.label}</div>
                          <div className="text-xs text-muted-foreground">{option.description}</div>
                        </div>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-xs text-muted-foreground">
                Choose the default priority level for new tasks
              </p>
            </div>

            <Separator />

            {/* Daily Task Limit */}
            <div className="space-y-2">
              <Label htmlFor="daily_task_limit">Daily Task Limit</Label>
              <div className="flex items-center gap-4">
                <Input
                  id="daily_task_limit"
                  type="number"
                  min={1}
                  max={50}
                  value={config.daily_task_limit}
                  onChange={(e) => handleConfigChange('daily_task_limit', parseInt(e.target.value) || 10)}
                  className="w-20"
                />
                <span className="text-sm text-muted-foreground">tasks per day</span>
              </div>
              <p className="text-xs text-muted-foreground">
                Maximum number of tasks to show per day (helps maintain focus)
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Categories */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5" />
              Task Categories
            </CardTitle>
            <CardDescription>
              Define custom categories to organize your tasks
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="task_categories">Categories (comma-separated)</Label>
              <Textarea
                id="task_categories"
                value={config.task_categories}
                onChange={(e) => handleConfigChange('task_categories', e.target.value)}
                placeholder="Pickup, Delivery, Documentation, Customer Service"
                rows={3}
                className="resize-none"
              />
              <p className="text-xs text-muted-foreground">
                Separate categories with commas. These will appear as options when creating tasks.
              </p>
            </div>

            {/* Category Preview */}
            {categories.length > 0 && (
              <div className="space-y-2">
                <Label className="text-sm">Category Preview:</Label>
                <div className="flex flex-wrap gap-2">
                  {categories.map((category, index) => (
                    <Badge key={index} variant="secondary" className="text-xs">
                      {category}
                    </Badge>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Automation */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="h-5 w-5" />
              Automation
            </CardTitle>
            <CardDescription>
              Configure automatic task management features
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Auto Archive */}
            <div className="space-y-2">
              <Label htmlFor="auto_archive_days">Auto-Archive Completed Tasks</Label>
              <div className="flex items-center gap-4">
                <Input
                  id="auto_archive_days"
                  type="number"
                  min={0}
                  max={365}
                  value={config.auto_archive_days}
                  onChange={(e) => handleConfigChange('auto_archive_days', parseInt(e.target.value) || 0)}
                  className="w-20"
                />
                <span className="text-sm text-muted-foreground">days (0 to disable)</span>
              </div>
              <p className="text-xs text-muted-foreground">
                Automatically archive completed tasks after this many days
              </p>
            </div>

            <Separator />

            {/* Notifications */}
            <div className="flex items-center justify-between p-4 border rounded-md">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <Bell className="h-4 w-4" />
                  <Label className="font-medium">Task Notifications</Label>
                </div>
                <p className="text-xs text-muted-foreground">
                  Show browser notifications for task reminders and updates
                </p>
              </div>
              <Switch
                checked={config.enable_notifications}
                onCheckedChange={(checked) => handleConfigChange('enable_notifications', checked)}
              />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Sticky Save Button - Floating at bottom of scrollable content */}
      <div className="sticky bottom-0 left-0 right-0 bg-white/95 backdrop-blur-sm border-t shadow-lg p-4 bg-background">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            {hasChanges ? (
              <>
                <div className="w-2 h-2 bg-orange-500 rounded-full animate-pulse"></div>
                Unsaved changes
              </>
            ) : (
              <>
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                All changes saved
              </>
            )}
          </div>
          <div className="flex items-center gap-3">
            {hasChanges && (
              <Button variant="outline" onClick={handleReset} disabled={isLoading}>
                <RotateCcw className="h-4 w-4 mr-2" />
                Reset
              </Button>
            )}
            <Button
              onClick={handleSave}
              disabled={!hasChanges || isLoading}
              className="min-w-[120px]"
            >
              <Save className="h-4 w-4 mr-2" />
              {isLoading ? 'Saving...' : 'Save Changes'}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
