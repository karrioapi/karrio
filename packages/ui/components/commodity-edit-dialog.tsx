import React, { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@karrio/ui/components/ui/dialog";
import {
  CurrencyCodeEnum,
  DEFAULT_COMMODITY_CONTENT,
  WeightUnitEnum,
  ProductTemplateType,
} from "@karrio/types";
import { EnhancedMetadataEditor } from "@karrio/ui/components/enhanced-metadata-editor";
import { isEqual, isNone } from "@karrio/lib";
import { CommodityType, CURRENCY_OPTIONS, WEIGHT_UNITS } from "@karrio/types";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { LineItemInput } from "@karrio/ui/components/line-item-input";
import { ProductCombobox } from "@karrio/ui/components/product-combobox";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { CountrySelect } from "@karrio/ui/components/country-select";
import { Textarea } from "@karrio/ui/components/ui/textarea";
import { useOrders } from "@karrio/hooks/order";

export interface CommodityEditDialogProps {
  trigger: React.ReactElement;
  commodity?: CommodityType;
  onSubmit: (commodity: CommodityType) => Promise<any>;
  orderFilter?: any;
  disableOrderLinking?: boolean;
}


export const CommodityEditDialog = ({
  trigger,
  commodity: initialCommodity,
  onSubmit,
  orderFilter,
  disableOrderLinking = false,
}: CommodityEditDialogProps): JSX.Element => {
  const { metadata: { ORDERS_MANAGEMENT } } = useAPIMetadata();
  const [isOpen, setIsOpen] = useState(false);
  const [commodity, setCommodity] = useState<Partial<CommodityType>>(
    initialCommodity || DEFAULT_COMMODITY_CONTENT
  );
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [advancedExpanded, setAdvancedExpanded] = useState(false);
  const [maxQty, setMaxQty] = useState<number | null | undefined>();

  const { query } = useOrders({
    first: 10,
    status: ["unfulfilled", "partial"] as any,
    isDisabled: !ORDERS_MANAGEMENT,
    ...(orderFilter || {}),
  });

  React.useEffect(() => {
    setCommodity(initialCommodity || DEFAULT_COMMODITY_CONTENT);
  }, [initialCommodity]);

  // always provide fresh state for new operations
  React.useEffect(() => {
    if (isOpen) {
      // always set commodity state when opening
      const commodityData = initialCommodity || DEFAULT_COMMODITY_CONTENT;
      setCommodity(commodityData);
      // Reset maxQty for new operations
      if (!initialCommodity) {
        setMaxQty(undefined);
      }
    }
  }, [isOpen, initialCommodity]);

  const handleChange = (field: string, value: string | number | boolean | null) => {
    const updatedCommodity = { ...commodity, [field]: value };

    // Handle value_amount special case
    if (field === "value_amount") {
      updatedCommodity.value_currency = updatedCommodity.value_currency || CurrencyCodeEnum.USD;
    }

    setCommodity(updatedCommodity);
  };

  const handleSubmit = async (data: Partial<CommodityType>) => {
    try {
      await onSubmit(data as CommodityType);
      setIsOpen(false);
    } catch (error) {
      console.error("Commodity submission error:", error);
    }
  };

  const handleFooterSubmit = async () => {
    setIsSubmitting(true);
    try {
      await handleSubmit(commodity);
    } finally {
      setIsSubmitting(false);
    }
  };

  const loadLineItem = (item?: any) => {
    if (!item) {
      setMaxQty(undefined);
      return;
    }

    const {
      id: parent_id,
      unfulfilled_quantity: quantity,
      ...content
    } = item;

    // Clean content to handle null values - use description as fallback for title
    const cleanedContent = {
      ...content,
      title: content.title || content.description || "",
      description: content.description || "",
      sku: content.sku || "",
      hs_code: content.hs_code || "",
      origin_country: content.origin_country || "",
    };

    setMaxQty(quantity);
    setCommodity({
      ...commodity,
      ...cleanedContent,
      parent_id,
      quantity: Number(quantity) || commodity.quantity,
    });
  };

  const loadProductTemplate = (product: ProductTemplateType | null) => {
    if (!product) return;

    // Load product template data into commodity form
    setCommodity({
      ...commodity,
      title: product.title || commodity.title,
      description: product.description || commodity.description,
      sku: product.sku || commodity.sku,
      hs_code: product.hs_code || commodity.hs_code,
      origin_country: product.origin_country || commodity.origin_country,
      weight: product.weight || commodity.weight,
      weight_unit: product.weight_unit || commodity.weight_unit,
      quantity: product.quantity || commodity.quantity,
      value_amount: product.value_amount || commodity.value_amount,
      value_currency: product.value_currency || commodity.value_currency,
      metadata: product.metadata || commodity.metadata,
    });
  };

  // Validation logic
  const missingRequired = !commodity?.title || !commodity?.quantity || !commodity?.weight || !commodity?.origin_country;
  const hasChanges = !isEqual(initialCommodity, commodity) || (
    commodity?.title || commodity?.quantity || commodity?.weight
  );
  const isQuantityValid = !maxQty || !commodity?.quantity || commodity.quantity <= maxQty;

  const isNew = !initialCommodity?.id;

  return (
    <>
      {React.cloneElement(trigger, {
        onClick: () => setIsOpen(true),
      })}

      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="max-w-2xl max-h-[90vh] p-0 flex flex-col">
          {/* Sticky Header */}
          <DialogHeader className="px-4 py-3 border-b sticky top-0 bg-background z-5">
            <DialogTitle>
              {isNew ? "Add" : "Update"} commodity
            </DialogTitle>
          </DialogHeader>

          <div className="flex flex-col flex-1 min-h-0">
            <div className="flex-1 overflow-y-auto px-4 py-3">
              <div className="space-y-6">
                {/* Product Template Selector */}
                <ProductCombobox
                  label="Load from Product Template"
                  placeholder="Search products by name, SKU, or HS code..."
                  onValueChange={loadProductTemplate}
                  disabled={!isNone(commodity?.parent_id)}
                />

                {ORDERS_MANAGEMENT && !disableOrderLinking && (
                  <LineItemInput
                    label="Order Line Item"
                    value={commodity?.parent_id || null}
                    onValueChange={(value) => {
                      handleChange("parent_id", value);
                      if (!value) {
                        setMaxQty(undefined);
                      } else {
                        // Find and load the selected line item
                        const allItems = (query.data?.orders.edges || []).map(({ node: order }) => order.line_items).flat();
                        const selectedItem = allItems.find(item => item.id === value);
                        if (selectedItem) loadLineItem(selectedItem);
                      }
                    }}
                    onUnlink={() => {
                      handleChange("parent_id", null);
                      setMaxQty(undefined);
                    }}
                    query={query}
                    showUnlinkButton={true}
                    placeholder="Link an order line item"
                  />
                )}

                <div className="space-y-2">
                  <Label htmlFor="title" className="text-sm font-medium">
                    Title <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    id="title"
                    placeholder="Product Name"
                    value={commodity?.title || ""}
                    onChange={(e) => handleChange("title", e.target.value)}
                    disabled={!isNone(commodity?.parent_id)}
                    maxLength={35}
                    className="h-8"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="hs_code" className="text-sm font-medium">HS Code</Label>
                  <Input
                    id="hs_code"
                    placeholder="0000.00.00.00"
                    value={commodity?.hs_code || ""}
                    onChange={(e) => handleChange("hs_code", e.target.value)}
                    disabled={!isNone(commodity?.parent_id)}
                    maxLength={35}
                    className="h-8"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="sku" className="text-sm font-medium">SKU</Label>
                    <Input
                      id="sku"
                      value={commodity?.sku || ""}
                      onChange={(e) => handleChange("sku", e.target.value)}
                      placeholder="0000001"
                      disabled={!isNone(commodity?.parent_id)}
                      maxLength={35}
                      className="h-8"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="origin_country" className="text-sm font-medium">Origin Country</Label>
                    <CountrySelect
                      value={commodity?.origin_country || ""}
                      onValueChange={(value) => handleChange("origin_country", value)}
                      placeholder="Select country"
                      disabled={!isNone(commodity?.parent_id)}
                      className="h-8"
                      noWrapper={true}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="quantity" className="text-sm font-medium">
                      Quantity <span className="text-red-500">*</span>
                    </Label>
                    <Input
                      id="quantity"
                      type="number"
                      min="1"
                      step="1"
                      value={commodity?.quantity || ""}
                      onChange={(e) => handleChange("quantity", Number(e.target.value))}
                      {...(isNone(maxQty) ? {} : { max: maxQty as number })}
                      className={`h-8 ${!isQuantityValid ? "border-red-500 focus:border-red-500" : ""}`}
                    />
                    {!isQuantityValid && maxQty && (
                      <p className="text-xs text-red-500 mt-1">
                        Quantity cannot exceed {maxQty}
                      </p>
                    )}
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="weight" className="text-sm font-medium">
                      Weight <span className="text-red-500">*</span>
                    </Label>
                    <div className="flex">
                      <Input
                        id="weight"
                        type="number"
                        min="0"
                        step="any"
                        value={commodity?.weight || ""}
                        onChange={(e) => handleChange("weight", Number(e.target.value))}
                        disabled={!isNone(commodity?.parent_id)}
                        className="h-8 rounded-r-none border-r-0"
                      />
                      <Select
                        value={commodity?.weight_unit || WeightUnitEnum.KG}
                        onValueChange={(value) => handleChange("weight_unit", value)}
                        disabled={!isNone(commodity?.parent_id)}
                      >
                        <SelectTrigger className="h-8 w-20 rounded-l-none border-l-0">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {WEIGHT_UNITS.map((unit) => (
                            <SelectItem key={unit} value={unit}>
                              {unit}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="value_amount" className="text-sm font-medium">
                      Value Amount
                    </Label>
                    <div className="flex">
                      <Input
                        id="value_amount"
                        type="number"
                        min="0"
                        step="any"
                        value={commodity?.value_amount || ""}
                        onChange={(e) => handleChange("value_amount", Number(e.target.value))}
                        disabled={!isNone(commodity?.parent_id)}
                        className="h-8 rounded-r-none border-r-0"
                      />
                      <Select
                        value={commodity?.value_currency || CurrencyCodeEnum.USD}
                        onValueChange={(value) => handleChange("value_currency", value)}
                        disabled={!isNone(commodity?.parent_id)}
                      >
                        <SelectTrigger className="h-8 w-20 rounded-l-none border-l-0">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {CURRENCY_OPTIONS.map((currency) => (
                            <SelectItem key={currency} value={currency}>
                              {currency}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="description" className="text-sm font-medium">Description</Label>
                  <Textarea
                    id="description"
                    placeholder="Item description"
                    rows={2}
                    maxLength={100}
                    value={commodity?.description || ""}
                    onChange={(e) => handleChange("description", e.target.value)}
                    disabled={!isNone(commodity?.parent_id)}
                    className="resize-none"
                  />
                </div>

                {/* Metadata Editor */}
                <EnhancedMetadataEditor
                  value={commodity?.metadata || {}}
                  onChange={(metadata) => setCommodity({ ...commodity, metadata })}
                  className="w-full"
                  placeholder="No metadata configured"
                  emptyStateMessage="Add key-value pairs to configure commodity metadata"
                  showTypeInference={true}
                  maxHeight="300px"
                />
              </div>
            </div>

            {/* Sticky Footer */}
            <DialogFooter className="px-4 py-3 border-t sticky bottom-0 bg-background">
              <Button
                type="button"
                variant="outline"
                onClick={() => setIsOpen(false)}
              >
                Cancel
              </Button>
              <Button
                type="button"
                onClick={handleFooterSubmit}
                disabled={isSubmitting || !hasChanges || missingRequired || !isQuantityValid}
              >
                {isSubmitting ? "Saving..." : (isNew ? "Add Commodity" : "Save Changes")}
              </Button>
            </DialogFooter>
          </div>
        </DialogContent>
      </Dialog>
    </>
  );
};

CommodityEditDialog.displayName = "CommodityEditDialog";