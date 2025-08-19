"use client";
import {
  CommodityEditModalProvider,
  CommodityStateContext,
} from "@karrio/ui/core/modals/commodity-edit-modal";
import {
  MetadataEditor,
  MetadataEditorContext,
} from "@karrio/ui/core/forms/metadata-editor";
import { GoogleGeocodingScript } from "@karrio/ui/core/components/google-geocoding-script";
import { CommodityDescription } from "@karrio/ui/components/commodity-description";
import { AddressDescription } from "@karrio/ui/components/address-description";
import { formatRef, isEqual, isNone, isNoneOrEmpty } from "@karrio/lib";
import { AddressModalEditor } from "@karrio/ui/components/address-modal-editor";
import { MetadataObjectTypeEnum, PaidByEnum } from "@karrio/types";
import { InputField } from "@karrio/ui/components/input-field";
import { RadioGroupField } from "@karrio/ui/components/radio-group-field";
import { ButtonField } from "@karrio/ui/components/button-field";
import { useLoader } from "@karrio/ui/core/components/loader";
import { ModalProvider } from "@karrio/ui/core/modals/modal";
import { bundleContexts } from "@karrio/hooks/utils";
import { Spinner } from "@karrio/ui/core/components";
import { useOrderForm } from "@karrio/hooks/order";
import React, { useEffect, useState } from "react";
import { AddressType } from "@karrio/types";

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
          <header className="px-0 pb-2 pt-4 is-flex is-justify-content-space-between">
            <span className="title is-4 my-2">{`${id === "new" ? "Create" : "Edit"} order`}</span>
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
            <div className="columns pb-6 m-0">
              <div className="column px-0" style={{ minHeight: "850px" }}>
                {/* Line Items */}
                <div className="card px-0 py-3">
                  <header className="px-3 is-flex is-justify-content-space-between">
                    <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">
                      LINE ITEMS
                    </span>
                    <div className="is-vcentered">
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
                            leftIcon={
                              <span className="icon is-small">
                                <i className="fas fa-plus"></i>
                              </span>
                            }
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
                        <div className="is-flex is-justify-content-space-between is-vcentered">
                          <CommodityDescription
                            className="is-flex-grow-1 pr-2"
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
                                  <span className="icon is-small">
                                    <i className="fas fa-pen"></i>
                                  </span>
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
                              <span className="icon is-small">
                                <i className="fas fa-times"></i>
                              </span>
                            </ButtonField>
                          </div>
                        </div>
                      </React.Fragment>
                    ))}

                    {(order.line_items || []).length === 0 && (
                      <div className="m-2 notification is-warning is-light is-default is-size-7">
                        Add one or more product to create a order.
                      </div>
                    )}
                  </div>
                </div>

                {/* Order options section */}
                <div className="card px-0 py-3 mt-5">
                  <header className="px-3 is-flex is-justify-content-space-between">
                    <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">
                      OPTIONS
                    </span>
                  </header>

                  <hr className="my-1" style={{ height: "1px" }} />

                  <div className="p-3 pb-0">
                    {/* order date */}
                    <InputField
                      name="order_date"
                      label="order date"
                      type="date"
                      className="is-small"
                      fieldClass="column mb-0 is-4 p-0 mb-2"
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
                      className="is-small"
                      autoComplete="off"
                      fieldClass="column mb-0 is-4 p-0 mb-2"
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
                    <InputField
                      name="invoice_date"
                      label="invoice date"
                      type="date"
                      className="is-small"
                      fieldClass="column mb-0 is-4 p-0 mb-2"
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
                          className="columns m-1 px-2 py-0"
                          style={{ borderLeft: "solid 2px #ddd" }}
                        >
                          <InputField
                            label="account number"
                            className="is-small"
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

              <div className="p-2"></div>

              <div className="column is-5 px-0 pb-6 is-relative">
                <div
                  style={{ position: "sticky", top: "8.5%", right: 0, left: 0 }}
                >
                  {/* Summary section */}
                  {!isNone(order.line_items) && (
                    <div className="card px-0 mb-5">
                      <header className="px-3 py-2 is-flex is-justify-content-space-between">
                        <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">
                          SUMMARY
                        </span>
                      </header>

                      <div className="p-0 pb-1">
                        <p className="is-title is-size-7 px-3 has-text-weight-semibold">
                          {`ITEMS (${(order.line_items || []).reduce((_, { quantity }) => _ + (isNone(quantity) ? 1 : (quantity as any)), 0)})`}
                        </p>

                        <div
                          className="menu-list px-3 py-1"
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
                        <p className="has-text-weight-semibold is-size-7">
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
                        <p className="has-text-weight-semibold is-size-7">
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
                  <div className="card p-0">
                    <div className="p-3">
                      <header className="is-flex is-justify-content-space-between">
                        <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">
                          Customer
                        </span>
                        <div className="is-vcentered">
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
                        <div className="notification is-warning is-light my-2 py-2 px-4 is-size-7">
                          Please specify the customer address.
                        </div>
                      )}
                    </div>

                    <hr className="my-1" style={{ height: "1px" }} />

                    <div className="p-3">
                      <header className="is-flex is-justify-content-space-between">
                        <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">
                          Billing Address
                        </span>
                        <div className="is-vcentered">
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
                          <div className="notification my-2 py-2 px-4 is-size-7">
                            Same as shipping address.
                          </div>
                        )}
                    </div>
                  </div>

                  {/* Metadata section */}
                  <div className="card px-0 mt-5">
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
                              <header className="is-flex is-justify-content-space-between p-2">
                                <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">
                                  METADATA
                                </span>
                                <div className="is-vcentered">
                                  <ButtonField
                                    type="button"
                                    variant="link"
                                    size="sm"
                                    disabled={isEditing}
                                    onClick={() => editMetadata()}
                                    className="text-blue-600 hover:text-blue-800 p-1 h-auto"
                                  >
                                    <span>Edit metadata</span>
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