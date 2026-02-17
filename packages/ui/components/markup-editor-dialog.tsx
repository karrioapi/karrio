"use client";

import React, { useEffect, useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogDescription,
  DialogBody,
} from "@karrio/ui/components/ui/dialog";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Checkbox } from "@karrio/ui/components/ui/checkbox";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@karrio/ui/components/ui/select";
import type { MarkupType, MarkupMeta } from "@karrio/hooks/admin-markups";

interface MarkupEditorDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  markup: MarkupType | null;
  isNew?: boolean;
  onSave: (data: {
    name: string;
    amount: number;
    markup_type: string;
    active: boolean;
    is_visible: boolean;
    meta: MarkupMeta;
  }) => void | Promise<void>;
}

const MARKUP_TYPES = [
  { value: "AMOUNT", label: "Fixed Amount" },
  { value: "PERCENTAGE", label: "Percentage" },
];

const META_TYPES = [
  { value: "", label: "None" },
  { value: "brokerage-fee", label: "Brokerage Fee" },
  { value: "insurance", label: "Insurance" },
  { value: "surcharge", label: "Surcharge" },
  { value: "notification", label: "Notification" },
  { value: "address-validation", label: "Address Validation" },
];

export function MarkupEditorDialog({
  open,
  onOpenChange,
  markup,
  isNew = false,
  onSave,
}: MarkupEditorDialogProps) {
  const [name, setName] = useState("");
  const [markupType, setMarkupType] = useState("AMOUNT");
  const [amount, setAmount] = useState("0");
  const [active, setActive] = useState(true);
  const [isVisible, setIsVisible] = useState(true);
  const [metaType, setMetaType] = useState("");
  const [metaPlan, setMetaPlan] = useState("");
  const [showInPreview, setShowInPreview] = useState(false);
  const [featureGate, setFeatureGate] = useState("");

  useEffect(() => {
    if (open) {
      if (markup && !isNew) {
        const meta = (markup as any).meta as MarkupMeta | undefined;
        setName(markup.name || "");
        setMarkupType(markup.markup_type || "AMOUNT");
        setAmount(markup.amount?.toString() || "0");
        setActive(markup.active ?? true);
        setIsVisible(markup.is_visible ?? true);
        setMetaType(meta?.type || "");
        setMetaPlan(meta?.plan || "");
        setShowInPreview(meta?.show_in_preview ?? false);
        setFeatureGate(meta?.feature_gate || "");
      } else {
        setName("");
        setMarkupType("AMOUNT");
        setAmount("0");
        setActive(true);
        setIsVisible(true);
        setMetaType("");
        setMetaPlan("");
        setShowInPreview(false);
        setFeatureGate("");
      }
    }
  }, [markup, open, isNew]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const meta: MarkupMeta = {};
    if (metaType) meta.type = metaType as MarkupMeta["type"];
    if (metaPlan) meta.plan = metaPlan;
    if (showInPreview) meta.show_in_preview = true;
    if (featureGate) meta.feature_gate = featureGate;

    await onSave({
      name,
      amount: parseFloat(amount) || 0,
      markup_type: markupType,
      active,
      is_visible: isVisible,
      meta,
    });
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-lg">
        <DialogHeader>
          <DialogTitle>{isNew ? "Create Markup" : "Edit Markup"}</DialogTitle>
          <DialogDescription>
            Configure markup details and categorization
          </DialogDescription>
        </DialogHeader>

        <DialogBody>
          <form id="markup-form" onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-1.5">
              <Label className="text-xs">Name</Label>
              <Input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Brokerage Fee"
                className="h-9"
                required
              />
            </div>

            <div className="space-y-1.5">
              <Label className="text-xs">Markup Type</Label>
              <Select value={markupType} onValueChange={setMarkupType}>
                <SelectTrigger className="w-full h-9">
                  <SelectValue placeholder="Select type" />
                </SelectTrigger>
                <SelectContent>
                  {MARKUP_TYPES.map((type) => (
                    <SelectItem key={type.value} value={type.value}>
                      {type.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-1.5">
              <Label className="text-xs">
                Amount {markupType === "PERCENTAGE" ? "(%)" : ""}
              </Label>
              <Input
                type="number"
                step="0.01"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="0.00"
                className="h-9"
                required
              />
            </div>

            <div className="flex items-center space-x-4 pt-1">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="markup-active"
                  checked={active}
                  onCheckedChange={(checked) => setActive(checked === true)}
                />
                <Label htmlFor="markup-active" className="text-xs cursor-pointer">
                  Active
                </Label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="markup-visible"
                  checked={isVisible}
                  onCheckedChange={(checked) => setIsVisible(checked === true)}
                />
                <Label htmlFor="markup-visible" className="text-xs cursor-pointer">
                  Visible
                </Label>
              </div>
            </div>

            {/* Meta Configuration */}
            <div className="pt-3 border-t border-border space-y-4">
              <p className="text-xs font-medium text-muted-foreground">Categorization</p>

              <div className="space-y-1.5">
                <Label className="text-xs">Category</Label>
                <Select value={metaType} onValueChange={setMetaType}>
                  <SelectTrigger className="w-full h-9">
                    <SelectValue placeholder="Select category" />
                  </SelectTrigger>
                  <SelectContent>
                    {META_TYPES.map((type) => (
                      <SelectItem key={type.value || "none"} value={type.value || "none"}>
                        {type.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-1.5">
                <Label className="text-xs">Plan</Label>
                <Input
                  value={metaPlan}
                  onChange={(e) => setMetaPlan(e.target.value)}
                  placeholder="e.g. scale, pro, enterprise"
                  className="h-9"
                />
              </div>

              <div className="space-y-1.5">
                <Label className="text-xs">Feature Gate</Label>
                <Input
                  value={featureGate}
                  onChange={(e) => setFeatureGate(e.target.value)}
                  placeholder="e.g. insurance, notification"
                  className="h-9"
                />
                <p className="text-xs text-muted-foreground">
                  Service feature key required for this markup to apply
                </p>
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="markup-preview"
                  checked={showInPreview}
                  onCheckedChange={(checked) => setShowInPreview(checked === true)}
                />
                <Label htmlFor="markup-preview" className="text-xs cursor-pointer">
                  Show in rate sheet preview
                </Label>
              </div>
            </div>
          </form>
        </DialogBody>

        <DialogFooter>
          <Button type="button" variant="outline" size="sm" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button type="submit" size="sm" form="markup-form">
            {isNew ? "Create" : "Save"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default MarkupEditorDialog;
