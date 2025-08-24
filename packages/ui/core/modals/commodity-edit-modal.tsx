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
} from "../forms/metadata-editor";
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
import { Notifier } from "../components/notifier";
import { Loading } from "../components/loader";
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

interface CommodityEditModalComponent {
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

export const CommodityEditModalProvider = ({
  children,
  orderFilter,
}: CommodityEditModalComponent): JSX.Element => {
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
  const [isInvalid, setIsInvalid] = useState<boolean>(false);
  const [maxQty, setMaxQty] = useState<number | null | undefined>();
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

  const handleChange = (event: React.ChangeEvent<HTMLInputElement | any>) => {
    event.preventDefault();
    const target = event.target;
    let name: string = target.name;
    let value: stateValue =
      target.type === "checkbox" ? target.checked : target.value;

    dispatch({
      name,
      value: target.type === "number" ? parseFloat(value as string) : value,
    });
  };
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    commodity.id && setLoading(true);
    operation?.onSubmit &&
      (await operation?.onSubmit(commodity as CommodityType));
    setTimeout(() => {
      commodity.id && setLoading(false);
      close();
    }, 500);
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
                onChange={(e: any) => {
                  setIsInvalid(
                    e.currentTarget.querySelectorAll(".is-danger").length > 0,
                  );
                }}
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
                        dispatch({ name: "parent_id", value });
                        if (!value) setMaxQty(undefined);
                        else {
                          // Find and load the selected line item
                          const allItems = (query.data?.orders.edges || []).map(({ node: order }) => order.line_items).flat();
                          const selectedItem = allItems.find(item => item.id === value);
                          if (selectedItem) loadLineItem(selectedItem);
                        }
                      }}
                      onUnlink={() => {
                        dispatch({ name: "parent_id", value: null });
                        setMaxQty(undefined);
                      }}
                      query={query}
                      showUnlinkButton={true}
                      placeholder="Link an order line item"
                    />
                  )}

                  <div className="space-y-2">
                    <Label htmlFor="title" className="text-sm font-medium">
                      Title <span className="text-destructive">*</span>
                    </Label>
                    <Input
                      id="title"
                      name="title"
                      placeholder="IPod Nano"
                      onChange={handleChange}
                      value={commodity?.title || ""}
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
                      name="hs_code"
                      placeholder="000000"
                      onChange={handleChange}
                      value={commodity?.hs_code || ""}
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
                        name="sku"
                        value={commodity?.sku || ""}
                        onChange={handleChange}
                        placeholder="0000001"
                        disabled={!isNone(commodity?.parent_id)}
                        maxLength={35}
                        className="h-8"
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="origin_country" className="text-sm font-medium">Origin Country</Label>
                      <CountrySelect
                        name="origin_country"
                        value={commodity.origin_country || ""}
                        onValueChange={(value) =>
                          dispatch({
                            name: "origin_country",
                            value: value as string,
                          })
                        }
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
                        Quantity <span className="text-destructive">*</span>
                      </Label>
                      <Input
                        id="quantity"
                        name="quantity"
                        type="number"
                        min="1"
                        step="1"
                        onChange={handleChange}
                        value={commodity?.quantity || ""}
                        onInvalid={validityCheck(
                          validationMessage("Please enter a valid quantity"),
                        )}
                        {...(isNone(maxQty) ? {} : { max: maxQty as number })}
                        required
                        className="h-8"
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="weight" className="text-sm font-medium">
                        Weight <span className="text-destructive">*</span>
                      </Label>
                      <div className="flex">
                        <Input
                          id="weight"
                          name="weight"
                          type="number"
                          min="0"
                          step="any"
                          onChange={handleChange}
                          value={commodity.weight || ""}
                          disabled={!isNone(commodity?.parent_id)}
                          onInvalid={validityCheck(
                            validationMessage("Please enter a valid weight"),
                          )}
                          required
                          className="h-8 rounded-r-none border-r-0"
                        />
                        <Select
                          value={commodity.weight_unit || WeightUnitEnum.KG}
                          onValueChange={(value) =>
                            dispatch({
                              name: "weight_unit",
                              value: value as WeightUnitEnum,
                            })
                          }
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
                          name="value_amount"
                          type="number"
                          min="0"
                          step="any"
                          onChange={handleChange}
                          value={commodity.value_amount || ""}
                          disabled={!isNone(commodity?.parent_id)}
                          className="h-8 rounded-r-none border-r-0"
                        />
                        <Select
                          value={commodity.value_currency || CurrencyCodeEnum.USD}
                          onValueChange={(value) =>
                            dispatch({
                              name: "value_currency",
                              value: value as CurrencyCodeEnum,
                            })
                          }
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
                      name="description"
                      placeholder="Item description"
                      rows={2}
                      maxLength={100}
                      onChange={handleChange}
                      value={commodity?.description || ""}
                      disabled={!isNone(commodity?.parent_id)}
                      className="resize-none"
                    />
                  </div>

                  {/* Advanced Fields */}
                  <Collapsible>
                    <CollapsibleTrigger asChild>
                      <Button
                        type="button"
                        variant="ghost"
                        className="flex items-center gap-2 text-sm font-medium text-blue-600 hover:text-blue-700 p-0 h-auto"
                      >
                        Advanced Options
                        <ChevronDown className="h-4 w-4" />
                      </Button>
                    </CollapsibleTrigger>
                    <CollapsibleContent className="space-y-6 mt-6 pl-4 border-l-2 border-gray-200">
                      <MetadataEditor
                        id={commodity.id}
                        object_type={MetadataObjectTypeEnum.commodity}
                        metadata={commodity.metadata}
                        onChange={(value) => dispatch({ name: "metadata", value })}
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
                      isInvalid ||
                      isEqual(operation?.commodity, commodity)
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

export function useCommodityEditModal() {
  return React.useContext(CommodityStateContext);
}
