import { AddressType, CommodityType, CURRENCY_OPTIONS, CustomsType, NotificationType, OrderType, ShipmentType } from '@/lib/types';
import { formatRef, formatWeight, getShipmentCommodities, isNone, isNoneOrEmpty, toSingleItem, useLocation } from '@/lib/helper';
import { AddressModalEditor, CustomsModalEditor, ParcelModalEditor } from '@/components/form-parts/form-modals';
import CommodityEditModalProvider, { CommodityStateContext } from '@/components/commodity-edit-modal';
import CustomsInfoDescription from '@/components/descriptions/customs-info-description';
import MetadataEditor, { MetadataEditorContext } from '@/components/metadata-editor';
import { DEFAULT_CUSTOMS_CONTENT } from '@/components/form-parts/customs-info-form';
import CommodityDescription from '@/components/descriptions/commodity-description';
import { LabelTypeEnum, MetadataObjectTypeEnum, PaidByEnum } from 'karrio/graphql';
import MessagesDescription from '@/components/descriptions/messages-description';
import AddressDescription from '@/components/descriptions/address-description';
import ParcelDescription from '@/components/descriptions/parcel-description';
import { DEFAULT_PARCEL_CONTENT } from '@/components/form-parts/parcel-form';
import CommoditySummary from '@/components/descriptions/commodity-summary';
import GoogleGeocodingScript from '@/components/google-geocoding-script';
import RateDescription from '@/components/descriptions/rate-description';
import { useDefaultTemplates } from '@/context/default-template';
import CheckBoxField from '@/components/generic/checkbox-field';
import LineItemSelector from '@/components/line-item-selector';
import { useConnections } from '@/context/carrier-connections';
import AuthenticatedPage from '@/layouts/authenticated-page';
import ButtonField from '@/components/generic/button-field';
import SelectField from '@/components/generic/select-field';
import { useLabelDataMutation } from '@/context/label-data';
import InputField from '@/components/generic/input-field';
import DashboardLayout from '@/layouts/dashboard-layout';
import ModalProvider from '@/components/generic/modal';
import CarrierImage from '@/components/carrier-image';
import { useNotifier } from '@/components/notifier';
import React, { useEffect, useState } from 'react';
import { bundleContexts } from '@/context/utils';
import { useLoader } from '@/components/loader';
import { useAppMode } from '@/context/app-mode';
import { Disclosure } from '@headlessui/react';
import { useOrders } from '@/context/order';
import Spinner from '@/components/spinner';
import Head from 'next/head';
import moment from 'moment';

export { getServerSideProps } from "@/lib/data-fetching";

const ContextProviders = bundleContexts([
  CommodityEditModalProvider,
  ModalProvider,
]);

export default function CreateShipmentPage(pageProps: any) {
  const Component: React.FC = () => {
    const loader = useLoader();
    const notifier = useNotifier();
    const { basePath } = useAppMode();
    const { carrierOptions } = useConnections();
    const { query: templates } = useDefaultTemplates();
    const { addUrlParam, ...router } = useLocation();
    const [ready, setReady] = useState<boolean>(false);
    const [loading, setLoading] = useState<boolean>(false);
    const { shipment_id = 'new', order_id = "" } = router.query as { shipment_id: string, order_id: string };
    const { state: { shipment, query }, ...mutation } = useLabelDataMutation(shipment_id);
    const [key, setKey] = useState<string>(`${shipment_id}-${Date.now()}`);
    const [selected_rate, setSelectedRate] = useState<ShipmentType['rates'][0] | undefined>(
      shipment?.selected_rate_id ? { id: shipment?.selected_rate_id } as any : undefined
    );
    const { query: orders } = useOrders({
      first: 20,
      status: ['unfulfilled', 'partial'] as any,
      ...(order_id ? { id: order_id.split(',').map(s => s.trim()) } : {})
    });

    const requireInfoForRating = (shipment: ShipmentType) => {
      return (
        shipment.recipient.address_line1 === undefined ||
        shipment.shipper.address_line1 === undefined ||
        shipment.parcels.length === 0 ||
        loading === true
      );
    };
    const isInternational = (shipment: ShipmentType) => {
      return (
        shipment.recipient.country_code !== undefined &&
        shipment.shipper.country_code !== undefined &&
        shipment.recipient.country_code !== shipment.shipper.country_code
      );
    };
    const getMetadatas = (): any => {
      return (orders.data?.orders.edges || [])
        .reduce((acc, { node: { metadata } }) => ({ ...acc, ...(metadata || {}) }), {});
    };
    const getOptions = (): any => {
      return (orders.data?.orders.edges || [])
        .reduce((acc, { node: { options } }) => ({ ...acc, ...options }), {});
    };
    const getItems = () => {
      return (orders.data?.orders.edges || [])
        .map(({ node: { line_items } }) => line_items).flat();
    };
    const getParent = (id: string | null) => {
      return getItems()
        .find((item) => item.id === id);
    };
    const getOrder = (item_id?: string | null) => {
      return (orders.data?.orders.edges || [])
        .find(({ node: order }) => order.line_items.find((item) => item.id === item_id))
        ?.node;
    };
    const getAvailableQuantity = (shipment: ShipmentType, item: CommodityType, item_index: number) => {
      const parent_quantity = getParent(item.parent_id)?.unfulfilled_quantity || 0;
      const packed_quantity = shipment.parcels
        .map(({ items }) => items || []).flat()
        .filter((_, index) => index !== item_index)
        .reduce((acc, { parent_id, quantity }) => {
          return (parent_id === item.parent_id) ? acc + (quantity as number) : 0;
        }, 0);

      return parent_quantity - packed_quantity;
    };
    const isPackedItem = (cdt: CommodityType, shipment: ShipmentType) => {
      const item = getShipmentCommodities(shipment).find(item => (
        (!!cdt.parent_id && cdt.parent_id === item.parent_id)
        || (!!cdt.hs_code && cdt.hs_code === cdt.hs_code)
        || (!!cdt.sku && cdt.sku === item.sku)
      ));
      return !!item;
    };
    const setInitialData = () => {
      const orderList = orders.data!.orders!.edges;
      const default_parcel = templates.data?.default_templates.default_parcel?.parcel;
      const default_address = templates.data?.default_templates.default_address?.address;

      const order_ids = orderList.map(({ node: { order_id } }) => order_id).join(',');
      const { id: _, ...recipient } = orderList[0].node.shipping_to || {};
      const { id: __, ...shipper } = (orderList[0].node!.shipping_from || default_address || {} as any);
      const billing_address = orderList[0].node.billing_address ? orderList[0].node.billing_address : undefined;

      // Collect orders merged options
      const order_options = getOptions();
      const order_metadatas = getMetadatas();

      // Collect unfulfilled line items
      const line_items = (
        getItems()
          .map(({ id: parent_id, unfulfilled_quantity: quantity, ...item }) => ({ ...item, quantity, parent_id }))
          .filter(({ quantity }) => quantity || 0 > 0)
      );
      const parcel = default_parcel || DEFAULT_PARCEL_CONTENT;
      const parcel_items = order_options.single_item_per_parcel ? toSingleItem(line_items as any) : [line_items];
      const parcels: any[] = (parcel_items as typeof line_items[]).map(items => {
        const weight = items.reduce((acc, { weight, quantity }) => (weight || 0) * (quantity || 1) + acc, 0.0);
        const weight_unit = items[0].weight_unit || parcel.weight_unit;
        return { ...parcel, items, weight, weight_unit };
      });
      const declared_value = line_items.reduce(
        (acc, { value_amount, quantity }) => (acc + (value_amount || 0) * (quantity || 1)), 0
      );
      const options = {
        ...shipment.options,
        ...(order_options.currency ? { currency: order_options.currency } : {}),
        ...(order_options.service ? { service: order_options.service } : {}),
        ...(order_options.invoice_template ? { invoice_template: order_options.invoice_template } : {}),
        ...(order_options.paperless_trade ? { paperless_trade: order_options.paperless_trade } : {}),
        declared_value: parseFloat(`${declared_value}`).toFixed(2),
      };
      const metadata = {
        order_ids,
        ...order_metadatas,
      };
      const payment = {
        paid_by: order_options.paid_by as any || PaidByEnum.sender,
        ...(order_options.currency ? { currency: order_options.currency } : {}),
        ...(order_options.payment_account_number ? { account_number: order_options.payment_account_number } : {}),
      } as any;
      const isIntl = shipper && (shipper.country_code !== recipient.country_code);
      const isDocument = parcels.every(p => p.is_document);
      const customs = (isDocument ? null : {
        ...DEFAULT_CUSTOMS_CONTENT,
        commercial_invoice: true,
        invoice: orderList[0].node.order_id,
        invoice_date: order_options.invoice_date || moment().format('YYYY-MM-DD'),
        incoterm: payment?.paid_by == 'sender' ? 'DDP' : 'DDU',
        commodities: getShipmentCommodities({ parcels } as any),
        duty: {
          ...DEFAULT_CUSTOMS_CONTENT.duty,
          currency: order_options?.currency,
          paid_by: order_options.duty_paid_by || payment?.paid_by,
          account_number: order_options.duty_account_number || payment?.account_number,
          declared_value,
        },
        duty_billing_address: billing_address,
      });

      onChange({
        ...(shipper ? { shipper: (shipper as typeof shipment['shipper']) } : {}),
        ...(recipient ? { recipient: (recipient as typeof shipment['recipient']) } : {}),
        options,
        payment,
        parcels,
        metadata,
        label_type: LabelTypeEnum.PDF,
        carrier_ids: order_options.carrier_ids || [],
        billing_address,
        customs: (isIntl ? customs : undefined) as typeof shipment['customs'],
      });

      setReady(true);
    };
    const onChange = async (changes: Partial<ShipmentType>) => {
      if (changes === undefined) { return; }
      await mutation.updateShipment({ id: shipment_id, ...changes });
      setKey(`${shipment_id}-${Date.now()}`);
    };

    useEffect(() => { setLoading(query.isFetching || loader.loading); }, [query.isFetching, loader.loading]);
    useEffect(() => {
      if (isNoneOrEmpty(order_id)) {
        notifier.notify({ type: NotificationType.info, message: 'Select order(s) first! redirecting...' });
        setTimeout(() => router.push(basePath + '/orders'), 2000);
      }
    }, [order_id]);
    useEffect(() => {
      if (
        !ready && query.isFetched &&
        templates.isFetched &&
        orders.isFetched &&
        shipment_id === 'new' &&
        (orders.data?.orders.edges || []).length > 0
      ) {
        setTimeout(() => setInitialData(), 1000);
      }
    }, [query.isFetched, orders.isFetched, templates.isFetched]);

    return (
      <>
        <header className="px-0 py-6 is-flex is-justify-content-space-between">
          <div>
            <span className="title is-4 my-2">Create shipment</span>
            <br />
            {ready && <span className="has-text-weight-semibold is-size-7">
              {(orders.data?.orders.edges || [{}]).length > 1 ? `Multiple Orders` : `Order #${(orders.data?.orders.edges || [{}])[0]?.node?.order_id}`}
            </span>}
          </div>
        </header>

        {(shipment.messages || []).length > 0 && <div className="notification is-danger is-light is-size-7 my-2 p-2">
          <MessagesDescription messages={shipment.messages} />
        </div>}

        {!ready && <Spinner />}

        {(ready && Object.keys(shipment.recipient).length > 0) && <div className="columns pb-6 m-0">
          <div className="column px-0" style={{ minHeight: '850px' }}>

            {/* Address section */}
            <div className="card p-0">

              <div className="p-3">

                <header className="is-flex is-justify-content-space-between">
                  <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">SHIP TO</span>
                  <div className="is-vcentered">
                    <AddressModalEditor
                      shipment={shipment}
                      address={shipment.recipient}
                      onSubmit={(address) => onChange({ recipient: address })}
                      trigger={
                        <button className="button is-small is-info is-text is-inverted p-1" disabled={loading}>
                          Edit ship to address
                        </button>
                      }
                    />
                  </div>
                </header>

                <AddressDescription address={shipment.recipient} />

              </div>

              <hr className='my-1' style={{ height: '1px' }} />

              <div className="p-3">

                <header className="is-flex is-justify-content-space-between">
                  <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">SHIP FROM</span>
                  <div className="is-vcentered">
                    <AddressModalEditor
                      shipment={shipment}
                      address={shipment.shipper}
                      onSubmit={(address) => onChange({ shipper: address })}
                      trigger={
                        <button className="button is-small is-info is-text is-inverted p-1" disabled={loading}>
                          Edit origin address
                        </button>
                      }
                    />
                  </div>
                </header>

                <AddressDescription address={shipment.shipper} />

                {Object.values(shipment.shipper || {}).length === 0 &&
                  <div className="notification is-warning is-light my-2 py-2 px-4">
                    Please specify the origin address.
                  </div>}

              </div>

            </div>

            {/* Parcel & Items section */}
            <div className="card px-0 py-3 mt-5">

              <header className="px-3 is-flex is-justify-content-space-between">
                <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">PACKAGES AND ITEMS</span>
                <div className="is-vcentered">
                  <ParcelModalEditor
                    header='Add package'
                    shipment={shipment}
                    onSubmit={mutation.addParcel}
                    trigger={
                      <button className="button is-small is-info is-text is-inverted p-1" disabled={loading}>
                        Add package
                      </button>
                    }
                  />
                </div>
              </header>

              <hr className='my-1' style={{ height: '1px' }} />

              {shipment.parcels.map((pkg, pkg_index) => (
                <React.Fragment key={pkg.id || `${pkg_index}-${new Date()}`}>
                  {pkg_index > 0 && <hr className='my-1' style={{ height: '3px' }} />}

                  <div className="p-3" key={pkg_index}>
                    {/* Parcel header */}
                    <div className="is-flex is-justify-content-space-between mb-4">
                      <div>
                        <ParcelDescription
                          parcel={pkg}
                          suffix={<span className="tag ml-1 has-text-weight-bold">{pkg_index + 1}</span>}
                        />
                      </div>
                      <div>
                        <ParcelModalEditor header='Edit package'
                          onSubmit={mutation.updateParcel(pkg_index, pkg.id)}
                          parcel={pkg}
                          shipment={shipment}
                          trigger={
                            <button type="button" className="button is-small is-white" disabled={loading}>
                              <span className="icon is-small"><i className="fas fa-pen"></i></span>
                            </button>
                          }
                        />
                        <button type="button" className="button is-small is-white"
                          disabled={loading || shipment.parcels.length === 1}
                          onClick={mutation.removeParcel(pkg_index, pkg.id)}>
                          <span className="icon is-small"><i className="fas fa-times"></i></span>
                        </button>
                      </div>
                    </div>

                    {/* Items section */}
                    <span className="is-size-7 has-text-weight-semibold">ITEMS</span>

                    {(pkg.items || []).map((item, item_index) => (
                      <React.Fragment key={item.id || `${item_index}-${new Date()}`}>
                        <hr className='my-1' style={{ height: '1px' }} />
                        <div key={item_index} className="py-1 is-flex is-justify-content-space-between">
                          <div>
                            <p className="is-size-7 my-1 has-text-weight-semibold">
                              {item_index + 1} {`${item.title || item.description || 'Item'}`}
                            </p>
                            <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">
                              <span className='has-text-info'>{` ORDER: ${getOrder(item.parent_id)?.order_id}`}</span>
                              {isNoneOrEmpty(item.sku) ? ' | SKU: 0000000' : ` | SKU: ${item.sku}`}
                            </p>
                          </div>
                          <div className="is-flex">
                            <div className="is-size-7 has-text-grey has-text-weight-semibold is-flex px-2">
                              <span className="p-2 has-text-right" style={{ minWidth: '90px' }}>{formatWeight(item)}</span>
                              <div className="field has-addons">
                                <p className="control is-expanded">
                                  <input
                                    min={1}
                                    type="number"
                                    defaultValue={item.quantity as number}
                                    max={getAvailableQuantity(shipment, item, item_index)}
                                    onChange={e => {
                                      mutation.updateItem(pkg_index, item_index, pkg.id)({
                                        quantity: parseInt(e.target.value)
                                      } as CommodityType)
                                    }}
                                    className="input is-small"
                                    style={{ width: '60px', textAlign: 'center' }}
                                  />
                                </p>
                                <p className="control">
                                  <a className="button is-static is-small">
                                    of {getParent(item.parent_id)?.unfulfilled_quantity}
                                  </a>
                                </p>
                              </div>
                            </div>
                            <button type="button" className="button is-small is-white"
                              onClick={mutation.removeItem(pkg_index, item_index, item.id)}
                              disabled={pkg.items.length === 1}>
                              <span className="icon is-small"><i className="fas fa-times"></i></span>
                            </button>
                          </div>
                        </div>
                      </React.Fragment>
                    ))}

                    {(pkg.items || []).length === 0 && <div className="notification is-light my-2 py-2 px-4 is-size-7">
                      You can specify content items.
                    </div>}

                    <div className="mt-4">
                      <LineItemSelector
                        title='Edit items'
                        shipment={shipment}
                        onChange={_ => mutation.addItems(pkg_index, pkg.id)(_ as any)}
                      />
                    </div>
                  </div>
                </React.Fragment>
              ))}

              {(shipment.parcels || []).length === 0 && <div className="m-4 notification is-default">
                Add one or more packages to create a shipment.
              </div>}

            </div>


            {/* Shipping options section */}
            <div className="card px-0 py-3 mt-5">

              <header className="px-3 is-flex is-justify-content-space-between">
                <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">OPTIONS</span>
              </header>

              <hr className='my-1' style={{ height: '1px' }} />

              <div className="p-3 pb-0">

                {/* shipment date */}
                <InputField name="shipment_date"
                  label="shipment date"
                  type="date"
                  className="is-small"
                  fieldClass="column mb-0 is-4 p-0 mb-2"
                  defaultValue={shipment.options?.shipment_date}
                  onChange={e => onChange({ options: { ...shipment.options, shipment_date: e.target.value } })}
                />


                {/* currency */}
                <SelectField name="currency"
                  label="shipment currency"
                  className="is-small is-fullwidth"
                  fieldClass="column is-4 mb-0 px-0 py-2"
                  value={shipment.options?.currency}
                  required={!isNone(shipment.options?.insurance) || !isNone(shipment.options?.cash_on_delivery) || !isNone(shipment.options?.declared_value)}
                  onChange={e => onChange({ options: { ...shipment.options, currency: e.target.value } })}
                >
                  <option value="">Select a currency</option>
                  {CURRENCY_OPTIONS.map(unit => <option key={unit} value={unit}>{unit}</option>)}
                </SelectField>


                {/* signature confirmation */}
                <CheckBoxField name="signature_confirmation"
                  fieldClass="column mb-0 is-12 px-0 py-2"
                  defaultChecked={shipment.options?.signature_confirmation}
                  onChange={e => onChange({ options: { ...shipment.options, signature_confirmation: e.target.checked } })}
                >
                  <span>Add signature confirmation</span>
                </CheckBoxField>


                {/* insurance */}
                <CheckBoxField name="addInsurance"
                  fieldClass="column mb-0 is-12 px-0 py-2"
                  defaultChecked={!isNone(shipment.options?.insurance)}
                  onChange={e => onChange({ options: { ...shipment.options, insurance: e.target.checked === true ? "" : null } })}
                >
                  <span>Add insurance coverage</span>
                </CheckBoxField>

                <div className="column is-multiline mb-0 ml-4 my-1 px-2 py-0" style={{
                  borderLeft: "solid 1px #ddd",
                  display: `${isNone(shipment.options?.insurance) ? 'none' : 'block'}`
                }}>

                  <InputField name="insurance"
                    label="Coverage value"
                    type="number"
                    min={0}
                    step="any"
                    className="is-small"
                    fieldClass="column mb-0 is-4 px-1 py-0"
                    controlClass="has-icons-left has-icons-right"
                    defaultValue={shipment.options?.insurance}
                    required={!isNone(shipment.options?.insurance)}
                    onChange={e => onChange({ options: { ...shipment.options, insurance: parseFloat(e.target.value) } })}
                  >
                    <span className="icon is-small is-left">
                      <i className="fas fa-dollar-sign"></i>
                    </span>
                    <span className="icon is-small is-right">{shipment.options?.currency}</span>
                  </InputField>

                </div>


                {/* Cash on delivery */}
                <CheckBoxField name="addCOD"
                  fieldClass="column mb-0 is-12 px-0 py-2"
                  defaultChecked={!isNone(shipment.options?.cash_on_delivery)}
                  onChange={e => onChange({ options: { ...shipment.options, cash_on_delivery: e.target.checked === true ? "" : null } })}
                >
                  <span>Collect on delivery</span>
                </CheckBoxField>

                <div className="column is-multiline mb-0 ml-4 my-1 px-2 py-0" style={{
                  borderLeft: "solid 1px #ddd",
                  display: `${isNone(shipment.options?.cash_on_delivery) ? 'none' : 'block'}`
                }}>

                  <InputField name="cash_on_delivery"
                    label="Amount to collect"
                    type="number" min={0} step="any"
                    className="is-small"
                    controlClass="has-icons-left has-icons-right"
                    fieldClass="column mb-0 is-4 px-1 py-2"
                    value={shipment.options?.cash_on_delivery}
                    required={!isNone(shipment.options?.cash_on_delivery)}
                    onChange={e => onChange({ options: { ...shipment.options, cash_on_delivery: parseFloat(e.target.value) } })}
                  >
                    <span className="icon is-small is-left">
                      <i className="fas fa-dollar-sign"></i>
                    </span>
                    <span className="icon is-small is-right">{shipment.options?.currency}</span>
                  </InputField>

                </div>


                {/* Declared value */}
                <CheckBoxField name="addDeclaredValue"
                  fieldClass="column mb-0 is-12 px-0 py-2"
                  defaultChecked={!isNone(shipment.options?.declared_value)}
                  onChange={e => onChange({ options: { ...shipment.options, declared_value: e.target.checked === true ? "" : null } })}
                >
                  <span>Add package value</span>
                </CheckBoxField>

                <div className="column is-multiline mb-0 ml-4 my-1 px-2 py-0" style={{
                  borderLeft: "solid 1px #ddd",
                  display: `${isNone(shipment.options?.declared_value) ? 'none' : 'block'}`
                }}>

                  <InputField name="declared_value"
                    label="Package value"
                    type="number" min={0} step="any"
                    className="is-small"
                    controlClass="has-icons-right"
                    fieldClass="column mb-0 is-4 px-1 py-2"
                    value={shipment.options?.declared_value}
                    required={!isNone(shipment.options?.declared_value)}
                    onChange={e => onChange({ options: { ...shipment.options, declared_value: parseFloat(e.target.value) } })}
                    addonRight={<span className="icon is-small is-right pr-2">{shipment.options?.currency}</span>}
                  />
                </div>


                {/* paperless trade */}
                <CheckBoxField name="paperless_trade"
                  fieldClass="column mb-0 is-12 px-0 py-2"
                  defaultChecked={shipment.options?.paperless_trade}
                  onChange={e => onChange({ options: { ...shipment.options, paperless_trade: e.target.checked } })}
                >
                  <span>Paperless trade</span>
                </CheckBoxField>


                {/* hold at location */}
                <CheckBoxField name="hold_at_location"
                  fieldClass="column mb-0 is-12 px-0 py-2"
                  defaultChecked={shipment.options?.hold_at_location}
                  onChange={e => onChange({ options: { ...shipment.options, hold_at_location: e.target.checked } })}
                >
                  <span>Hold at location</span>
                </CheckBoxField>

              </div>

              {/* CARRIER OPTIONS SECTION */}
              {carrierOptions.length > 0 && <div className='mb-4 px-3'>

                <Disclosure>
                  {({ open }) => (
                    <div className="block">
                      <Disclosure.Button as="div" style={{ boxShadow: 'none' }}
                        className="is-flex is-justify-content-space-between is-clickable py-2">
                        <div className="has-text-grey has-text-weight-semibold is-size-7 pt-1">CARRIER SPECIFIC OPTIONS</div>
                        <span className="icon is-small m-1">
                          {open ? <i className="fas fa-chevron-up"></i> : <i className="fas fa-chevron-down"></i>}
                        </span>
                      </Disclosure.Button>
                      <Disclosure.Panel className="card is-flat columns is-multiline m-0 px-2">

                        {(carrierOptions.includes("dpdhl_packstation")) && <>
                          {/* dpdhl packstation */}
                          <CheckBoxField name="Packstation"
                            fieldClass="column mb-0 is-12 px-1 py-2"
                            defaultChecked={!isNoneOrEmpty(shipment.options?.dpdhl_packstation)}
                            onChange={e => onChange({ options: { ...shipment.options, dpdhl_packstation: e.target.checked === true ? "" : null } })}
                          >
                            <span>Packstation</span>
                          </CheckBoxField>

                          <div className="column is-multiline m-0 p-0" style={{
                            display: `${isNone(shipment.options?.dpdhl_packstation) ? 'none' : 'block'}`
                          }}>

                            <InputField name="dpdhl_packstation"
                              // label="Packstation"
                              className="is-small"
                              fieldClass="column mb-0 is-6 px-1 py-2"
                              value={shipment.options?.dpdhl_packstation}
                              required={!isNone(shipment.options?.dpdhl_packstation)}
                              onChange={e => onChange({ options: { ...shipment.options, dpdhl_packstation: e.target.value } })}
                            />
                          </div>
                        </>}

                      </Disclosure.Panel>
                    </div>
                  )}
                </Disclosure>

              </div>}

              <hr className='my-1' style={{ height: '1px' }} />

              <div className="p-3">

                <InputField label="Reference"
                  name="reference"
                  defaultValue={shipment.reference as string}
                  onChange={e => mutation.updateShipment({ reference: e.target.value })}
                  placeholder="shipment reference"
                  className="is-small"
                  autoComplete="off"
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
                      defaultChecked={shipment.payment?.paid_by === PaidByEnum.sender}
                      onChange={() => mutation.updateShipment({ payment: { paid_by: PaidByEnum.sender } } as any)}
                    />
                    <span className="is-size-7 has-text-weight-bold">{formatRef(PaidByEnum.sender.toString())}</span>
                  </label>
                  <label className="radio">
                    <input
                      className="mr-1"
                      type="radio"
                      name="paid_by"
                      defaultChecked={shipment.payment?.paid_by === PaidByEnum.recipient}
                      onChange={() => mutation.updateShipment({ payment: { ...shipment.payment, paid_by: PaidByEnum.recipient } })}
                    />
                    <span className="is-size-7 has-text-weight-bold">{formatRef(PaidByEnum.recipient.toString())}</span>
                  </label>
                  <label className="radio">
                    <input
                      className="mr-1"
                      type="radio"
                      name="paid_by"
                      defaultChecked={shipment.payment?.paid_by === PaidByEnum.third_party}
                      onChange={() => mutation.updateShipment({ payment: { ...shipment.payment, paid_by: PaidByEnum.third_party } })}
                    />
                    <span className="is-size-7 has-text-weight-bold">{formatRef(PaidByEnum.third_party.toString())}</span>
                  </label>

                </div>

                {(shipment.payment?.paid_by && shipment.payment?.paid_by !== PaidByEnum.sender) &&
                  <div className="columns m-1 px-2 py-0" style={{ borderLeft: "solid 2px #ddd" }}>
                    <InputField
                      label="account number"
                      className="is-small"
                      defaultValue={shipment?.payment?.account_number as string}
                      onChange={e => mutation.updateShipment({ payment: { ...shipment.payment, account_number: e.target.value } })}
                    />
                  </div>}
              </div>

              {/* Billing address section */}
              {(shipment.billing_address || shipment.payment?.paid_by === PaidByEnum.third_party) && <>
                <hr className='my-1' style={{ height: '1px' }} />

                <div className="p-3">
                  <header className="is-flex is-justify-content-space-between">
                    <label className="label is-capitalized" style={{ fontSize: '0.8em' }}>Billing address</label>
                    <div className="is-vcentered">
                      <AddressModalEditor
                        shipment={shipment}
                        address={shipment.billing_address || (orders.data?.orders.edges || [{}])[0].node?.billing_address || {} as AddressType}
                        onSubmit={(address) => onChange({ billing_address: address })}
                        trigger={
                          <button className="button is-small is-info is-text is-inverted p-1" disabled={query.isFetching}>
                            Edit billing address
                          </button>
                        }
                      />
                    </div>
                  </header>

                  {shipment.billing_address &&
                    <AddressDescription address={shipment!.billing_address as any} />}

                  {!shipment.billing_address && <div className="notification is-default p-2 is-size-7">
                    Add shipment billing address. (optional)
                  </div>}

                </div>
              </>}

            </div>

            {/* Customs declaration section */}
            {isInternational(shipment) && <div className="card px-0 py-3 mt-5">

              <header className="px-3 is-flex is-justify-content-space-between">
                <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">CUSTOMS DECLARATION</span>
                <div className="is-vcentered">
                  <CustomsModalEditor
                    header='Edit customs info'
                    shipment={shipment}
                    customs={shipment?.customs as any || {
                      ...DEFAULT_CUSTOMS_CONTENT,
                      commercial_invoice: true,
                      invoice: (orders.data?.orders.edges || [{}])[0]?.node?.order_id,
                      invoice_date: getOptions().invoice_date || moment().format('YYYY-MM-DD'),
                      incoterm: shipment.payment?.paid_by == 'sender' ? 'DDP' : 'DDU',
                      commodities: getShipmentCommodities(shipment),
                      duty: {
                        ...DEFAULT_CUSTOMS_CONTENT.duty,
                        currency: shipment.options?.currency,
                        paid_by: getOptions().duty_paid_by || shipment.payment?.paid_by,
                        account_number: getOptions().duty_account_number || shipment.payment?.account_number,
                        declared_value: shipment.options?.declared_value,
                      },
                      duty_billing_address: shipment.billing_address,
                    }}
                    onSubmit={mutation.updateCustoms(shipment?.customs?.id)}
                    trigger={
                      <button className="button is-small is-info is-text is-inverted p-1" disabled={loading}>
                        Edit customs info
                      </button>
                    }
                  />
                </div>
              </header>

              <hr className='my-1' style={{ height: '1px' }} />

              <div className="p-3">

                {!isNone(shipment.customs) && <>
                  <CustomsInfoDescription customs={shipment.customs as CustomsType} />

                  {/* Commodities section */}
                  <span className="is-size-7 mt-4 has-text-weight-semibold">COMMODITIES</span>

                  {(shipment.customs!.commodities || []).map((commodity, index) => <React.Fragment key={index + "customs-info"}>
                    <hr className="mt-1 mb-2" style={{ height: '1px' }} />
                    <div className="is-flex is-justify-content-space-between is-vcentered">
                      <CommodityDescription className="is-flex-grow-1 pr-2" commodity={commodity} prefix={`${index + 1} - `} />
                      <div>
                        <CommodityStateContext.Consumer>{({ editCommodity }) => (
                          <button type="button" className="button is-small is-white"
                            disabled={isPackedItem(commodity, shipment) || query.isFetching}
                            onClick={() => editCommodity({
                              commodity,
                              onSubmit: _ => mutation.updateCommodity(index, shipment.customs?.id)(_)
                            })}>
                            <span className="icon is-small"><i className="fas fa-pen"></i></span>
                          </button>
                        )}</CommodityStateContext.Consumer>
                        <button type="button" className="button is-small is-white"
                          disabled={query.isFetching || shipment.customs!.commodities.length === 1}
                          onClick={() => mutation.removeCommodity(index, shipment.customs?.id)(commodity.id)}>
                          <span className="icon is-small"><i className="fas fa-times"></i></span>
                        </button>
                      </div>
                    </div>
                  </React.Fragment>)}

                  {(shipment.customs!.commodities || []).length === 0 && <div className="notification is-warning is-light my-2 py-2 px-4 is-size-7">
                    You need provide commodity items for customs purpose. (required)
                  </div>}

                  <div className="is-flex is-justify-content-space-between mt-4">
                    <CommodityStateContext.Consumer>{({ editCommodity }) => (
                      <button type="button" className="button is-small is-info is-inverted p-2"
                        disabled={query.isFetching}
                        onClick={() => editCommodity({
                          onSubmit: _ => mutation.addCommodities([_] as any)
                        })}>
                        <span className="icon is-small">
                          <i className="fas fa-plus"></i>
                        </span>
                        <span>add commodity</span>
                      </button>
                    )}</CommodityStateContext.Consumer>
                  </div>

                  {/* Duty Billing address section */}
                  {(shipment.customs!.duty_billing_address || shipment.customs!.duty?.paid_by === PaidByEnum.third_party) && <>
                    <hr className='my-1' style={{ height: '1px' }} />

                    <div className="py-3">
                      <header className="is-flex is-justify-content-space-between">
                        <label className="label is-capitalized" style={{ fontSize: '0.8em' }}>Billing address</label>
                        <div className="is-vcentered">
                          <AddressModalEditor
                            address={shipment.customs?.duty_billing_address || {} as AddressType}
                            onSubmit={(address) => mutation.updateShipment({
                              customs: {
                                ...shipment!.customs,
                                duty_billing_address: address
                              } as any
                            })}
                            trigger={
                              <button className="button is-small is-info is-text is-inverted p-1" disabled={query.isFetching}>
                                Edit duty billing address
                              </button>
                            }
                          />
                        </div>
                      </header>

                      {shipment!.customs!.duty_billing_address &&
                        <AddressDescription address={shipment!.customs!.duty_billing_address as any} />}

                      {isNone(shipment!.customs!.duty_billing_address) && <div className="notification is-default p-2 is-size-7">
                        Add customs duty billing address. (optional)
                      </div>}

                    </div>
                  </>}
                </>}

                {isNone(shipment.customs) && <div className="notification is-warning is-light my-2 py-2 px-4 is-size-7">
                  Looks like you have an international shipment.
                  You may need to provide a customs declaration unless you are shipping documents only.
                </div>}

              </div>

            </div>}

          </div>

          <div className="p-2"></div>

          <div className="column is-5 px-0 pb-6 is-relative">
            <div style={{ position: 'sticky', top: '8.5%', right: 0, left: 0 }}>

              <CommoditySummary
                shipment={shipment as ShipmentType}
                orders={orders.data?.orders?.edges.map(({ node }) => node) as OrderType[]}
                className="card px-0 mb-5"
              />

              {/* Shipping section */}
              <div className="card px-0">

                <header className="px-3 py-2 is-flex is-justify-content-space-between">
                  <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">SHIPPING SERVICES</span>
                  <div className="is-vcentered">
                    <button className="button is-small is-info is-text is-inverted p-1"
                      onClick={() => mutation.fetchRates()}
                      disabled={requireInfoForRating(shipment)}>
                      Refresh rates
                    </button>
                  </div>
                </header>

                <hr className='my-1' style={{ height: '1px' }} />

                {/* Live rates section */}
                <div className="p-0 py-1">

                  {loading && <Spinner className="my-1 p-2 has-text-centered" />}

                  {(!loading && (shipment.rates || []).length === 0) && <div className="notification p-2 m-2 is-default is-size-7">
                    Provide all shipping details to retrieve shipping rates.
                  </div>}

                  {(!loading && (shipment.rates || []).length > 0) &&
                    <div className="menu-list px-3 rates-list-box" style={{ maxHeight: '16.8em' }}>
                      {(shipment.rates || []).map(rate => (
                        <a key={rate.id} {...(rate.test_mode ? { title: "Test Mode" } : {})}
                          className={`columns card m-0 mb-1 is-vcentered p-1 ${rate.service === shipment.options.preferred_service ? 'has-text-grey-dark has-background-success-light' : 'has-text-grey'} ${rate.id === selected_rate?.id ? 'has-text-grey-dark has-background-grey-lighter' : 'has-text-grey'}`}
                          onClick={() => setSelectedRate(rate)}>

                          <CarrierImage carrier_name={(rate.meta as any)?.carrier || rate.carrier_name} width={30} height={30} />

                          <RateDescription rate={rate} />
                        </a>
                      ))}
                    </div>}

                </div>

                <hr className='my-1' style={{ height: '1px' }} />

                <div className="p-3 has-text-centered">

                  <div className="control">
                    <label className="radio">
                      <input
                        className="mr-1"
                        type="radio"
                        name="label_type"
                        defaultChecked={shipment.label_type === LabelTypeEnum.PDF}
                        onChange={() => onChange({ label_type: LabelTypeEnum.PDF })}
                      />
                      <span className="is-size-7 has-text-weight-bold">{LabelTypeEnum.PDF}</span>
                    </label>
                    <label className="radio">
                      <input
                        className="mr-1"
                        type="radio"
                        name="label_type"
                        defaultChecked={shipment.label_type === LabelTypeEnum.ZPL}
                        onChange={() => onChange({ label_type: LabelTypeEnum.ZPL })}
                      />
                      <span className="is-size-7 has-text-weight-bold">{LabelTypeEnum.ZPL}</span>
                    </label>
                  </div>

                </div>

                <ButtonField
                  onClick={() => mutation.buyLabel(selected_rate as any)}
                  fieldClass="has-text-centered py-1 px-6 m-0"
                  className="is-success is-fullwidth"
                  disabled={(shipment.rates || []).filter(r => r.id === selected_rate?.id).length === 0 || loading}>
                  <span className="px-6">Buy shipping label</span>
                </ButtonField>

                <div className="py-1"></div>

                {!(!!shipment.id && shipment.id !== 'new') &&
                  <ButtonField
                    onClick={() => mutation.saveDraft()}
                    fieldClass="has-text-centered py-1 px-6 m-0"
                    className="is-default is-fullwidth"
                    disabled={query.isFetching}>
                    <span className="px-6">Save draft</span>
                  </ButtonField>}

                <div className="py-2"></div>

              </div>

              {/* Metadata section */}
              <div className="card px-0 mt-5">

                <div className="p-1 pb-4">
                  <MetadataEditor
                    object_type={MetadataObjectTypeEnum.shipment}
                    metadata={shipment.metadata}
                    onChange={(metadata) => onChange({ metadata })}
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

      </>
    )
  };

  return AuthenticatedPage((
    <DashboardLayout showModeIndicator={true}>
      <GoogleGeocodingScript />
      <Head><title>{`Create shipment - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>

      <ContextProviders>

        <Component />

      </ContextProviders>
    </DashboardLayout>
  ), pageProps);
}
