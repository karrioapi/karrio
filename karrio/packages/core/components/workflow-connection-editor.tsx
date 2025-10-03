"use client";

import React, { useState } from "react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from "@karrio/ui/components/ui/sheet";
import { AutomationAuthType, PartialWorkflowConnectionMutationInput, MetafieldInput, CreateMetafieldInput, MetafieldTypeEnum } from "@karrio/types/graphql/ee";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@karrio/ui/components/ui/tabs";
import { Textarea } from "@karrio/ui/components/ui/textarea";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Checkbox } from "@karrio/ui/components/ui/checkbox";
import { AlertCircle, Plus, Trash2, Eye, EyeOff } from "lucide-react";
import { jsonLanguage } from "@codemirror/lang-json";
import { htmlLanguage } from "@codemirror/lang-html";
import CodeMirror from "@uiw/react-codemirror";

interface ConnectionEditorProps {
  connection: PartialWorkflowConnectionMutationInput;
  onSubmit: (data: PartialWorkflowConnectionMutationInput) => Promise<void>;
  trigger: React.ReactElement;
}

interface MetafieldState extends MetafieldInput {
  tempId?: string;
}

export function ConnectionModalEditor({ connection, onSubmit, trigger }: ConnectionEditorProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [formData, setFormData] = useState<PartialWorkflowConnectionMutationInput>(connection);
  const [isLoading, setIsLoading] = useState(false);
  const [metafields, setMetafields] = useState<MetafieldState[]>(
    connection.metafields?.map(mf => ({ ...mf })) || []
  );
  const [useLegacyCredentials, setUseLegacyCredentials] = useState(
    Boolean(connection.credentials && Object.keys(connection.credentials).length > 0)
  );
  const [showSensitiveValues, setShowSensitiveValues] = useState<Record<string, boolean>>({});

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const submitData = {
        ...formData,
        metafields: metafields.map(({ tempId, ...mf }) => mf),
        // Clear credentials if using metafields
        ...(useLegacyCredentials ? {} : { credentials: null })
      };
      await onSubmit(submitData);
      setIsOpen(false);
    } catch (error) {
      console.error("Failed to save connection:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (field: keyof PartialWorkflowConnectionMutationInput, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  // Metafield management functions
  const addMetafield = () => {
    const newMetafield: MetafieldState = {
      tempId: `temp-${Date.now()}`,
      key: "",
      type: MetafieldTypeEnum.text,
      is_required: false,
      value: ""
    };
    setMetafields(prev => [...prev, newMetafield]);
  };

  const updateMetafield = (index: number, updates: Partial<MetafieldState>) => {
    setMetafields(prev => prev.map((mf, i) => i === index ? { ...mf, ...updates } : mf));
  };

  const removeMetafield = (index: number) => {
    setMetafields(prev => prev.filter((_, i) => i !== index));
  };

  const toggleSensitiveValue = (key: string) => {
    setShowSensitiveValues(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const getCredentialsFromMetafields = () => {
    return metafields.reduce((acc, mf) => {
      if (mf.key && mf.value) {
        acc[mf.key] = mf.value;
      }
      return acc;
    }, {} as Record<string, string>);
  };

  const authTypes = [
    { value: AutomationAuthType.basic, label: "Basic Auth" },
    { value: AutomationAuthType.api_key, label: "API Key" },
    { value: AutomationAuthType.oauth2, label: "OAuth2" },
    { value: AutomationAuthType.jwt, label: "JWT" },
  ];

  const metafieldTypes = [
    { value: MetafieldTypeEnum.text, label: "Text" },
    { value: MetafieldTypeEnum.number, label: "Number" },
    { value: MetafieldTypeEnum.boolean, label: "Boolean" },
  ];

  return (
    <Sheet open={isOpen} onOpenChange={setIsOpen}>
      <SheetTrigger asChild>{trigger}</SheetTrigger>
      <SheetContent className="w-full sm:w-[800px] sm:max-w-[800px] p-0 shadow-none">
        <div className="h-full flex flex-col">
          <SheetHeader className="sticky top-0 z-10 bg-white px-4 py-3 border-b">
            <SheetTitle className="text-lg font-semibold">Edit Connection</SheetTitle>
            <p className="text-xs text-slate-600">Configure connection settings and authentication for this action.</p>
          </SheetHeader>

          <form onSubmit={handleSubmit} className="flex-1 overflow-y-auto">
            <div className="px-4 py-4 space-y-6 pb-32">

              {/* Basic Configuration */}
              <div className="space-y-4">
                <h3 className="text-sm font-semibold text-slate-900 mb-4">Basic Configuration</h3>
                <div className="space-y-3">
                  <div className="grid grid-cols-2 gap-3">
                    <div className="space-y-1">
                      <Label className="text-xs text-slate-700">Connection Name *</Label>
                      <Input
                        value={formData.name || ""}
                        onChange={(e) => handleInputChange("name", e.target.value)}
                        placeholder="e.g., Production API"
                        className="h-8"
                        required
                      />
                    </div>

                    <div className="space-y-1">
                      <Label className="text-xs text-slate-700">Auth Type *</Label>
                      <Select
                        value={formData.auth_type || ""}
                        onValueChange={(value) => handleInputChange("auth_type", value)}
                      >
                        <SelectTrigger className="h-8">
                          <SelectValue placeholder="Select auth type" />
                        </SelectTrigger>
                        <SelectContent>
                          {authTypes.map((type) => (
                            <SelectItem key={type.value} value={type.value}>
                              {type.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="space-y-1">
                    <Label className="text-xs text-slate-700">Description</Label>
                    <Textarea
                      value={formData.description || ""}
                      onChange={(e) => handleInputChange("description", e.target.value)}
                      placeholder="Describe this connection..."
                      rows={2}
                      className="text-xs"
                    />
                  </div>
                </div>
              </div>

              {/* Connection Details */}
              {(formData.auth_type === AutomationAuthType.oauth2 || formData.auth_type === AutomationAuthType.jwt) && (
                <div className="space-y-4">
                  <h3 className="text-sm font-semibold text-slate-900 mb-2">Connection Details</h3>

                  <div className="space-y-3">
                    <div className="grid grid-cols-2 gap-3">
                      <div className="space-y-1">
                        <Label className="text-xs text-slate-700">Host *</Label>
                        <Input
                          value={formData.host || ""}
                          onChange={(e) => handleInputChange("host", e.target.value)}
                          placeholder="api.example.com"
                          className="h-8"
                          required
                        />
                      </div>

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
                    </div>

                    <div className="space-y-1">
                      <Label className="text-xs text-slate-700">Endpoint</Label>
                      <Input
                        value={formData.endpoint || ""}
                        onChange={(e) => handleInputChange("endpoint", e.target.value)}
                        placeholder="/oauth/token"
                        className="h-8"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* Authentication Configuration */}
              <div className="space-y-4">
                <h3 className="text-sm font-semibold text-slate-900 mb-2">Authentication Configuration</h3>

                <Tabs defaultValue="auth" className="w-full">
                  <TabsList className="grid w-full grid-cols-2 h-9">
                    <TabsTrigger value="auth" className="text-xs">Auth Template</TabsTrigger>
                    <TabsTrigger value="parameters" className="text-xs">Parameters</TabsTrigger>
                  </TabsList>

                  <TabsContent value="auth" className="mt-3">
                    <div className="space-y-1">
                      <Label className="text-xs text-slate-700">Authentication Template</Label>
                      <div className="border rounded-md">
                        <CodeMirror
                          value={formData.auth_template || "{}"}
                          height="200px"
                          extensions={[htmlLanguage]}
                          onChange={(value) => handleInputChange("auth_template", value)}
                          className="text-xs"
                        />
                      </div>
                      <p className="text-xs text-slate-500">
                        {formData.auth_type === AutomationAuthType.basic && "Format: username:password (base64 encoded)"}
                        {formData.auth_type === AutomationAuthType.api_key && "Format: API key value or header format"}
                        {formData.auth_type === AutomationAuthType.oauth2 && "Format: OAuth2 token request template"}
                        {formData.auth_type === AutomationAuthType.jwt && "Format: JWT token template"}
                      </p>
                    </div>
                  </TabsContent>

                  <TabsContent value="parameters" className="mt-3">
                    <div className="space-y-1">
                      <Label className="text-xs text-slate-700">Parameters Template</Label>
                      <div className="border rounded-md">
                        <CodeMirror
                          value={formData.parameters_template || "{}"}
                          height="200px"
                          extensions={[jsonLanguage]}
                          onChange={(value) => handleInputChange("parameters_template", value)}
                          className="text-xs"
                        />
                      </div>
                      <p className="text-xs text-slate-500">
                        Additional parameters for authentication (client_id, scopes, etc.)
                      </p>
                    </div>
                  </TabsContent>
                </Tabs>
              </div>

              {/* Credentials Management */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-semibold text-slate-900">Credentials Management</h3>
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="use-legacy"
                      checked={useLegacyCredentials}
                      onCheckedChange={(checked) => setUseLegacyCredentials(checked === true)}
                    />
                    <Label htmlFor="use-legacy" className="text-xs text-slate-600">Use legacy JSON credentials</Label>
                  </div>
                </div>

                {!useLegacyCredentials ? (
                  <Tabs defaultValue="setup" className="w-full">
                    <TabsList className="grid w-full grid-cols-2 h-7">
                      <TabsTrigger value="setup" className="text-xs h-7">Metafields Setup</TabsTrigger>
                      <TabsTrigger value="values" className="text-xs h-7">Credential Values</TabsTrigger>
                    </TabsList>

                    <TabsContent value="setup" className="mt-3 space-y-4">
                      <div className="space-y-3">
                        <div className="flex items-center justify-between">
                          <Label className="text-xs text-slate-700">Metafield Definitions</Label>
                          <Button
                            type="button"
                            variant="outline"
                            size="sm"
                            onClick={addMetafield}
                            className="h-7 text-xs"
                          >
                            <Plus className="h-3 w-3 mr-1" />
                            Add Field
                          </Button>
                        </div>

                        {metafields.length === 0 ? (
                          <div className="text-center py-8 text-slate-500 border rounded-md border-dashed">
                            <p className="text-sm">No metafields defined</p>
                            <p className="text-xs">Click "Add Field" to create credential fields</p>
                          </div>
                        ) : (
                          <div className="space-y-3">
                            {metafields.map((metafield, index) => (
                              <div key={metafield.tempId || metafield.id || index} className="border rounded-md p-3 space-y-3">
                                <div className="grid grid-cols-12 gap-2 items-end">
                                  <div className="col-span-4 space-y-1">
                                    <Label className="text-xs text-slate-700">Key *</Label>
                                    <Input
                                      value={metafield.key || ""}
                                      onChange={(e) => updateMetafield(index, { key: e.target.value })}
                                      placeholder="e.g., api_key"
                                      className="h-7 text-xs"
                                      required
                                    />
                                  </div>

                                  <div className="col-span-3 space-y-1">
                                    <Label className="text-xs text-slate-700">Type</Label>
                                    <Select
                                      value={metafield.type || MetafieldTypeEnum.text}
                                      onValueChange={(value) => updateMetafield(index, { type: value as MetafieldTypeEnum })}
                                    >
                                      <SelectTrigger className="h-7 text-xs">
                                        <SelectValue />
                                      </SelectTrigger>
                                      <SelectContent>
                                        {metafieldTypes.map((type) => (
                                          <SelectItem key={type.value} value={type.value}>
                                            {type.label}
                                          </SelectItem>
                                        ))}
                                      </SelectContent>
                                    </Select>
                                  </div>

                                  <div className="col-span-3 flex items-center space-x-2 pb-1">
                                    <Checkbox
                                      id={`required-${index}`}
                                      checked={metafield.is_required || false}
                                      onCheckedChange={(checked) => updateMetafield(index, { is_required: checked === true })}
                                    />
                                    <Label htmlFor={`required-${index}`} className="text-xs text-slate-600">Required</Label>
                                  </div>

                                  <div className="col-span-2 flex justify-end">
                                    <Button
                                      type="button"
                                      variant="ghost"
                                      size="sm"
                                      onClick={() => removeMetafield(index)}
                                      className="h-7 w-7 p-0 text-red-500 hover:text-red-700"
                                    >
                                      <Trash2 className="h-3 w-3" />
                                    </Button>
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    </TabsContent>

                    <TabsContent value="values" className="mt-3 space-y-4">
                      <div className="space-y-3">
                        <Label className="text-xs text-slate-700">Set Credential Values</Label>

                        {metafields.length === 0 ? (
                          <div className="text-center py-8 text-slate-500 border rounded-md border-dashed">
                            <p className="text-sm">No metafields to configure</p>
                            <p className="text-xs">Add metafields in the Setup tab first</p>
                          </div>
                        ) : (
                          <div className="space-y-3">
                            {metafields.map((metafield, index) => (
                              <div key={metafield.tempId || metafield.id || index} className="space-y-1">
                                <div className="flex items-center gap-2">
                                  <Label className="text-xs text-slate-700">
                                    {metafield.key}
                                    {metafield.is_required && (
                                      <Badge variant="destructive" className="ml-1 text-xs">Required</Badge>
                                    )}
                                  </Label>
                                  {metafield.key && (metafield.key.toLowerCase().includes('password') ||
                                    metafield.key.toLowerCase().includes('secret') ||
                                    metafield.key.toLowerCase().includes('token')) && (
                                      <Button
                                        type="button"
                                        variant="ghost"
                                        size="sm"
                                        onClick={() => toggleSensitiveValue(metafield.key!)}
                                        className="h-6 w-6 p-0"
                                      >
                                        {showSensitiveValues[metafield.key!] ? (
                                          <EyeOff className="h-3 w-3" />
                                        ) : (
                                          <Eye className="h-3 w-3" />
                                        )}
                                      </Button>
                                    )}
                                </div>

                                {metafield.type === MetafieldTypeEnum.boolean ? (
                                  <div className="flex items-center space-x-2">
                                    <Checkbox
                                      id={`value-${index}`}
                                      checked={metafield.value === 'true'}
                                      onCheckedChange={(checked) => updateMetafield(index, { value: checked === true ? 'true' : 'false' })}
                                    />
                                    <Label htmlFor={`value-${index}`} className="text-xs text-slate-600">Enabled</Label>
                                  </div>
                                ) : (
                                  <Input
                                    type={metafield.type === MetafieldTypeEnum.number ? "number" :
                                      (metafield.key && (metafield.key.toLowerCase().includes('password') ||
                                        metafield.key.toLowerCase().includes('secret') ||
                                        metafield.key.toLowerCase().includes('token')) &&
                                        !showSensitiveValues[metafield.key]) ? "password" : "text"}
                                    value={metafield.value || ""}
                                    onChange={(e) => updateMetafield(index, { value: e.target.value })}
                                    placeholder={`Enter ${metafield.key}`}
                                    className={`h-8 text-xs ${metafield.is_required && !metafield.value ? 'border-red-300 focus:border-red-500' : ''}`}
                                    required={metafield.is_required || false}
                                  />
                                )}

                                {metafield.is_required && !metafield.value && (
                                  <div className="flex items-center gap-1 text-red-600">
                                    <AlertCircle className="h-3 w-3" />
                                    <span className="text-xs">This field is required</span>
                                  </div>
                                )}
                              </div>
                            ))}

                            {/* Preview of credentials from metafields */}
                            <div className="mt-4 p-3 bg-slate-50 rounded-md">
                              <Label className="text-xs text-slate-700 font-medium">Credentials Preview</Label>
                              <pre className="text-xs text-slate-600 mt-1 whitespace-pre-wrap">
                                {JSON.stringify(getCredentialsFromMetafields(), null, 2)}
                              </pre>
                            </div>
                          </div>
                        )}
                      </div>
                    </TabsContent>
                  </Tabs>
                ) : (
                  // Legacy Credentials JSON
                  <div className="space-y-1">
                    <Label className="text-xs text-slate-700">Credentials (JSON)</Label>
                    <div className="border rounded-md">
                      <CodeMirror
                        value={formData.credentials ? JSON.stringify(formData.credentials, null, 2) : "{}"}
                        height="150px"
                        extensions={[jsonLanguage]}
                        onChange={(value) => {
                          try {
                            const parsed = JSON.parse(value);
                            handleInputChange("credentials", parsed);
                          } catch (e) {
                            // Invalid JSON, store as string temporarily
                            handleInputChange("credentials", value);
                          }
                        }}
                        className="text-xs"
                      />
                    </div>
                    <p className="text-xs text-slate-500">
                      Store sensitive authentication data (passwords, client secrets, etc.)
                    </p>
                  </div>
                )}
              </div>
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
