"use client";
import {
  CommodityEditModalProvider,
  CommodityStateContext,
} from "@karrio/ui/core/modals/commodity-edit-modal";
import {
  MetadataEditor,
  MetadataEditorContext,
} from "@karrio/ui/components/metadata-editor";
import { GoogleGeocodingScript } from "@karrio/ui/core/components/google-geocoding-script";
import { CommodityDescription } from "@karrio/ui/components/commodity-description";
import { AddressDescription } from "@karrio/ui/components/address-description";
import { formatRef, isEqual, isNone, isNoneOrEmpty } from "@karrio/lib";
import { AddressModalEditor } from "@karrio/ui/components/address-modal-editor";
import { MetadataObjectTypeEnum, PaidByEnum } from "@karrio/types";
import { InputField } from "@karrio/ui/components/input-field";
import { DateInput } from "@karrio/ui/components/date-input";
import { RadioGroupField } from "@karrio/ui/components/radio-group-field";
import { ButtonField } from "@karrio/ui/components/button-field";
import { useLoader } from "@karrio/ui/core/components/loader";
import { ModalProvider } from "@karrio/ui/core/modals/modal";
import { bundleContexts } from "@karrio/hooks/utils";
import { Spinner } from "@karrio/ui/core/components";
import { useOrderForm } from "@karrio/hooks/order";
import React, { useEffect, useState } from "react";
import { AddressType } from "@karrio/types";
import { Plus, Edit, X } from "lucide-react";

const ContextProviders = bundleContexts([
  CommodityEditModalProvider,
  ModalProvider,
]);

export default function Page(pageProps: any) {
  const Component = (): JSX.Element => {
    const params = pageProps.params || {};
    const { id } = params;
    const loader = useLoader();
    const [ready, setReady] = useState<boolean>(false);
    const [loading, setLoading] = useState<boolean>(false);
    const [key, setKey] = useState<string>(`order-${Date.now()}`);


    const { order, current, isNew, DEFAULT_STATE, query, ...mutation } =
      useOrderForm({ id });

    const handleChange = async (changes?: Partial<typeof order>) => {
      if (changes === undefined) {
        return;
      }
      await mutation.updateOrder({ id, ...changes });
      setKey(`${id}-${Date.now()}`);
    };
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
        <CommodityEditModalProvider orderFilter={{ isDisabled: true }}>
          <header className="px-0 pb-2 pt-4 flex justify-between items-center">
            <span className="text-2xl font-semibold my-2">{`${id === "new" ? "Create" : "Edit"} order`}</span>
            <div>
              <ButtonField
                type="button"
                isSuccess
                isSmall
                onClick={() => mutation.save()}
                loading={loader.loading}
                disabled={
                  isEqual(order, current || DEFAULT_STATE) ||
                  !order?.shipping_to?.country_code
                }
              >
                Save
              </ButtonField>
            </div>
          </header>

          {!ready && <Spinner />}

          {ready && (
            <div className="flex flex-col lg:flex-row gap-6 pb-6">
              <div className="flex-1 lg:flex-[7] px-0 lg:min-h-[850px]">
                {/* Line Items */}
                <div className="rounded-xl border bg-card text-card-foreground shadow px-0 py-3">
                  <header className="px-3 flex justify-between">
                    <span className="text-xs font-bold uppercase tracking-wide text-gray-700 flex items-center my-2">
                      LINE ITEMS
                    </span>
                    <div className="flex items-center">
                      {/* @ts-ignore */}
                      <CommodityStateContext.Consumer>
                        {({ editCommodity }) => (
                          <ButtonField
                            type="button"
                            variant="link"
                            size="sm"
                            disabled={query.isFetching}
                            onClick={() =>
                              editCommodity({
                                onSubmit: (_) => mutation.addItem(_),
                              })
                            }
                            leftIcon={<Plus className="h-4 w-4" />}
                            className="text-blue-600 hover:text-blue-800 p-2 h-auto"
                          >
                            add item
                          </ButtonField>
                        )}
                      </CommodityStateContext.Consumer>
                    </div>
                  </header>

                  <hr className="my-1" style={{ height: "1px" }} />

                  <div className="p-3">
                    {(order.line_items || []).map((item, index) => (
                      <React.Fragment key={index + "customs-info"}>
                        {index > 0 && (
                          <hr className="my-1" style={{ height: "1px" }} />
                        )}
                        <div className="flex justify-between items-center">
                          <CommodityDescription
                            className="flex-grow pr-2"
                            commodity={item as any}
                          />
                          <div>
                            {/* @ts-ignore */}
                            <CommodityStateContext.Consumer>
                              {({ editCommodity }) => (
                                <ButtonField
                                  type="button"
                                  variant="ghost"
                                  size="sm"
                                  onClick={() =>
                                    editCommodity({
                                      commodity: item as any,
                                      onSubmit: (_) =>
                                        mutation.updateItem(index, item.id)(_),
                                    })
                                  }
                                >
                                  <Edit className="h-4 w-4" />
                                </ButtonField>
                              )}
                            </CommodityStateContext.Consumer>
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
                      defaultValue={order.order_date || ""}
                      onChange={(e) =>
                        handleChange({ order_date: e.target.value })
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
                      gap="gap-4"
                      wrapperClass="p-0 mb-3"
                      labelBold={true}
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
                <div
                  style={{ position: "sticky", top: "8.5%", right: 0, left: 0 }}
                >
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
                            <span>
                              {(order.line_items || []).reduce(
                                (_, { quantity, value_amount }) =>
                                  _ +
                                  (isNone(quantity) ? 1 : (quantity as any)) *
                                  (isNone(value_amount)
                                    ? 1.0
                                    : (value_amount as any)),
                                0.0,
                              )}{" "}
                              {(order.line_items || [])[0]?.value_currency}
                            </span>
                          }
                        </p>
                        <p className="font-semibold text-xs">
                          TOTAL WEIGHT:{" "}
                          {
                            <span>
                              {(order.line_items || []).reduce(
                                (_, { quantity, weight }) =>
                                  _ +
                                  (isNone(quantity) ? 1 : (quantity as any)) *
                                  (isNone(weight) ? 1.0 : (weight as any)),
                                0.0,
                              )}{" "}
                              {(order.line_items || [])[0]?.weight_unit}
                            </span>
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
                          <AddressModalEditor
                            shipment={order as any}
                            address={order.shipping_to as AddressType}
                            onSubmit={(address) =>
                              handleChange({ shipping_to: address })
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
                          <AddressModalEditor
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
                    <div className="p-1 pb-4">
                      <MetadataEditor
                        object_type={MetadataObjectTypeEnum.order}
                        metadata={order.metadata}
                        onChange={(metadata) => handleChange({ metadata })}
                      >
                        {/* @ts-ignore */}
                        <MetadataEditorContext.Consumer>
                          {({ isEditing, editMetadata }) => (
                            <>
                              <header className="flex justify-between p-2">
                                <span className="text-xs font-bold uppercase tracking-wide text-gray-700 flex items-center my-2">
                                  METADATA
                                </span>
                                <div className="flex items-center">
                                  <ButtonField
                                    type="button"
                                    variant="link"
                                    size="sm"
                                    disabled={loading}
                                    onClick={() => editMetadata()}
                                    className="text-blue-600 hover:text-blue-800 p-1 h-auto"
                                  >
                                    Edit metadata
                                  </ButtonField>
                                </div>
                              </header>
                            </>
                          )}
                        </MetadataEditorContext.Consumer>
                      </MetadataEditor>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </CommodityEditModalProvider>
      </>
    );
  };

  return (
    <>
      <GoogleGeocodingScript />
      <ContextProviders>
        <Component />
      </ContextProviders>
    </>
  );
}