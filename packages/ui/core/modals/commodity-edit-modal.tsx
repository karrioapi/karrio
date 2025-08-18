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
import { isEqual, isNone, validationMessage, validityCheck } from "@karrio/lib";
import { CommodityType, CURRENCY_OPTIONS, WEIGHT_UNITS } from "@karrio/types";
import React, { useContext, useReducer, useState } from "react";
import { TextareaField } from "@karrio/ui/components/textarea-field";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { LineItemInput } from "../forms/line-item-input";
import { InputField } from "@karrio/ui/components/input-field";
import { SelectField } from "@karrio/ui/components/select-field";
import { CountryInput } from "../forms/country-input";
import { Notifier } from "../components/notifier";
import { Loading } from "../components/loader";
import { useOrders } from "@karrio/hooks/order";
import {
  Dialog,
  DialogContent,
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
        <DialogContent className="max-w-3xl max-h-[95vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="text-lg font-semibold">
              {isNew ? "Add" : "Update"} commodity
            </DialogTitle>
          </DialogHeader>
          
          <div className="mt-2 pb-4">
            {commodity !== undefined && (
              <>
                <div
                  className="px-0 py-2"
                  key={key}
                  onChange={(e: any) => {
                    setIsInvalid(
                      e.currentTarget.querySelectorAll(".is-danger").length > 0,
                    );
                  }}
                >
                  {ORDERS_MANAGEMENT && (
                    <div className="flex gap-2 items-end mb-2 px-1">
                      <div className="flex-1">
                        <LineItemInput
                          name="parent_id"
                          label="Order Line Item"
                          value={commodity?.parent_id}
                          onChange={loadLineItem}
                          query={query}
                          onReady={(_: any) => setMaxQty(_?.unfulfilled_quantity)}
                          dropdownClass="is-small"
                          fieldClass="mb-0 p-0"
                          wrapperClass=""
                          className="is-small is-fullwidth"
                          placeholder="Link an order line item"
                        />
                      </div>

                      <div className="flex-shrink-0">
                        <button
                          type="button"
                          className="button is-white is-small"
                          disabled={isNone(commodity?.parent_id)}
                          title="unlink order line item"
                          onClick={() => {
                            dispatch({ name: "parent_id", value: null });
                            setMaxQty(undefined);
                          }}
                        >
                          <span className="icon is-small">
                            <i className="fas fa-unlink"></i>
                          </span>
                        </button>
                      </div>
                    </div>
                  )}

                  <div className="columns is-multiline mb-2 px-1">
                    <div className="column is-12 px-1 py-1">
                      <div className="tailwind-only">
                    <InputField
                      name="title"
                      label="Title"
                      placeholder="IPod Nano"
                      onChange={handleChange}
                      value={commodity?.title}
                      disabled={!isNone(commodity?.parent_id)}
                      max={35}
                      labelBold={true}
                    />
                      </div>
                    </div>
                  </div>

                  <div className="columns is-multiline mb-2 px-1">
                    <div className="column is-12 px-1 py-1">
                      <div className="tailwind-only">
                    <InputField
                      name="hs_code"
                      label="HS code"
                      placeholder="000000"
                      onChange={handleChange}
                      value={commodity?.hs_code}
                      disabled={!isNone(commodity?.parent_id)}
                      max={35}
                      labelBold={true}
                    />
                      </div>
                    </div>
                  </div>

                  <div className="columns is-multiline mb-2 px-1">
                    <div className="column is-7 px-1 py-1">
                      <div className="tailwind-only">
                    <InputField
                      name="sku"
                      label="SKU"
                      value={commodity?.sku}
                      onChange={handleChange}
                      placeholder="0000001"
                      disabled={!isNone(commodity?.parent_id)}
                      max={35}
                      labelBold={true}
                    />
                      </div>
                    </div>

                    <div className="column is-5 px-1 py-1">
                      <div className="tailwind-only">
                    <CountryInput
                      label="Origin Country"
                      value={commodity.origin_country}
                      onValueChange={(value) =>
                        dispatch({
                          name: "origin_country",
                          value: value as string,
                        })
                      }
                      disabled={!isNone(commodity?.parent_id)}
                      labelBold={true}
                    />
                      </div>
                    </div>
                  </div>

                                    <div className="px-1 mb-2">
                    {/* Responsive Layout: Flex on desktop (side by side), stack on mobile */}
                    <div className="tailwind-only flex flex-col sm:flex-row gap-2 items-end">
                      {/* Quantity Field - 1 flex unit */}
                      <div className="w-full sm:flex-1 min-w-0">
                        <div className="tailwind-only">
                          <InputField
                            label="Quantity"
                            name="quantity"
                            type="number"
                            min="1"
                            step="1"
                            onChange={handleChange}
                            value={commodity?.quantity}
                            onInvalid={validityCheck(
                              validationMessage("Please enter a valid quantity"),
                            )}
                            {...(isNone(maxQty) ? {} : { max: maxQty as number })}
                            required
                            labelBold={true}
                          />
                        </div>
                      </div>

                      {/* Weight Field - 1.5 flex units */}
                      <div className="w-full sm:flex-[1.5] min-w-0">
                        <div className="tailwind-only isolate py-2 px-1">
                          <label className="capitalize text-xs mb-1 block font-bold text-[0.8em]">
                            Weight
                            <span className="ml-1 text-red-500 text-xs">
                              <i className="fas fa-asterisk text-[0.7em]"></i>
                            </span>
                          </label>
                          <div className="flex">
                            <input
                              name="weight"
                              type="number"
                              min="0"
                              step="any"
                              onChange={handleChange}
                              value={commodity.weight}
                              disabled={!isNone(commodity?.parent_id)}
                              onInvalid={validityCheck(
                                validationMessage("Please enter a valid weight"),
                              )}
                              required
                              className="flex-1 min-w-0 h-9 rounded-l-md border border-r-0 border-input bg-transparent px-2 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                            />
                            <SelectField
                              name="weight_unit"
                              value={commodity.weight_unit || WeightUnitEnum.KG}
                              onChange={handleChange}
                              options={WEIGHT_UNITS}
                              disabled={!isNone(commodity?.parent_id)}
                              attachedToInput={true}
                              attachmentSide="right"
                              width="w-24"
                            />
                          </div>
                        </div>
                      </div>

                      {/* Value Amount Field - 2 flex units (largest) */}
                      <div className="w-full sm:flex-[2] min-w-0">
                        <div className="tailwind-only isolate py-2 px-1">
                          <label className="capitalize text-xs mb-1 block font-bold text-[0.8em]">
                            Value Amount
                          </label>
                          <div className="flex">
                            <input
                              name="value_amount"
                              type="number"
                              min="0"
                              step="any"
                              onChange={handleChange}
                              value={commodity.value_amount || ""}
                              disabled={!isNone(commodity?.parent_id)}
                              className="flex-1 min-w-0 h-9 rounded-l-md border border-r-0 border-input bg-transparent px-3 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
                            />
                            <SelectField
                              name="value_currency"
                              value={commodity.value_currency || CurrencyCodeEnum.USD}
                              onChange={handleChange}
                              options={CURRENCY_OPTIONS}
                              required={!isNone(commodity?.value_amount)}
                              disabled={!isNone(commodity?.parent_id)}
                              attachedToInput={true}
                              attachmentSide="right"
                              width="w-24"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="columns is-multiline mb-0 px-1">
                    <div className="column is-12 px-1 py-1">
                      <div className="tailwind-only">
                        <TextareaField
                      name="description"
                      label="description"
                      placeholder="item description"
                      rows={2}
                      maxLength={100}
                      onChange={handleChange}
                      value={commodity?.description}
                      disabled={!isNone(commodity?.parent_id)}
                      labelBold={true}
                    />
                      </div>
                    </div>
                  </div>

                  <hr className="mt-1 my-3 border-t border-border h-px" />

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
                          <div className="is-flex is-justify-content-space-between">
                            <h2 className="title is-6 my-3">Metadata</h2>

                            <button
                              type="button"
                              className="button is-default is-small is-align-self-center"
                              disabled={isEditing}
                              onClick={() => editMetadata()}
                            >
                              <span className="icon is-small">
                                <i className="fas fa-pen"></i>
                              </span>
                              <span>Edit metadata</span>
                            </button>
                          </div>

                          <hr className="mt-1 my-1 border-t border-border h-px" />
                        </>
                      );
                    })()}
                  </MetadataEditor>
                </div>

                <div className="flex justify-center gap-2 mt-4">
                  <button
                    className="button is-default is-small"
                    onClick={close}
                    disabled={loading}
                  >
                    <span>Cancel</span>
                  </button>
                  <button
                    className={`button is-primary ${loading ? "is-loading" : ""} is-small`}
                    disabled={
                      loading ||
                      isInvalid ||
                      isEqual(operation?.commodity, commodity)
                    }
                    onClick={handleSubmit}
                  >
                    <span>{isNew ? "Add" : "Save"}</span>
                  </button>
                </div>
              </>
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
