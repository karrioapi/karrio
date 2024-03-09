import { CommodityEditModalProvider, CommodityStateContext } from '@karrio/ui/modals/commodity-edit-modal';
import { MetadataEditor, MetadataEditorContext } from '@karrio/ui/forms/metadata-editor';
import { GoogleGeocodingScript } from '@karrio/ui/components/google-geocoding-script';
import { CommodityDescription } from '@karrio/ui/components/commodity-description';
import { AddressDescription } from '@karrio/ui/components/address-description';
import { formatRef, isEqual, isNone, isNoneOrEmpty, useLocation } from '@karrio/lib';
import { MetadataObjectTypeEnum, PaidByEnum } from '@karrio/types';
import { AddressModalEditor } from '@karrio/ui/modals/form-modals';
import { AuthenticatedPage } from '@/layouts/authenticated-page';
import { InputField } from '@karrio/ui/components/input-field';
import { DashboardLayout } from '@/layouts/dashboard-layout';
import { useLoader } from '@karrio/ui/components/loader';
import { ModalProvider } from '@karrio/ui/modals/modal';
import { bundleContexts } from '@karrio/hooks/utils';
import { useOrderForm } from '@karrio/hooks/order';
import React, { useEffect, useState } from 'react';
import { AddressType } from '@karrio/types';
import Head from 'next/head';
import { Spinner } from '@karrio/ui/components';

export { getServerSideProps } from "@/context/main";

const ContextProviders = bundleContexts([
  CommodityEditModalProvider,
  ModalProvider,
]);

export default function Page(pageProps: any) {
  const Component: React.FC = () => {
    const loader = useLoader();
    const router = useLocation();
    const { id } = router.query;
    const [ready, setReady] = useState<boolean>(false);
    const [loading, setLoading] = useState<boolean>(false);
    const [key, setKey] = useState<string>(`order-${Date.now()}`);
    const { order, current, isNew, DEFAULT_STATE, query, ...mutation } = useOrderForm({ id });

    const handleChange = async (changes?: Partial<typeof order>) => {
      if (changes === undefined) { return; }
      await mutation.updateOrder({ id, ...changes });
      setKey(`${id}-${Date.now()}`);
    };
    useEffect(() => {
      if (
        !ready && query.isFetched &&
        id === 'new' &&
        !isNone(order.line_items)
      ) {
        setTimeout(() => setReady(true), 1000);
      }
      if (
        !ready && query.isFetched &&
        !isNoneOrEmpty(id) &&
        id !== 'new' &&
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
            <span className="title is-4 my-2">{`${id === 'new' ? 'Create' : 'Edit'} order`}</span>
            <div>
              <button type="button" className="button is-small is-success" onClick={() => mutation.save()}
                disabled={loader.loading || isEqual(order, current || DEFAULT_STATE) || !order?.shipping_to?.country_code}>
                Save
              </button>
            </div>
          </header>

          {!ready && <Spinner />}

          {ready && <div className="columns pb-6 m-0">
            <div className="column px-0" style={{ minHeight: '850px' }}>

              {/* Line Items */}
              <div className="card px-0 py-3">

                <header className="px-3 is-flex is-justify-content-space-between">
                  <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">LINE ITEMS</span>
                  <div className="is-vcentered">
                    <CommodityStateContext.Consumer>{({ editCommodity }) => (
                      <button type="button" className="button is-small is-info is-inverted p-2"
                        disabled={query.isFetching}
                        onClick={() => editCommodity({ onSubmit: _ => mutation.addItem(_) })}>
                        <span className="icon is-small">
                          <i className="fas fa-plus"></i>
                        </span>
                        <span>add item</span>
                      </button>
                    )}</CommodityStateContext.Consumer>
                  </div>
                </header>

                <hr className='my-1' style={{ height: '1px' }} />

                <div className="p-3">
                  {(order.line_items || []).map((item, index) => <React.Fragment key={index + "customs-info"}>
                    {index > 0 && <hr className='my-1' style={{ height: '1px' }} />}
                    <div className="is-flex is-justify-content-space-between is-vcentered">
                      <CommodityDescription className="is-flex-grow-1 pr-2" commodity={item as any} />
                      <div>
                        <CommodityStateContext.Consumer>{({ editCommodity }) => (
                          <button type="button" className="button is-small is-white"
                            onClick={() => editCommodity({
                              commodity: item as any,
                              onSubmit: _ => mutation.updateItem(index, item.id)(_)
                            })}>
                            <span className="icon is-small"><i className="fas fa-pen"></i></span>
                          </button>
                        )}</CommodityStateContext.Consumer>
                        <button type="button" className="button is-small is-white"
                          disabled={query.isFetching || order.line_items.length === 1}
                          onClick={() => mutation.deleteItem(index, item?.id)()}>
                          <span className="icon is-small"><i className="fas fa-times"></i></span>
                        </button>
                      </div>
                    </div>
                  </React.Fragment>)}

                  {(order.line_items || []).length === 0 && <div className="m-2 notification is-warning is-light is-default is-size-7">
                    Add one or more product to create a order.
                  </div>}
                </div>

              </div>


              {/* Order options section */}
              <div className="card px-0 py-3 mt-5">

                <header className="px-3 is-flex is-justify-content-space-between">
                  <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">OPTIONS</span>
                </header>

                <hr className='my-1' style={{ height: '1px' }} />

                <div className="p-3 pb-0">

                  {/* order date */}
                  <InputField name="order_date"
                    label="order date"
                    type="date"
                    className="is-small"
                    fieldClass="column mb-0 is-4 p-0 mb-2"
                    defaultValue={order.order_date || ''}
                    onChange={e => handleChange({ order_date: e.target.value })}
                  />


                  {/* invoice */}
                  <InputField label="invoice number"
                    name="invoice_number"
                    placeholder="invoice number"
                    className="is-small"
                    autoComplete="off"
                    fieldClass="column mb-0 is-4 p-0 mb-2"
                    defaultValue={order.options?.invoice_number || ''}
                    onChange={e => handleChange({ options: { ...order.options, invoice_number: e.target.value } })}
                  />


                  {/* invoice date */}
                  <InputField name="invoice_date"
                    label="invoice date"
                    type="date"
                    className="is-small"
                    fieldClass="column mb-0 is-4 p-0 mb-2"
                    defaultValue={order.options?.invoice_date || ''}
                    onChange={e => handleChange({ options: { ...order.options, invoice_date: e.target.value } })}
                  />

                </div>

                <hr className='my-1' style={{ height: '1px' }} />

                <div className="p-3">
                  <label className="label is-capitalized" style={{ fontSize: '0.8em' }}>Shipment Paid By</label>

                  <div className="control">

                    <label className="radio">
                      <input
                        className="mr-1"
                        type="radio"
                        name="paid_by"
                        defaultChecked={order.options?.paid_by === PaidByEnum.sender}
                        onChange={() => handleChange({ options: { ...order.options, paid_by: PaidByEnum.sender } })}
                      />
                      <span className="is-size-7 has-text-weight-bold">{formatRef(PaidByEnum.sender.toString())}</span>
                    </label>
                    <label className="radio">
                      <input
                        className="mr-1"
                        type="radio"
                        name="paid_by"
                        defaultChecked={order.options?.paid_by === PaidByEnum.recipient}
                        onChange={() => handleChange({ options: { ...order.options, paid_by: PaidByEnum.recipient } })}
                      />
                      <span className="is-size-7 has-text-weight-bold">{formatRef(PaidByEnum.recipient.toString())}</span>
                    </label>
                    <label className="radio">
                      <input
                        className="mr-1"
                        type="radio"
                        name="paid_by"
                        defaultChecked={order.options?.paid_by === PaidByEnum.third_party}
                        onChange={() => handleChange({ options: { ...order.options, paid_by: PaidByEnum.third_party } })}
                      />
                      <span className="is-size-7 has-text-weight-bold">{formatRef(PaidByEnum.third_party.toString())}</span>
                    </label>

                  </div>

                  {(order.options?.paid_by && order.options?.paid_by !== PaidByEnum.sender) &&
                    <div className="columns m-1 px-2 py-0" style={{ borderLeft: "solid 2px #ddd" }}>
                      <InputField
                        label="account number"
                        className="is-small"
                        defaultValue={order?.options?.account_number as string}
                        onChange={e => handleChange({ options: { ...order.options, account_number: e.target.value } })}
                      />
                    </div>}
                </div>

              </div>

            </div>

            <div className="p-2"></div>

            <div className="column is-5 px-0 pb-6 is-relative">
              <div style={{ position: 'sticky', top: '8.5%', right: 0, left: 0 }}>

                {/* Summary section */}
                {!isNone(order.line_items) && <div className="card px-0 mb-5">

                  <header className="px-3 py-2 is-flex is-justify-content-space-between">
                    <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">SUMMARY</span>
                  </header>

                  <div className="p-0 pb-1">
                    <p className="is-title is-size-7 px-3 has-text-weight-semibold">
                      {`ITEMS (${order.line_items.reduce((_, { quantity }) => _ + (isNone(quantity) ? 1 : quantity as any), 0)})`}
                    </p>

                    <div className="menu-list px-3 py-1" style={{ maxHeight: '14em', overflow: 'auto' }}>

                      {order.line_items.map((item, index) => <React.Fragment key={index + "parcel-info"}>
                        <hr className="my-1" style={{ height: '1px' }} />
                        <CommodityDescription commodity={item as any} />
                      </React.Fragment>)}

                    </div>
                  </div>

                  <footer className="px-3 py-1">
                    <p className="has-text-weight-semibold is-size-7">
                      TOTAL: {<span>{order.line_items.reduce((_, { quantity, value_amount }) => _ + ((isNone(quantity) ? 1 : quantity as any) * (isNone(value_amount) ? 1.0 : value_amount as any)), 0.0)} {order.line_items[0]?.value_currency}</span>}
                    </p>
                    <p className="has-text-weight-semibold is-size-7">
                      TOTAL WEIGHT: {<span>{order.line_items.reduce((_, { quantity, weight }) => _ + ((isNone(quantity) ? 1 : quantity as any) * (isNone(weight) ? 1.0 : weight as any)), 0.0)} {order.line_items[0]?.weight_unit}</span>}
                    </p>
                  </footer>

                </div>}

                {/* Address section */}
                <div className="card p-0">
                  <div className="p-3">

                    <header className="is-flex is-justify-content-space-between">
                      <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">Customer</span>
                      <div className="is-vcentered">
                        <AddressModalEditor
                          shipment={order as any}
                          address={order.shipping_to as AddressType}
                          onSubmit={(address) => handleChange({ shipping_to: address })}
                          trigger={
                            <button className="button is-small is-info is-text is-inverted p-1" disabled={loading}>
                              Edit address
                            </button>
                          }
                        />
                      </div>
                    </header>

                    {Object.values(order.shipping_to || {}).length > 0 &&
                      <AddressDescription address={order.shipping_to as AddressType} />}

                    {Object.values(order.shipping_to || {}).length === 0 &&
                      <div className="notification is-warning is-light my-2 py-2 px-4 is-size-7">
                        Please specify the customer address.
                      </div>}

                  </div>

                  <hr className='my-1' style={{ height: '1px' }} />

                  <div className="p-3">

                    <header className="is-flex is-justify-content-space-between">
                      <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">Billing Address</span>
                      <div className="is-vcentered">
                        <AddressModalEditor
                          shipment={order as any}
                          address={order.billing_address as AddressType}
                          onSubmit={(address) => handleChange({ billing_address: address })}
                          trigger={
                            <button className="button is-small is-info is-text is-inverted p-1" disabled={loading}>
                              Edit billing address
                            </button>
                          }
                        />
                      </div>
                    </header>


                    {Object.values(order.billing_address || {}).length > 0 &&
                      <AddressDescription address={order.billing_address as AddressType} />}

                    {Object.values(order.billing_address || {}).length === 0 &&
                      <div className="notification my-2 py-2 px-4 is-size-7">
                        Same as shipping address.
                      </div>}

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
                      <MetadataEditorContext.Consumer>{({ isEditing, editMetadata }) => (<>

                        <header className="is-flex is-justify-content-space-between p-2">
                          <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">METADATA</span>
                          <div className="is-vcentered">
                            <button
                              type="button"
                              className="button is-small is-info is-text is-inverted p-1"
                              disabled={isEditing}
                              onClick={() => editMetadata()}>
                              <span>Edit metadata</span>
                            </button>
                          </div>
                        </header>

                      </>)}</MetadataEditorContext.Consumer>
                    </MetadataEditor>
                  </div>

                </div>

              </div>
            </div>
          </div>}

        </CommodityEditModalProvider>
      </>
    )
  };

  return AuthenticatedPage((
    <DashboardLayout showModeIndicator={true}>
      <GoogleGeocodingScript />
      <Head><title>{`Draft order - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>

      <ContextProviders>
        <Component />
      </ContextProviders>
    </DashboardLayout>
  ), pageProps);
}
