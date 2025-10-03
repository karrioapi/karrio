"use client";

import React, { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@karrio/ui/components/ui/dialog";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@karrio/ui/components/ui/card";
import { Badge } from "@karrio/ui/components/ui/badge";
import { Search, Truck, Settings, Plus } from "lucide-react";
import { useShippingRuleTemplates, ShippingRuleTemplate } from "@karrio/hooks/shipping-rule-templates";

interface ShippingRuleTemplatePickerProps {
  onSelectTemplate: (template: ShippingRuleTemplate | null) => void;
  children: React.ReactNode;
}

export function ShippingRuleTemplatePicker({ onSelectTemplate, children }: ShippingRuleTemplatePickerProps) {
  const [open, setOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const { templates } = useShippingRuleTemplates();

  const filteredTemplates = templates.filter(
    template =>
      template.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      template.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSelectTemplate = (template: ShippingRuleTemplate) => {
    onSelectTemplate(template);
    setOpen(false);
    setSearchTerm("");
  };

  const handleCreateCustom = () => {
    onSelectTemplate(null);
    setOpen(false);
    setSearchTerm("");
  };

  return (
    <>
      {React.cloneElement(children as React.ReactElement, {
        onClick: () => setOpen(true),
      })}

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="max-w-4xl h-[80vh]">
          <DialogHeader className="p-4 pb-2">
            <div className="flex items-center gap-2">
              <Truck className="h-5 w-5" />
              <DialogTitle className="text-base">Choose a Shipping Rule Template</DialogTitle>
            </div>
            <p className="text-sm text-slate-600 mt-1">
              Start with a pre-configured rule or create your own from scratch
            </p>
          </DialogHeader>

          {/* Search */}
          <div className="p-4 pb-8">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
              <Input
                placeholder="Search templates..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 h-8 text-sm"
              />
            </div>
          </div>

          {/* Templates Grid */}
          <div className="flex-1 overflow-y-auto p-4 pb-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {filteredTemplates.map((template) => (
                <Card
                  key={template.slug}
                  className="cursor-pointer hover:shadow-md transition-shadow border-slate-200 hover:border-slate-300"
                  onClick={() => handleSelectTemplate(template)}
                >
                  <CardHeader className="pb-2 p-3">
                    <div className="flex items-start gap-2">
                      <span className="text-lg">{template.icon}</span>
                      <div className="flex-1 min-w-0">
                        <CardTitle className="text-sm font-medium line-clamp-2">
                          {template.name}
                        </CardTitle>
                        <div className="flex items-center gap-1 mt-1">
                          <Badge variant="outline" className="text-xs h-5">
                            Priority {template.priority}
                          </Badge>
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="px-3 pb-3">
                    <p className="text-xs text-slate-600 line-clamp-3">
                      {template.description}
                    </p>

                    {/* Preview conditions and actions */}
                    <div className="mt-3 space-y-2">
                      {Object.keys(template.conditions).length > 0 && (
                        <div>
                          <p className="text-xs font-medium text-slate-700">Conditions:</p>
                          <div className="text-xs text-slate-500">
                            {template.conditions.destination?.country_code && (
                              <span>Country: {template.conditions.destination.country_code} </span>
                            )}
                            {template.conditions.weight && (
                              <span>Weight: {template.conditions.weight.min || 0}-{template.conditions.weight.max || '∞'}{template.conditions.weight.unit} </span>
                            )}
                            {template.conditions.address_type && (
                              <span>Address: {template.conditions.address_type.type} </span>
                            )}
                          </div>
                        </div>
                      )}

                      <div>
                        <p className="text-xs font-medium text-slate-700">Actions:</p>
                        <div className="text-xs text-slate-500">
                          {template.actions.select_service && (
                            <span>Select: {template.actions.select_service.strategy} </span>
                          )}
                          {template.actions.block_service && (
                            <span>Block service </span>
                          )}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}

              {/* Create Custom Option */}
              <Card
                className="cursor-pointer hover:shadow-md transition-shadow border-dashed border-slate-300 hover:border-slate-400"
                onClick={handleCreateCustom}
              >
                <CardContent className="flex flex-col items-center justify-center h-full p-6 text-center">
                  <div className="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center mb-3">
                    <Plus className="h-6 w-6 text-slate-500" />
                  </div>
                  <h3 className="text-sm font-medium text-slate-900">Create Custom Rule</h3>
                  <p className="text-xs text-slate-500 mt-1">
                    Start from scratch with your own conditions and actions
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* No results */}
            {filteredTemplates.length === 0 && searchTerm && (
              <div className="text-center py-8">
                <Settings className="h-8 w-8 text-slate-400 mx-auto mb-2" />
                <p className="text-sm text-slate-600">No templates found for "{searchTerm}"</p>
                <Button
                  variant="outline"
                  size="sm"
                  className="mt-2"
                  onClick={handleCreateCustom}
                >
                  Create Custom Rule Instead
                </Button>
              </div>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
}
