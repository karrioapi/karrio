"use client";

import React, { useState } from "react";
import {
  AutomationActionType,
  AutomationHTTPContentType,
  AutomationHTTPMethod,
  AutomationParametersType,
  PartialWorkflowActionMutationInput,
} from "@karrio/types/graphql/ee";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@karrio/ui/components/ui/sheet";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Textarea } from "@karrio/ui/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@karrio/ui/components/ui/tabs";
import CodeMirror from "@uiw/react-codemirror";
import { jsonLanguage } from "@codemirror/lang-json";
import { htmlLanguage } from "@codemirror/lang-html";

interface ActionEditorProps {
  action: PartialWorkflowActionMutationInput;
  onSubmit: (data: PartialWorkflowActionMutationInput) => Promise<void>;
  trigger: React.ReactElement;
}

export function ActionModalEditor({ action, onSubmit, trigger }: ActionEditorProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [formData, setFormData] = useState<PartialWorkflowActionMutationInput>(action);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await onSubmit(formData);
      setIsOpen(false);
    } catch (error) {
      console.error("Failed to save action:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (field: keyof PartialWorkflowActionMutationInput, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const actionTypes = [
    { value: AutomationActionType.http_request, label: "HTTP Request" },
    { value: AutomationActionType.data_mapping, label: "Data Mapping" },
    { value: AutomationActionType.conditional, label: "Conditional" },
  ];

  const httpMethods = [
    { value: AutomationHTTPMethod.get, label: "GET" },
    { value: AutomationHTTPMethod.post, label: "POST" },
    { value: AutomationHTTPMethod.put, label: "PUT" },
    { value: AutomationHTTPMethod.patch, label: "PATCH" },
    { value: AutomationHTTPMethod.delete, label: "DELETE" },
  ];

  const contentTypes = [
    { value: AutomationHTTPContentType.json, label: "JSON" },
    { value: AutomationHTTPContentType.form, label: "Form Data" },
    { value: AutomationHTTPContentType.xml, label: "XML" },
    { value: AutomationHTTPContentType.text, label: "Text" },
  ];

  const parameterTypes = [
    { value: AutomationParametersType.data, label: "DATA" },
    { value: AutomationParametersType.querystring, label: "QUERYSTRING" },
  ];

  return (
    <Sheet open={isOpen} onOpenChange={setIsOpen}>
      <SheetTrigger asChild>{trigger}</SheetTrigger>
      <SheetContent className="w-[800px] min-w-[800px] sm:max-w-[800px] p-0 shadow-none">
        <div className="h-full flex flex-col">
          <SheetHeader className="sticky top-0 z-10 bg-white px-4 py-3 border-b">
            <SheetTitle className="text-lg font-semibold">Edit Action</SheetTitle>
            <p className="text-xs text-slate-600">Configure action settings and parameters for this workflow step.</p>
          </SheetHeader>

          <form onSubmit={handleSubmit} className="flex-1 overflow-y-auto">
            <div className="px-4 py-4 space-y-6 pb-32">

              {/* Basic Configuration */}
              <div className="space-y-4">
                <h3 className="text-sm font-semibold text-slate-900 mb-4">Basic Configuration</h3>
                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-3">
                    <div className="space-y-1">
                      <Label className="text-xs text-slate-700">Action Type *</Label>
                      <Select
                        value={formData.action_type || ""}
                        onValueChange={(value) => handleInputChange("action_type", value)}
                      >
                        <SelectTrigger className="h-8">
                          <SelectValue placeholder="Select action type" />
                        </SelectTrigger>
                        <SelectContent>
                          {actionTypes.map((type) => (
                            <SelectItem key={type.value} value={type.value}>
                              {type.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-1">
                      <Label className="text-xs text-slate-700">Name *</Label>
                      <Input
                        value={formData.name || ""}
                        onChange={(e) => handleInputChange("name", e.target.value)}
                        placeholder="e.g., Fetch FedEx Rates"
                        className="h-8"
                        required
                      />
                    </div>
                  </div>

                  <div className="space-y-1">
                    <Label className="text-xs text-slate-700">Description</Label>
                    <Textarea
                      value={formData.description || ""}
                      onChange={(e) => handleInputChange("description", e.target.value)}
                      placeholder="Describe what this action does..."
                      rows={2}
                      className="text-xs"
                    />
                  </div>
                </div>
              </div>

              {/* HTTP Request Configuration */}
              {formData.action_type === AutomationActionType.http_request && (
                <div className="space-y-4">
                  <h3 className="text-sm font-semibold text-slate-900 mb-4">HTTP Request Configuration</h3>

                  <Tabs defaultValue="general" className="w-full">
                    <TabsList className="grid w-full grid-cols-3 h-9">
                      <TabsTrigger value="general" className="text-sm">General</TabsTrigger>
                      <TabsTrigger value="headers" className="text-sm">Headers</TabsTrigger>
                      <TabsTrigger value="parameters" className="text-sm">Parameters</TabsTrigger>
                    </TabsList>

                    <TabsContent value="general" className="space-y-4 mt-4 p-4 border rounded-lg bg-slate-50">
                      <div className="grid grid-cols-2 gap-3">
                        <div className="space-y-1">
                          <Label className="text-xs text-slate-700">Host *</Label>
                          <Input
                            value={formData.host || ""}
                            onChange={(e) => handleInputChange("host", e.target.value)}
                            placeholder="example.com"
                            className="h-8"
                            required
                          />
                        </div>

                        <div className="space-y-1">
                          <Label className="text-xs text-slate-700">Endpoint</Label>
                          <Input
                            value={formData.endpoint || ""}
                            onChange={(e) => handleInputChange("endpoint", e.target.value)}
                            placeholder="/api/webhook"
                            className="h-8"
                          />
                        </div>
                      </div>

                      <div className="grid grid-cols-3 gap-3">
                        <div className="space-y-1">
                          <Label className="text-xs text-slate-700">Port</Label>
                          <Input
                            type="number"
                            value={formData.port || ""}
                            onChange={(e) => handleInputChange("port", parseInt(e.target.value) || null)}
                            placeholder="443"
                            className="h-8"
                          />
                        </div>

                        <div className="space-y-1">
                          <Label className="text-xs text-slate-700">HTTP Method *</Label>
                          <Select
                            value={formData.method || ""}
                            onValueChange={(value) => handleInputChange("method", value)}
                          >
                            <SelectTrigger className="h-8">
                              <SelectValue placeholder="Method" />
                            </SelectTrigger>
                            <SelectContent>
                              {httpMethods.map((method) => (
                                <SelectItem key={method.value} value={method.value}>
                                  {method.label}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>

                        <div className="space-y-1">
                          <Label className="text-xs text-slate-700">Content Type *</Label>
                          <Select
                            value={formData.content_type || ""}
                            onValueChange={(value) => handleInputChange("content_type", value)}
                          >
                            <SelectTrigger className="h-8">
                              <SelectValue placeholder="Type" />
                            </SelectTrigger>
                            <SelectContent>
                              {contentTypes.map((type) => (
                                <SelectItem key={type.value} value={type.value}>
                                  {type.label}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>
                      </div>
                    </TabsContent>

                    <TabsContent value="headers" className="mt-4 p-4 border rounded-lg bg-slate-50">
                      <div className="space-y-3">
                        <Label className="text-sm text-slate-700">Header Template</Label>
                        <div className="border rounded-md">
                          <CodeMirror
                            value={formData.header_template || "{}"}
                            height="200px"
                            extensions={[jsonLanguage]}
                            onChange={(value) => handleInputChange("header_template", value)}
                            className="text-sm"
                          />
                        </div>
                      </div>
                    </TabsContent>

                    <TabsContent value="parameters" className="space-y-4 mt-4 p-4 border rounded-lg bg-slate-50">
                      <div className="space-y-2">
                        <Label className="text-sm text-slate-700">Parameters Type *</Label>
                        <Select
                          value={formData.parameters_type || ""}
                          onValueChange={(value) => handleInputChange("parameters_type", value)}
                        >
                          <SelectTrigger className="h-9">
                            <SelectValue placeholder="Select type" />
                          </SelectTrigger>
                          <SelectContent>
                            {parameterTypes.map((type) => (
                              <SelectItem key={type.value} value={type.value}>
                                {type.label}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="space-y-2">
                        <Label className="text-sm text-slate-700">Parameters Template</Label>
                        <div className="border rounded-md">
                          <CodeMirror
                            value={formData.parameters_template || "{}"}
                            height="200px"
                            extensions={[htmlLanguage]}
                            onChange={(value) => handleInputChange("parameters_template", value)}
                            className="text-sm"
                          />
                        </div>
                      </div>
                    </TabsContent>
                  </Tabs>
                </div>
              )}

              {/* Data Mapping Configuration */}
              {formData.action_type === AutomationActionType.data_mapping && (
                <div className="space-y-4">
                  <h3 className="text-sm font-semibold text-slate-900 mb-2">Data Mapping Configuration</h3>

                  <div className="space-y-3">
                    <div className="space-y-1">
                      <Label className="text-xs text-slate-700">Content Type *</Label>
                      <Select
                        value={formData.content_type || ""}
                        onValueChange={(value) => handleInputChange("content_type", value)}
                      >
                        <SelectTrigger className="h-8">
                          <SelectValue placeholder="Select format" />
                        </SelectTrigger>
                        <SelectContent>
                          {contentTypes.map((type) => (
                            <SelectItem key={type.value} value={type.value}>
                              {type.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div className="space-y-1">
                      <Label className="text-xs text-slate-700">Mapping Template</Label>
                      <div className="border rounded-md">
                        <CodeMirror
                          value={formData.parameters_template || "{}"}
                          height="200px"
                          extensions={[htmlLanguage]}
                          onChange={(value) => handleInputChange("parameters_template", value)}
                          className="text-xs"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Conditional Configuration */}
              {formData.action_type === AutomationActionType.conditional && (
                <div className="space-y-4">
                  <h3 className="text-sm font-semibold text-slate-900 mb-2">Conditional Configuration</h3>

                  <div className="space-y-1">
                    <Label className="text-xs text-slate-700">Condition Template</Label>
                    <div className="border rounded-md">
                      <CodeMirror
                        value={formData.parameters_template || "{}"}
                        height="200px"
                        extensions={[htmlLanguage]}
                        onChange={(value) => handleInputChange("parameters_template", value)}
                        className="text-xs"
                      />
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Floating Footer */}
            <div className="sticky bottom-0 z-10 bg-white border-t px-4 py-4">
              <div className="flex items-center justify-end gap-3">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => setIsOpen(false)}
                  disabled={isLoading}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  size="sm"
                  disabled={isLoading}
                >
                  {isLoading ? "Saving..." : "Save"}
                </Button>
              </div>
            </div>
          </form>
        </div>
      </SheetContent>
    </Sheet>
  );
}
