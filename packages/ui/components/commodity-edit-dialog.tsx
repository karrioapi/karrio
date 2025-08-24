import {
  CurrencyCodeEnum,
  DEFAULT_COMMODITY_CONTENT,
  MetadataObjectTypeEnum,
  OrderFilter,
  WeightUnitEnum,
} from "@karrio/types";
import {
  MetadataEditor,
  MetadataEditorContext,
} from "@karrio/ui/core/forms/metadata-editor";
import { isEqual, isNone, validationMessage, validityCheck, formatOrderLineItem } from "@karrio/lib";
import { CommodityType, CURRENCY_OPTIONS, WEIGHT_UNITS } from "@karrio/types";
import React, { useContext, useReducer, useState } from "react";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { InputField } from "@karrio/ui/components/input-field";
import { SelectField } from "@karrio/ui/core/components";
import { ButtonField } from "@karrio/ui/components/button-field";
import { TextareaField } from "@karrio/ui/components/textarea-field";
import { LineItemInput } from "@karrio/ui/components/line-item-input";
import { Button } from "@karrio/ui/components/ui/button";
import { Input } from "@karrio/ui/components/ui/input";
import { Label } from "@karrio/ui/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@karrio/ui/components/ui/select";
import { CountrySelect } from "@karrio/ui/components/country-select";
import { Textarea } from "@karrio/ui/components/ui/textarea";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@karrio/ui/components/ui/collapsible";
import { ChevronDown, ChevronUp } from "lucide-react";
import { cn } from "@karrio/ui/lib/utils";
import { Notifier } from "@karrio/ui/core/components/notifier";
import { Loading } from "@karrio/ui/core/components/loader";
import { useOrders } from "@karrio/hooks/order";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@karrio/ui/components/ui/dialog";

type OperationType = {
  commodity?: CommodityType;
  onSubmit: (commodity: CommodityType) => Promise<any>;
};
type CommodityStateContextType = {
  editCommodity: (operation: OperationType) => void;
};
type stateValue = string | boolean | Partial<CommodityType> | undefined | null;

export const CommodityStateContext =
  React.createContext<CommodityStateContextType>(
    {} as CommodityStateContextType,
  );

interface CommodityEditDialogComponent {
  children?: React.ReactNode;
  orderFilter?: OrderFilter & { isDisabled?: boolean; cacheKey?: string };
}

function reducer(
  state: any,
  { name, value }: { name: string; value: stateValue | number | boolean },
) {
  switch (name) {
    case "partial":
      return isNone(value)
        ? undefined
        : { ...(state || {}), ...(value as CommodityType) };
    case "value_amount":
      const value_currency = isNone(value)
        ? state.value_currency
        : CurrencyCodeEnum.USD;
      return { ...state, [name]: value, value_currency };
    default:
      return { ...state, [name]: value };
  }
}

export const CommodityEditDialogProvider = ({
  children,
  orderFilter,
}: CommodityEditDialogComponent): JSX.Element => {
  const {
    metadata: { ORDERS_MANAGEMENT },
    references,
  } = useAPIMetadata();
  const { loading, setLoading } = useContext(Loading);
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [key, setKey] = useState<string>(`commodity-${Date.now()}`);
  const [isNew, setIsNew] = useState<boolean>(true);
  const [commodity, dispatch] = useReducer(
    reducer,
    undefined,
    () => DEFAULT_COMMODITY_CONTENT,
  );
  const [operation, setOperation] = useState<OperationType | undefined>();
  const [maxQty, setMaxQty] = useState<number | null | undefined>();
  const [advancedExpanded, setAdvancedExpanded] = useState(false);
  
  const { query } = useOrders({
    first: 10,
    status: ["unfulfilled", "partial"] as any,
    isDisabled: !ORDERS_MANAGEMENT,
    ...(orderFilter || {}),
  });

  const editCommodity = (operation: OperationType) => {
    const commodity =
      operation.commodity || (DEFAULT_COMMODITY_CONTENT as CommodityType);

    setIsOpen(true);
    setOperation(operation);
    setIsNew(isNone(operation.commodity));
    dispatch({ name: "partial", value: commodity });
    setKey(`commodity-${Date.now()}`);
  };
  
  const close = () => {
    setIsOpen(false);
    setOperation(undefined);
    dispatch({ name: "partial", value: undefined });
  };

  const handleChange = (field: string, fieldValue: string | number | boolean | null) => {
    dispatch({ name: field, value: fieldValue });
  };

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!operation?.onSubmit) return;

    commodity.id && setLoading(true);
    try {
      await operation.onSubmit(commodity as CommodityType);
      setTimeout(() => {
        commodity.id && setLoading(false);
        close();
      }, 500);
    } catch (error) {
      setLoading(false);
      console.error('Commodity submission error:', error);
    }
  };
  
  const loadLineItem = (item?: CommodityType | any) => {
    const {
      id: parent_id,
      unfulfilled_quantity: quantity,
      ...content
    } = item || { id: null };
    setMaxQty(quantity);
    dispatch({ name: "partial", value: { ...content, parent_id, quantity } });
  };

  // Validation logic similar to address form
  const missingRequired = !commodity?.title || !commodity?.quantity || !commodity?.weight;
  const hasChanges = !isEqual(operation?.commodity, commodity) || (
    commodity?.title || commodity?.quantity || commodity?.weight
  );
  
  // Quantity validation
  const isQuantityValid = !maxQty || !commodity?.quantity || commodity.quantity <= maxQty;

  return (
    <Notifier>
      <CommodityStateContext.Provider value={{ editCommodity }}>
        {children}
      </CommodityStateContext.Provider>

      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="max-w-2xl max-h-[90vh] p-0 flex flex-col">
          {/* Sticky Header */}
          <DialogHeader className="px-4 py-3 border-b sticky top-0 bg-background z-5">
            <DialogTitle>
              {isNew ? "Add" : "Update"} commodity
            </DialogTitle>
          </DialogHeader>

          <div className="flex flex-col flex-1 min-h-0">
            {commodity !== undefined && (
              <form
                className="flex flex-col flex-1 min-h-0"
                key={key}
                onSubmit={handleSubmit}
              >
                {/* Scrollable Body */}
                <div className="flex-1 overflow-y-auto px-4 py-3">
                  <div className="space-y-6">
                  {ORDERS_MANAGEMENT && (
                    <LineItemInput
                      label="Order Line Item"
                      value={commodity?.parent_id || null}
                      onValueChange={(value) => {
                        handleChange("parent_id", value);
                        if (!value) setMaxQty(undefined);
                        else {
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
                      placeholder="IPod Nano"
                      value={commodity?.title || ""}
                      onChange={(e) => handleChange("title", e.target.value)}
                      disabled={!isNone(commodity?.parent_id)}
                      maxLength={35}
                      required
                      className="h-8"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="hs_code" className="text-sm font-medium">HS Code</Label>
                    <Input
                      id="hs_code"
                      placeholder="000000"
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
                        required
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
                          required
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

                  {/* Advanced Fields */}
                  <Collapsible open={advancedExpanded} onOpenChange={setAdvancedExpanded}>
                    <CollapsibleTrigger asChild>
                      <Button
                        type="button"
                        variant="ghost"
                        className="flex items-center gap-2 text-sm font-medium text-blue-600 hover:text-blue-700 p-0 h-auto"
                      >
                        Advanced Options
                        {advancedExpanded ? (
                          <ChevronUp className="h-4 w-4" />
                        ) : (
                          <ChevronDown className="h-4 w-4" />
                        )}
                      </Button>
                    </CollapsibleTrigger>
                    <CollapsibleContent className="space-y-6 mt-6 pl-4 border-l-2 border-gray-200">
                      <MetadataEditor
                        id={commodity?.id}
                        object_type={MetadataObjectTypeEnum.commodity}
                        metadata={commodity?.metadata}
                        onChange={(value) => handleChange("metadata", value)}
                      >
                        {(() => {
                          const { isEditing, editMetadata } = useContext(
                            MetadataEditorContext,
                          );

                          return (
                            <>
                              <div className="flex justify-between">
                                <Label className="text-sm font-medium">Metadata</Label>

                                <Button
                                  type="button"
                                  variant="link"
                                  size="sm"
                                  disabled={isEditing}
                                  onClick={() => editMetadata()}
                                  className="text-blue-600 hover:text-blue-800 p-1 h-auto"
                                >
                                  Edit metadata
                                </Button>
                              </div>
                            </>
                          );
                        })()}
                      </MetadataEditor>
                    </CollapsibleContent>
                  </Collapsible>

                  </div>
                </div>

                {/* Sticky Footer */}
                <DialogFooter className="px-4 py-3 border-t sticky bottom-0 bg-background z-5">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={close}
                    disabled={loading}
                  >
                    Cancel
                  </Button>
                  <Button
                    type="submit"
                    disabled={
                      loading ||
                      !hasChanges ||
                      missingRequired ||
                      !isQuantityValid
                    }
                  >
                    {loading ? "Saving..." : (isNew ? "Add" : "Save")}
                  </Button>
                </DialogFooter>
              </form>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </Notifier>
  );
};

export function useCommodityEditDialog() {
  return React.useContext(CommodityStateContext);
}