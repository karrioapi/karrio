"use client";
import React, { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@karrio/ui/components/ui/dialog";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Separator } from "@karrio/ui/components/ui/separator";
import { Search, Globe, Mail, MessageSquare, Database, Plus, Zap } from "lucide-react";
import {
  useWorkflowActionTemplates,
  PREDEFINED_ACTION_TEMPLATES
} from "@karrio/hooks/workflow-templates";
import { AutomationActionType } from "@karrio/types/graphql/ee";

interface ActionTemplatePickerProps {
  onSelectTemplate: (template: any) => void;
  children: React.ReactNode;
}

export function ActionTemplatePicker({ onSelectTemplate, children }: ActionTemplatePickerProps) {
  const [open, setOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const { data: serverTemplates, isLoading } = useWorkflowActionTemplates();

  // Combine server templates with predefined templates
  const allTemplates = [
    ...PREDEFINED_ACTION_TEMPLATES,
    ...(serverTemplates?.workflow_action_templates?.edges?.map(edge => edge.node) || [])
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

  const getActionIcon = (actionType: string) => {
    switch (actionType) {
      case AutomationActionType.http_request:
        return <Globe className="h-4 w-4" />;
      case AutomationActionType.data_mapping:
        return <Database className="h-4 w-4" />;
      default:
        return <Zap className="h-4 w-4" />;
    }
  };

  const getActionTypeLabel = (actionType: string) => {
    switch (actionType) {
      case AutomationActionType.http_request:
        return "HTTP Request";
      case AutomationActionType.data_mapping:
        return "Data Mapping";
      default:
        return "Action";
    }
  };

  const getTemplateIcon = (template: any) => {
    if (template.slug?.includes('slack')) return <MessageSquare className="h-5 w-5" />;
    if (template.slug?.includes('email')) return <Mail className="h-5 w-5" />;
    if (template.slug?.includes('database')) return <Database className="h-5 w-5" />;
    return <Globe className="h-5 w-5" />;
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        {children}
      </DialogTrigger>
      <DialogContent className="max-w-4xl h-[80vh] flex flex-col">
        <DialogHeader className="p-4 pb-2">
          <DialogTitle className="flex items-center gap-2 text-base">
            <Zap className="h-4 w-4" />
            Choose an Action Template
          </DialogTitle>
        </DialogHeader>

        {/* Search Bar */}
        <div className="relative p-4 pb-8">
          <Search className="absolute left-7 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            placeholder="Search action templates..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 h-8 text-sm"
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
              <Zap className="h-8 w-8 text-gray-400" />
              <div className="text-sm text-gray-500">No action templates found</div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 px-4 pb-4">
              {filteredTemplates.map((template, index) => (
                <Card
                  key={template.slug || `template-${index}`}
                  className="cursor-pointer hover:shadow-md transition-shadow border-slate-200"
                  onClick={() => handleSelectTemplate(template)}
                >
                  <CardHeader className="pb-2 p-3">
                    <div className="flex items-start justify-between">
                      <div className="flex items-center gap-2 flex-1">
                        {getTemplateIcon(template)}
                        <div>
                          <CardTitle className="text-xs font-semibold text-slate-900">
                            {template.name}
                          </CardTitle>
                          <CardDescription className="text-xs text-slate-600 mt-1">
                            {template.description}
                          </CardDescription>
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="pt-0 px-3 pb-3">
                    <Separator className="mb-3" />
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <Badge variant="outline" className="text-xs flex items-center gap-1">
                          {getActionIcon(template.action_type)}
                          {getActionTypeLabel(template.action_type)}
                        </Badge>
                      </div>
                      {template.method && (
                        <div className="flex items-center justify-between text-xs">
                          <span className="text-slate-600">Method:</span>
                          <code className="bg-slate-100 px-2 py-1 rounded text-xs">
                            {template.method?.toUpperCase()}
                          </code>
                        </div>
                      )}
                      {template.content_type && (
                        <div className="flex items-center justify-between text-xs">
                          <span className="text-slate-600">Content:</span>
                          <span className="text-slate-900 text-xs">
                            {template.content_type}
                          </span>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>

        {/* Custom Action Option */}
        <div className="border-t pt-3 p-4 pb-4">
          <Card
            className="cursor-pointer hover:shadow-md transition-shadow border-dashed border-slate-300"
            onClick={() => handleSelectTemplate(null)}
          >
            <CardContent className="flex items-center justify-center py-4 px-3">
              <div className="flex items-center gap-2 text-slate-600">
                <Plus className="h-4 w-4" />
                <span className="text-sm font-medium">Create custom action</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </DialogContent>
    </Dialog>
  );
}
