"use client";
import React, { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@karrio/ui/components/ui/dialog";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Separator } from "@karrio/ui/components/ui/separator";
import { Search, Clock, Link, Zap, FileText, Plus } from "lucide-react";
import {
  useWorkflowTemplates,
  PREDEFINED_WORKFLOW_TEMPLATES,
  WorkflowTemplateType
} from "@karrio/hooks/workflow-templates";
import { AutomationTriggerType } from "@karrio/types/graphql/ee";

interface WorkflowTemplatePickerProps {
  onSelectTemplate: (template: any) => void;
  children: React.ReactNode;
}

export function WorkflowTemplatePicker({ onSelectTemplate, children }: WorkflowTemplatePickerProps) {
  const [open, setOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const { data: serverTemplates, isLoading } = useWorkflowTemplates();

  // Combine server templates with predefined templates
  const allTemplates = [
    ...PREDEFINED_WORKFLOW_TEMPLATES,
    ...(serverTemplates?.workflow_templates?.edges?.map(edge => edge.node) || [])
  ];

  // Filter templates based on search query
  const filteredTemplates = allTemplates.filter(template =>
    template.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    template.description?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleSelectTemplate = (template: any) => {
    onSelectTemplate(template);
    setOpen(false);
  };

  const getTriggerIcon = (triggerType: string) => {
    switch (triggerType) {
      case AutomationTriggerType.scheduled:
        return <Clock className="h-4 w-4" />;
      case AutomationTriggerType.webhook:
        return <Link className="h-4 w-4" />;
      case AutomationTriggerType.manual:
        return <Zap className="h-4 w-4" />;
      default:
        return <Zap className="h-4 w-4" />;
    }
  };

  const getTriggerLabel = (triggerType: string) => {
    switch (triggerType) {
      case AutomationTriggerType.scheduled:
        return "Scheduled";
      case AutomationTriggerType.webhook:
        return "Webhook";
      case AutomationTriggerType.manual:
        return "Manual";
      default:
        return "Manual";
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        {children}
      </DialogTrigger>
      <DialogContent className="max-w-full sm:max-w-4xl h-[90vh] sm:h-[80vh] flex flex-col mx-2 sm:mx-auto">
        <DialogHeader className="p-3 sm:p-4 pb-2">
          <DialogTitle className="flex items-center gap-2 text-base">
            <FileText className="h-4 w-4" />
            Choose a Workflow Template
          </DialogTitle>
        </DialogHeader>

        {/* Search Bar */}
        <div className="relative p-3 sm:p-4 pb-8">
          <Search className="absolute left-6 sm:left-7 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            placeholder="Search templates..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 h-9 sm:h-8 text-sm"
          />
        </div>

        {/* Templates Grid */}
        <div className="flex-1 overflow-y-auto p-4 pb-8">
          {isLoading ? (
            <div className="flex items-center justify-center h-32">
              <div className="text-sm text-gray-500">Loading templates...</div>
            </div>
          ) : filteredTemplates.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-32 space-y-2">
              <FileText className="h-8 w-8 text-gray-400" />
              <div className="text-sm text-gray-500">No templates found</div>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 px-3 sm:px-4 pb-4">
              {filteredTemplates.map((template, index) => (
                <Card
                  key={template.slug || `template-${index}`}
                  className="cursor-pointer hover:shadow-md transition-shadow border-slate-200"
                  onClick={() => handleSelectTemplate(template)}
                >
                  <CardHeader className="pb-2 p-3">
                    <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-2">
                      <div className="flex-1 min-w-0">
                        <CardTitle className="text-sm font-semibold text-slate-900 truncate">
                          {template.name}
                        </CardTitle>
                        <CardDescription className="text-xs text-slate-600 mt-1 line-clamp-2">
                          {template.description}
                        </CardDescription>
                      </div>
                      <Badge variant="outline" className="flex items-center gap-1 text-xs flex-shrink-0">
                        {getTriggerIcon(template.trigger?.trigger_type)}
                        <span className="hidden sm:inline">{getTriggerLabel(template.trigger?.trigger_type)}</span>
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent className="p-3">
                    <Separator className="mb-3" />
                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-slate-600">Actions:</span>
                        <code className="font-medium text-slate-900">
                          {template.actions?.length || 0}
                        </code>
                      </div>
                      {template.trigger?.schedule && (
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between text-sm gap-1">
                          <span className="text-slate-600">Schedule:</span>
                          <code className="text-xs bg-slate-100 px-2 py-1 rounded break-all">
                            {template.trigger.schedule}
                          </code>
                        </div>
                      )}
                      {template.actions && template.actions.length > 0 && (
                        <div className="mt-3">
                          <div className="text-xs text-slate-500 mb-2">Actions included:</div>
                          <div className="flex flex-wrap gap-1">
                            {template.actions.slice(0, 2).map((action: any, actionIndex: number) => (
                              <Badge
                                key={action.slug || `action-${actionIndex}`}
                                variant="secondary"
                                className="text-xs truncate max-w-full"
                              >
                                {action.name}
                              </Badge>
                            ))}
                            {template.actions.length > 2 && (
                              <Badge variant="secondary" className="text-xs">
                                +{template.actions.length - 2}
                              </Badge>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>

        {/* Start from Scratch Option */}
        <div className="border-t pt-3 p-3 sm:p-4 pb-3 sm:pb-4">
          <Card
            className="cursor-pointer hover:shadow-md transition-shadow border-dashed border-slate-300"
            onClick={() => handleSelectTemplate(null)}
          >
            <CardContent className="flex items-center justify-center py-3 sm:py-4 px-3">
              <div className="flex items-center gap-2 text-slate-600">
                <Plus className="h-4 w-4" />
                <span className="text-sm font-medium">Start from scratch</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </DialogContent>
    </Dialog>
  );
}
