"use client";
import { CommodityEditDialog } from "@karrio/ui/components/commodity-edit-dialog";
import { EnhancedMetadataEditor } from "@karrio/ui/components/enhanced-metadata-editor";
import { GoogleGeocodingScript } from "@karrio/ui/core/components/google-geocoding-script";
import { CommodityDescription } from "@karrio/ui/components/commodity-description";
import { AddressDescription } from "@karrio/ui/components/address-description";
import { formatRef, isEqual, isNone, isNoneOrEmpty } from "@karrio/lib";
import { AddressEditDialog } from "@karrio/ui/components/address-edit-dialog";
import { PaidByEnum } from "@karrio/types";
import { InputField } from "@karrio/ui/components/input-field";
import { DateInput } from "@karrio/ui/components/date-input";
import { RadioGroupField } from "@karrio/ui/components/radio-group-field";
import { ButtonField } from "@karrio/ui/components/button-field";
import { useLoader } from "@karrio/ui/core/components/loader";
import { Spinner } from "@karrio/ui/core/components";
import { useOrderForm } from "@karrio/hooks/order";
import React, { useEffect, useState } from "react";
import { AddressType } from "@karrio/types";
import { Plus, Edit, X, AlertTriangle } from "lucide-react";

// Weight conversion rates to KG
const convertToKG = (weight: number, unit: string): number => {
  switch (unit) {
    case 'G': return weight / 1000;
    case 'KG': return weight;
    case 'LB': return weight * 0.453592;
    case 'OZ': return weight * 0.0283495;
    default: return weight; // fallback
  }
};

// Simplified utility to analyze weight units
const analyzeWeightUnits = (lineItems: any[]) => {
  if (!lineItems || lineItems.length === 0) {
    return { units: [], type: 'empty' };
  }

  const weightUnits = Array.from(new Set(
    lineItems.map(item => item.weight_unit).filter(unit => !isNone(unit))
  ));

  // Same unit or no units
  if (weightUnits.length <= 1) {
    return { units: weightUnits, type: 'single' };
  }

  // Any mixed units - convert all to KG
  return { units: weightUnits, type: 'mixed' };
};


export default function Page(pageProps: { params: Promise<{ id?: string }> }) {
  const Component = (): JSX.Element => {
    const params = React.use(pageProps.params || Promise.resolve({}));
    const { id } = params;
    const loader = useLoader();
    const [ready, setReady] = useState<boolean>(false);
    const [loading, setLoading] = useState<boolean>(false);
    const [key, setKey] = useState<string>(`order-${Date.now()}`);
    const [errorsExpanded, setErrorsExpanded] = useState<boolean>(false);

    const { order, current, isNew, DEFAULT_STATE, query, ...mutation } =
      useOrderForm({ id });

    const handleChange = async (changes?: Partial<typeof order>) => {
      if (changes === undefined) {
        return;
      }
      await mutation.updateOrder({ id, ...changes });
      setKey(`${id}-${Date.now()}`);
    };

    // Helper function to analyze currencies in line items
    const analyzeCurrencies = () => {
      if (!order?.line_items || order.line_items.length === 0) {
        return { currencies: [], hasMixedCurrencies: false, hasValues: false };
      }
      
      const itemsWithValues = order.line_items.filter(
        item => item.value_currency && item.value_amount && item.value_amount > 0
      );
      
      if (itemsWithValues.length === 0) {
        return { currencies: [], hasMixedCurrencies: false, hasValues: false };
      }
      
      const currencies = Array.from(new Set(
        itemsWithValues.map(item => item.value_currency)
      ));
      
      return {
        currencies,
        hasMixedCurrencies: currencies.length > 1,
        hasValues: true
      };
    };

    // Currency validation logic
    const getCurrencyValidationErrors = () => {
      const errors: string[] = [];
      const { hasMixedCurrencies } = analyzeCurrencies();
      
      if (hasMixedCurrencies) {
        errors.push("Please standardize currency - your order contains items with different currencies");
      }
      
      return errors;
    };

    // Validation logic
    const getValidationErrors = () => {
      const errors: string[] = [];
      
      // Check shipping address
      if (!order?.shipping_to?.country_code) {
        errors.push("Shipping address is required");
      }
      
      // Check line items
      if (!order?.line_items || order.line_items.length === 0) {
        errors.push("At least one line item is required");
      } else {
        order.line_items.forEach((item, index) => {
          if (!item.title) {
            errors.push(`Line item ${index + 1}: Title is required`);
          }
          if (!item.quantity || item.quantity <= 0) {
            errors.push(`Line item ${index + 1}: Quantity is required`);
          }
          if (!item.weight || item.weight <= 0) {
            errors.push(`Line item ${index + 1}: Weight is required`);
          }
          if (!item.origin_country) {
            errors.push(`Line item ${index + 1}: Origin country is required`);
          }
        });
      }
      
      return errors;
    };

    const validationErrors = [...getValidationErrors(), ...getCurrencyValidationErrors()];
    useEffect(() => {
      if (
        !ready &&
        query.isFetched &&
        id === "new" &&
        !isNone(order.line_items)
      ) {
        setTimeout(() => setReady(true), 1000);
      }
      if (
        !ready &&
        query.isFetched &&
        !isNoneOrEmpty(id) &&
        id !== "new" &&
        !isNone(order.line_items)
      ) {
        setReady(true);
      }
    }, [query.isFetched, id]);
    useEffect(() => {
      if (ready) {
        setKey(`order-${id}-${Date.now()}`);
      }
    }, [ready]);


    return (
      <>
        <header className="px-0 pb-2 pt-4 flex justify-between items-center">
          <span className="text-2xl font-semibold my-2">{`${id === "new" ? "Draft" : "Edit"} order`}</span>
          <div>
            <ButtonField
              type="button"
              isSuccess
              isSmall
              onClick={() => mutation.save()}
              loading={loader.loading}
              disabled={
                isEqual(order, current || DEFAULT_STATE) ||
                validationErrors.length > 0
              }
            >
              Save
            </ButtonField>
          </div>
        </header>

        {/* Error Summary - Message Box */}
        {ready && validationErrors.length > 0 && (
          <div className="mb-4">
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg backdrop-blur-sm overflow-hidden">
              <div className="p-4">
                <div className="flex items-start gap-3">
                  <AlertTriangle className="h-5 w-5 text-yellow-600 mt-0.5 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <h3 className="text-sm font-medium text-yellow-800 mb-2">
                      Please address the following errors before saving:
                    </h3>
                    <ul className={`text-sm text-yellow-700 space-y-1 list-disc list-inside ${
                      errorsExpanded || validationErrors.length <= 3 
                        ? '' 
                        : 'max-h-16 overflow-y-auto'
                    }`}>
                      {validationErrors.map((error, index) => (
                        <li key={index}>{error}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
              {(!errorsExpanded && validationErrors.length > 3) && (
                <div 
                  className="bg-yellow-100 border-t border-yellow-200 px-4 py-1.5 cursor-pointer hover:bg-yellow-150 transition-colors"
                  onClick={() => setErrorsExpanded(!errorsExpanded)}
                >
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-yellow-700">
                      {`${validationErrors.length - 3} more error${validationErrors.length - 3 > 1 ? 's' : ''} - Click to view all`}
                    </span>
                    <span className="text-yellow-700 text-xs">
                      ▼
                    </span>
                  </div>
                </div>
              )}
              {errorsExpanded && validationErrors.length > 3 && (
                <div 
                  className="bg-yellow-100 border-t border-yellow-200 px-4 py-1.5 cursor-pointer hover:bg-yellow-150 transition-colors"
                  onClick={() => setErrorsExpanded(!errorsExpanded)}
                >
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-yellow-700">
                      Click to collapse errors
                    </span>
                    <span className="text-yellow-700 text-xs">
                      ▲
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {!ready && <Spinner />}

        {ready && (
          <div className="flex flex-col lg:flex-row gap-6 pb-5">
            <div className="flex-1 lg:flex-[7] px-0">
              {/* Line Items */}
              <div className="rounded-xl border bg-card text-card-foreground shadow px-0 py-3">
                <header className="px-3 flex justify-between">
                  <span className="text-xs font-bold uppercase tracking-wide text-gray-700 flex items-center my-2">
                    LINE ITEMS
                  </span>
                  <div className="flex items-center">
                    <CommodityEditDialog
                      trigger={
                        <ButtonField
                          type="button"
                          variant="link"
                          size="sm"
                          disabled={query.isFetching}
                          leftIcon={<Plus className="h-4 w-4" />}
                          className="text-blue-600 hover:text-blue-800 p-2 h-auto"
                        >
                          add item
                        </ButtonField>
                      }
                      onSubmit={(_) => mutation.addItem(_ as any)}
                      disableOrderLinking={true}
                    />
                  </div>
                </header>

                <hr className="my-1" style={{ height: "1px" }} />

                <div className="p-3">
                  {(order.line_items || []).map((item, index) => (
                    <React.Fragment key={index + "customs-info"}>
                      {index > 0 && (
                        <hr className="my-1" style={{ height: "1px" }} />
                      )}
                      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2">
                        <CommodityDescription
                          className="flex-1 min-w-0"
                          commodity={item as any}
                        />
                        <div className="flex justify-end sm:justify-start gap-1 flex-shrink-0">
                          <CommodityEditDialog
                            trigger={
                              <ButtonField
                                type="button"
                                variant="ghost"
                                size="sm"
                              >
                                <Edit className="h-4 w-4" />
                              </ButtonField>
                            }
                            commodity={item as any}
                            onSubmit={(_) => mutation.updateItem(index, item.id)(_ as any)}
                            disableOrderLinking={true}
                          />
                          <ButtonField
                            type="button"
                            variant="ghost"
                            size="sm"
                            disabled={
                              query.isFetching ||
                              (order.line_items || []).length === 1
                            }
                            onClick={() =>
                              mutation.deleteItem(index, item?.id)()
                            }
                          >
                            <X className="h-4 w-4" />
                          </ButtonField>
                        </div>
                      </div>
                    </React.Fragment>
                  ))}

                  {(order.line_items || []).length === 0 && (
                    <div className="m-2 bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-2 rounded text-xs">
                      Add one or more product to create a order.
                    </div>
                  )}
                </div>
              </div>

              {/* Order options section */}
              <div className="rounded-xl border bg-card text-card-foreground shadow px-0 py-3 mt-5">
                <header className="px-3 flex justify-between">
                  <span className="text-xs font-bold uppercase tracking-wide text-gray-700 flex items-center my-2">
                    OPTIONS
                  </span>
                </header>

                <hr className="my-1" style={{ height: "1px" }} />

                <div className="p-3 pb-0">
                  {/* order date */}
                  <DateInput
                    name="order_date"
                    label="order date"
                    wrapperClass="w-full sm:w-1/3 mb-2"
                    labelBold={true}
                    defaultValue={order.options?.order_date || ""}
                    onChange={(e) =>
                      handleChange({
                        options: {
                          ...order.options,
                          order_date: e.target.value,
                        },
                      })
                    }
                  />

                  {/* invoice */}
                  <InputField
                    label="invoice number"
                    name="invoice_number"
                    placeholder="invoice number"
                    autoComplete="off"
                    wrapperClass="w-full sm:w-1/3 mb-2"
                    labelBold={true}
                    defaultValue={order.options?.invoice_number || ""}
                    onChange={(e) =>
                      handleChange({
                        options: {
                          ...order.options,
                          invoice_number: e.target.value,
                        },
                      })
                    }
                  />

                  {/* invoice date */}
                  <DateInput
                    name="invoice_date"
                    label="invoice date"
                    wrapperClass="w-full sm:w-1/3 mb-2"
                    labelBold={true}
                    defaultValue={order.options?.invoice_date || ""}
                    onChange={(e) =>
                      handleChange({
                        options: {
                          ...order.options,
                          invoice_date: e.target.value,
                        },
                      })
                    }
                  />
                </div>

                <hr className="my-1" style={{ height: "1px" }} />

                <div className="p-3">
                  <RadioGroupField
                    label="Shipment Paid By"
                    name="paid_by"
                    value={order.options?.paid_by}
                    onValueChange={(value) =>
                      handleChange({
                        options: {
                          ...order.options,
                          paid_by: value as PaidByEnum,
                        },
                      })
                    }
                    options={[
                      {
                        value: PaidByEnum.sender,
                        label: formatRef(PaidByEnum.sender.toString()),
                      },
                      {
                        value: PaidByEnum.recipient,
                        label: formatRef(PaidByEnum.recipient.toString()),
                      },
                      {
                        value: PaidByEnum.third_party,
                        label: formatRef(PaidByEnum.third_party.toString()),
                      },
                    ]}
                    orientation="horizontal"
                    className="p-0 mb-3"
                  />

                  {order.options?.paid_by &&
                    order.options?.paid_by !== PaidByEnum.sender && (
                      <div
                        className="ml-1 px-2 py-0 border-l-2 border-gray-300"
                      >
                        <InputField
                          label="account number"
                          labelBold={true}
                          defaultValue={
                            order?.options?.account_number as string
                          }
                          onChange={(e) =>
                            handleChange({
                              options: {
                                ...order.options,
                                account_number: e.target.value,
                              },
                            })
                          }
                        />
                      </div>
                    )}
                </div>
              </div>
            </div>

            <div className="flex-1 lg:flex-[5] px-0 pb-6 relative">
                {/* Summary section */}
                {!isNone(order.line_items) && (
                  <div className="rounded-xl border bg-card text-card-foreground shadow px-0 py-3 mb-5">
                    <header className="px-3 flex justify-between">
                      <span className="text-xs font-bold uppercase tracking-wide text-gray-700 flex items-center my-2">
                        SUMMARY
                      </span>
                    </header>

                    <div className="p-0 pb-1">
                      <p className="text-xs font-semibold px-3 uppercase tracking-wide text-gray-700">
                        {`ITEMS (${(order.line_items || []).reduce((_, { quantity }) => _ + (isNone(quantity) ? 1 : (quantity as any)), 0)})`}
                      </p>

                      <div
                        className="px-3 py-1"
                        style={{ maxHeight: "14em", overflow: "auto" }}
                      >
                        {(order.line_items || []).map((item, index) => (
                          <React.Fragment key={index + "parcel-info"}>
                            <hr className="my-1" style={{ height: "1px" }} />
                            <CommodityDescription commodity={item as any} />
                          </React.Fragment>
                        ))}
                      </div>
                    </div>

                    <footer className="px-3 py-1">
                      <p className="font-semibold text-xs">
                        TOTAL:{" "}
                        {
                          (() => {
                            const { hasMixedCurrencies, hasValues, currencies } = analyzeCurrencies();
                            
                            // If no items have values, show 0
                            if (!hasValues) {
                              return <span>0</span>;
                            }
                            
                            // If mixed currencies, show warning message
                            if (hasMixedCurrencies) {
                              return <span className="text-yellow-600">Mixed currencies</span>;
                            }
                            
                            // Single currency - calculate normally
                            const total = (order.line_items || []).reduce(
                              (sum, { quantity, value_amount }) =>
                                sum +
                                (isNone(quantity) ? 1 : (quantity as any)) *
                                (isNone(value_amount) ? 0 : (value_amount as any)),
                              0.0,
                            );
                            
                            return <span>{total} {currencies[0]}</span>;
                          })()
                        }
                      </p>
                      <p className="font-semibold text-xs">
                        TOTAL WEIGHT:{" "}
                        {
                          (() => {
                            const items = order.line_items || [];
                            if (items.length === 0) return <span>0</span>;

                            const { type, units } = analyzeWeightUnits(items);

                            // Same unit or no units - keep original unit
                            if (type === 'single' || type === 'empty') {
                              const totalWeight = items.reduce(
                                (total, { quantity, weight }) =>
                                  total +
                                  (isNone(quantity) ? 1 : (quantity as any)) *
                                  (isNone(weight) ? 1.0 : (weight as any)),
                                0.0,
                              );
                              return <span>{totalWeight} {units[0] || items[0]?.weight_unit}</span>;
                            }

                            // Mixed units - convert all to KG
                            if (type === 'mixed') {
                              const totalWeightInKG = items.reduce(
                                (total, { quantity, weight, weight_unit }) => {
                                  const qty = isNone(quantity) ? 1 : (quantity as any);
                                  const wt = isNone(weight) ? 1.0 : (weight as any);
                                  const itemWeight = qty * wt;

                                  // Convert to KG using universal converter
                                  return total + convertToKG(itemWeight, weight_unit || 'KG');
                                },
                                0.0,
                              );
                              return <span>{parseFloat(totalWeightInKG.toFixed(3))} KG</span>;
                            }

                            // Fallback
                            return <span>0</span>;
                          })()
                        }
                      </p>
                    </footer>
                  </div>
                )}

                {/* Address section */}
                <div className="rounded-xl border bg-card text-card-foreground shadow px-0 py-1">
                  <div className="p-3">
                    <header className="flex justify-between">
                      <span className="text-xs font-bold uppercase tracking-wide text-gray-700 flex items-center my-2">
                        Customer
                      </span>
                      <div className="flex items-center">
                        <AddressEditDialog
                          shipment={order as any}
                          address={order.shipping_to as AddressType}
                          onSubmit={(address) =>
                            handleChange({ shipping_to: address as any })
                          }
                          trigger={
                            <ButtonField
                              variant="link"
                              size="sm"
                              disabled={loading}
                              className="text-blue-600 hover:text-blue-800 p-1 h-auto"
                            >
                              Edit address
                            </ButtonField>
                          }
                        />
                      </div>
                    </header>

                    {Object.values(order.shipping_to || {}).length > 0 && (
                      <AddressDescription
                        address={order.shipping_to as AddressType}
                      />
                    )}

                    {Object.values(order.shipping_to || {}).length === 0 && (
                      <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 mt-2 mb-5 py-2 px-4 text-xs rounded">
                        Please specify the customer address.
                      </div>
                    )}

                    <hr className="my-0 mb-3" style={{ height: "1px" }} />

                    <header className="flex justify-between">
                      <span className="text-xs font-bold uppercase tracking-wide text-gray-700 flex items-center my-2">
                        Billing Address
                      </span>
                      <div className="flex items-center">
                        <AddressEditDialog
                          shipment={order as any}
                          address={order.billing_address as AddressType}
                          onSubmit={(address) =>
                            handleChange({ billing_address: address })
                          }
                          trigger={
                            <ButtonField
                              variant="link"
                              size="sm"
                              disabled={loading}
                              className="text-blue-600 hover:text-blue-800 p-1 h-auto"
                            >
                              Edit billing address
                            </ButtonField>
                          }
                        />
                      </div>
                    </header>

                    {Object.values(order.billing_address || {}).length >
                      0 && (
                        <AddressDescription
                          address={order.billing_address as AddressType}
                        />
                      )}

                    {Object.values(order.billing_address || {}).length ===
                      0 && (
                        <>
                          <div className="mt-2 mb-4 bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-2 rounded text-xs">
                            The shipping address will be used for billing. Click <span className="font-semibold">Edit billing address</span> if the billing address is different.
                          </div>
                          <div className="bg-gray-50 border border-gray-200 text-gray-700 my-2 py-2 px-4 text-xs rounded">
                            Same as shipping address.
                          </div>
                        </>
                      )}
                  </div>
                </div>

                {/* Metadata section */}
                <div className="rounded-xl border bg-card text-card-foreground shadow px-2 py-1 mt-5">
                  <div className="p-2 pb-3">
                    <EnhancedMetadataEditor
                      value={order.metadata || {}}
                      onChange={(metadata) => handleChange({ metadata })}
                      className="w-full"
                      placeholder="No metadata configured"
                      emptyStateMessage="Add key-value pairs to configure order metadata"
                      allowEdit={!loading}
                      showTypeInference={true}
                      maxHeight="300px"
                    />
                  </div>
                </div>
            </div>
          </div>
        )}
      </>
    );
  };

  return (
    <>
      <GoogleGeocodingScript />
      <Component />
    </>
  );
}
