import { commodityMatch, errorToMessages, getShipmentCommodities, gqlstr, isEqual, isNone, isNoneOrEmpty, toNumber, useLocation } from "@/lib/helper";
import { AddressType, Collection, CommodityType, CustomsType, NotificationType, ParcelType, ShipmentType } from "@/lib/types";
import { get_shipment_data, GET_SHIPMENT_DATA, LabelTypeEnum, PaidByEnum } from "@karrio/graphql";
import { DEFAULT_CUSTOMS_CONTENT } from "@/components/form-parts/customs-info-form";
import { useShipmentMutation } from "@/context/shipment";
import { useNotifier } from "@/components/notifier";
import { useQuery } from "@tanstack/react-query";
import { useAppMode } from "@/context/app-mode";
import { useLoader } from "@/components/loader";
import { useKarrio } from "@/lib/client";
import moment from "moment";
import React from "react";

const DEFAULT_SHIPMENT_DATA = {
  shipper: {} as AddressType,
  recipient: {} as AddressType,
  parcels: [] as ParcelType[],
  options: { shipment_date: moment().format('YYYY-MM-DD') },
  payment: { paid_by: PaidByEnum.sender },
  label_type: LabelTypeEnum.PDF
} as ShipmentType;

type ChangeType = {
  deleted?: boolean,
  created?: boolean,
  manuallyUpdated?: boolean,
  forcelocalUpdate?: boolean,
};


function reducer(state: any, { name, value }: { name: string, value: Partial<ShipmentType> | ShipmentType }): ShipmentType {
  switch (name) {
    case "full":
      return { ...(value as ShipmentType) };
    default:
      let newState = { ...state, ...(value as Partial<ShipmentType>) } as ShipmentType;
      Object.entries(value).forEach(([key, val]) => {
        if (val === undefined) delete newState[key as keyof ShipmentType];
      });
      return { ...state, ...(newState as ShipmentType) };
  }
}


export function useLabelData(id: string) {
  const karrio = useKarrio();
  const mutation = useShipmentMutation();
  const [shipment, dispatch] = React.useReducer(reducer, DEFAULT_SHIPMENT_DATA);

  // Queries
  const query = useQuery({
    queryKey: ['label', id],
    queryFn: () => (
      id === 'new'
        ? { shipment }
        : karrio.graphql$.request<get_shipment_data>(gqlstr(GET_SHIPMENT_DATA), { variables: { id } })
    ),
    enabled: !!id,
  });
  const updateLabelData = (data: Partial<ShipmentType> = {}) => {
    dispatch({ name: "partial", value: data });
  };

  React.useEffect(() => {
    if (id !== 'new' && isEqual(shipment, DEFAULT_SHIPMENT_DATA) && !isNone(query.data?.shipment)) {
      dispatch({ name: "full", value: query!.data!.shipment as ShipmentType })
    }
  }, [query.data?.shipment])

  return {
    query,
    mutation,
    updateLabelData,
    shipment: shipment as ShipmentType,
  };
}


export function useLabelDataMutation(id: string) {
  const loader = useLoader();
  const router = useLocation();
  const notifier = useNotifier();
  const { basePath } = useAppMode();
  const { mutation, ...state } = useLabelData(id);
  const [updateRate, setUpdateRate] = React.useState<boolean>(false);

  // state checks
  const isLocalDraft = (id?: string) => isNoneOrEmpty(id) || id === 'new';
  const hasRateRequirements = (shipment: ShipmentType) => {
    return (
      !isNoneOrEmpty(shipment.recipient.address_line1) &&
      !isNoneOrEmpty(shipment.shipper.address_line1) &&
      shipment.parcels.length > 0
    );
  };
  const shouldFetchRates = (changes: ShipmentType) => {
    return (
      (!isNone(changes.shipper) && state.shipment.shipper.address_line1 !== changes.shipper.address_line1) ||
      (!isNone(changes.shipper) && state.shipment.shipper.country_code !== changes.shipper.country_code) ||
      (!isNone(changes.shipper) && state.shipment.shipper.city !== changes.shipper.city) ||

      (!isNone(changes.recipient) && state.shipment.recipient.address_line1 !== changes.recipient.address_line1) ||
      (!isNone(changes.recipient) && state.shipment.recipient.country_code !== changes.recipient.country_code) ||
      (!isNone(changes.recipient) && state.shipment.recipient.city !== changes.recipient.city)
    );
  };
  const parcelHasRateUpdateChanges = (parcel: ParcelType, changes: Partial<ParcelType>) => {
    return (
      (!isNone(changes.packaging_type) && changes.packaging_type !== parcel.packaging_type) ||
      (!isNone(changes.package_preset) && changes.package_preset !== parcel.package_preset) ||
      (!isNone(changes.is_document) && changes.is_document !== parcel.is_document) ||
      (!isNone(changes.weight) && changes.weight !== parcel.weight) ||
      (!isNone(changes.length) && changes.length !== parcel.length) ||
      (!isNone(changes.height) && changes.height !== parcel.height) ||
      (!isNone(changes.width) && changes.width !== parcel.width)
    );
  };
  const syncOptionsChanges = (changes: Partial<ShipmentType>): Partial<ShipmentType> => {
    let options = changes.options || state.shipment.options || {};
    const parcels = changes.parcels || state.shipment.parcels;
    const customs = "customs" in changes ? changes.customs : state.shipment.customs;
    const commodities = getShipmentCommodities({ parcels } as any, customs?.commodities);

    const declared_value = parseFloat(
      commodities.reduce(
        (_, { value_amount, quantity }) => (_ + (toNumber(quantity || 1) * toNumber(value_amount || 0))),
        0
      ).toFixed(2)
    );
    const currency = parcels.reduce((__, p) => {
      const curr = (p.items || [])
        .reduce((_, { value_currency }) => (_ ? _ : value_currency as any), null);
      return (__ ? __ : curr) as any;
    }, null);

    if (declared_value > 0 && declared_value !== state.shipment.options.declared_value) {
      options = { ...options, declared_value };
    }

    if (!isNone(currency) && currency !== state.shipment.options.currency) {
      options = { ...options, currency };
    }

    // ignore if options hasn't changed
    if (isEqual(options, state.shipment.options)) return changes

    return { ...changes, options };
  };
  const syncCustomsChanges = (changes: Partial<ShipmentType>): Partial<ShipmentType> => {
    const shipper = changes.shipper || state.shipment.shipper;
    const recipient = changes.recipient || state.shipment.recipient;
    const isIntl = (
      (!isNone(shipper?.country_code) && !isNone(recipient?.country_code)) &&
      (shipper.country_code !== recipient.country_code)
    );

    const parcels = changes.parcels || state.shipment.parcels;
    const isDocument = parcels.every(p => p.is_document);
    const requireCustoms = isIntl && !isDocument;
    const hasCustomsChanges = "customs" in changes;
    const hasParcelsChanges = "parcels" in changes;
    const customsExists = !!state.shipment.customs;

    let skip = !requireCustoms;
    if (!requireCustoms && customsExists) skip = false;
    if (requireCustoms && hasCustomsChanges) skip = true;
    if (requireCustoms && !hasCustomsChanges && hasParcelsChanges) skip = false;

    if (skip) return changes;
    if (isDocument) return { ...changes, customs: null };
    if (!isIntl) return { ...changes, customs: null };

    const customsItems = state.shipment.customs?.commodities || [];
    const parcelItems = getShipmentCommodities({ parcels } as any, customsItems);
    const commodities = (
      (isNone(changes.parcels) ? customsItems : parcelItems) || parcelItems
    );

    if (commodities.length === 0) return changes;

    const options = changes.options || state.shipment.options;
    const currency = (state.shipment.customs?.duty?.currency || options?.currency);
    const paid_by = (state.shipment.customs?.duty?.paid_by || state.shipment.payment?.paid_by);
    const incoterm = (state.shipment.customs?.incoterm || (paid_by == 'sender' ? 'DDP' : 'DDU'));
    const declared_value = (options?.declared_value || state.shipment.customs?.duty?.declared_value);
    const account_number = (state.shipment.customs?.duty?.account_number || state.shipment.payment?.account_number);

    const customs: any = {
      ...(state.shipment.customs || DEFAULT_CUSTOMS_CONTENT),
      ...(incoterm ? { incoterm } : {}),
      commodities,
      duty: {
        ...(state.shipment.customs?.duty || DEFAULT_CUSTOMS_CONTENT.duty),
        ...(paid_by ? { paid_by } : {}),
        ...(currency ? { currency } : {}),
        ...(declared_value ? { declared_value } : {}),
        ...(account_number ? { account_number } : {}),
      },
    };


    return { ...changes, customs };
  };
  const syncCustomsDuty = (changes: Partial<ShipmentType>): Partial<ShipmentType> => {
    const options = changes.options || state.shipment.options || {};
    const customs = "customs" in changes ? changes.customs : state.shipment.customs;

    if (!customs) return changes;

    const declared_value = options.declared_value || customs!.duty.declared_value;
    const duty = { ...customs!.duty, declared_value };

    // ignore if duty hasn't changed
    if (isEqual(duty, customs.duty)) return changes;

    return { ...changes, customs: { ...customs, duty } as any };
  };

  // updates
  const updateShipment = async (changes: Partial<ShipmentType>, change: ChangeType = { manuallyUpdated: false, forcelocalUpdate: false }) => {
    if (shouldFetchRates(changes as any)) { setUpdateRate(true); }
    changes = { ...syncOptionsChanges(changes) };
    changes = { ...syncCustomsChanges(changes) };
    changes = { ...syncCustomsDuty(changes) };

    const customsDiscarded = (
      "customs" in changes &&
      changes.customs === null &&
      !isNone(state.shipment.customs)
    );
    const updateLocalState = (
      change.forcelocalUpdate ||
      // always update local state if it is a new draft
      isLocalDraft(state.shipment.id) ||
      // only update local state first if it is not a draft and no new object is created or deleted.
      (!isLocalDraft(state.shipment.id) && !change.created && !change.deleted && !change.manuallyUpdated)
    );
    const uptateServerState = (
      !isLocalDraft(state.shipment.id) &&
      (!change.manuallyUpdated || customsDiscarded)
    );

    if (updateLocalState) {
      state.updateLabelData({ ...state.shipment, ...changes });
    }

    // if it is not a draft and hasn't been manually updated already
    if (uptateServerState) {
      try {
        const invalidCustoms = (
          "customs" in changes && [
            ...(changes.customs?.commodities || []),
            ...(state.shipment.customs?.commodities || [])
          ].length === 0
        );
        if (invalidCustoms) {
          const { customs, ...data } = changes;
          changes = { ...data };
        }
        let { status, rates, messages, service, carrier_ids, ...data } = changes;
        if (Object.keys(data).length === 0) return; // abort if no data changes

        await mutation.updateShipment.mutateAsync({ id: state.shipment.id, ...data } as any)
          .then(({ partial_shipment_update: { shipment } }) => {
            if ((change.created || change.deleted) && shipment) {
              const { messages, rates, ...value } = shipment;
              state.updateLabelData(value as any);
            }
          });
      } catch (error: any) {
        updateShipment({ messages: errorToMessages(error) });
      }
    }
  };
  const addParcel = async (data: ParcelType) => {
    const update = { parcels: [...state.shipment.parcels, data] };
    updateShipment(update, { created: true });
  };
  const updateParcel = (parcel_index: number, parcel_id?: string) => async (data: ParcelType, change?: ChangeType) => {
    if (parcelHasRateUpdateChanges(state.shipment.parcels[parcel_index], data)) {
      setUpdateRate(true);
    }

    const update = {
      parcels: state.shipment.parcels.map((parcel, index) => (
        (parcel.id === parcel_id || index === parcel_index) ? data : parcel
      ))
    };
    updateShipment(update as any, change);
  };
  const addItems = (parcel_index: number, parcel_id?: string) => async (items: CommodityType[]) => {
    const ts = Date.now();
    const parcel = (
      state.shipment.parcels.find(({ id }) => id === parcel_id) || state.shipment.parcels[parcel_index]
    );
    const indexes = new Set((state.shipment.parcels[parcel_index].items || []).map(
      (item, index) => item.parent_id || item.sku || item.hs_code || item.id || `${index}`)
    );
    const item_collection: Collection<CommodityType & { quantity: number }> = items.reduce(
      (acc, item, index) => ({ ...acc, [item.parent_id || item.sku || item.hs_code || item.id || `${ts}${index}`]: item }), {}
    )
    const update = {
      ...parcel, items: [
        ...(parcel.items || []).map((item, index) => {
          const _ref = item.parent_id || item.sku || item.hs_code || `${index}`;
          return ((_ref && Object.keys(item_collection).includes(_ref))
            ? { ...item, quantity: toNumber(item.quantity || 0) + item_collection[_ref].quantity }
            : item
          )
        }),
        ...items.filter((item, index) => !indexes.has(item.parent_id || item.sku || item.hs_code || `${ts}${index}`))
      ]
    };

    updateParcel(parcel_index, parcel_id)(update, { created: true });
  };
  const updateItem = (parcel_index: number, item_index: number, parcel_id?: string) =>
    async ({ id, ...data }: CommodityType) => {
      const parcel = (
        state.shipment.parcels.find(({ id }) => id === parcel_id) || state.shipment.parcels[parcel_index]
      );
      const update = {
        ...parcel,
        items: parcel.items.map(
          (item, index) => (index !== item_index ? item : { ...item, ...data })
        )
      };

      updateParcel(parcel_index, parcel_id)(update);
    };
  const removeParcel = (parcel_index: number, parcel_id?: string) => async () => {
    const update = {
      parcels: state.shipment.parcels.filter((_, index) => index !== parcel_index)
    };

    if (!isLocalDraft(state.shipment.id) && !!parcel_id) {
      await mutation.discardParcel.mutateAsync({ id: parcel_id as string });
    }

    updateShipment(update, { deleted: true });
    setUpdateRate(true);
  };
  const removeItem = (parcel_index: number, item_index: number, item_id?: string) => async () => {
    let change = { deleted: true, forcelocalUpdate: false, manuallyUpdated: false };
    let queue = () => Promise.resolve();
    const parcel = state.shipment.parcels[parcel_index];
    const update = {
      ...parcel,
      items: parcel.items.filter(({ id }, index) => (
        !!item_id ? id !== item_id : index !== item_index
      ))
    };

    // If shipment is persisted on the server
    if (!isLocalDraft(state.shipment.id) && !!item_id) {
      const item = parcel.items.find(({ id }) => id === item_id) as CommodityType;
      const commodity = (state.shipment.customs?.commodities || []).find(
        cdt => !!cdt.id && commodityMatch(item, state.shipment.customs?.commodities)
      );
      // send a request to remove item/commodity
      await mutation.discardCommodity.mutateAsync({ id: item!.id });
      if (!!commodity?.id && (state.shipment.customs?.commodities || []).length > 1) {
        Object.assign(change, { forcelocalUpdate: true, manuallyUpdated: true });
        queue = () => removeCommodity(-1, state.shipment.customs?.id)(commodity.id);
      }
    }

    updateParcel(parcel_index)(update, change);
    queue();
  };
  const updateCustoms = (customs_id?: string) => async (data: CustomsType | null, change?: ChangeType) => {
    if (!isLocalDraft(state.shipment.id) && !!customs_id && data === null) {
      await mutation.discardCustoms.mutateAsync({ id: customs_id as string });
    }

    updateShipment({ customs: data }, change);
  };
  const addCommodities = async (items: CommodityType[], customs_id?: string) => {
    const change = { created: true, forcelocalUpdate: !customs_id };
    const customs = state.shipment.customs as CustomsType;
    const commodities = customs?.commodities || [];
    const update = {
      ...customs,
      commodities: [
        ...commodities,
        ...items.filter((item) => !commodityMatch(item, commodities))
      ]
    };

    updateCustoms(state.shipment.customs?.id)(update, change);
  };
  const updateCommodity = (cdt_index: number, customs_id?: string) => async ({ id, ...data }: CommodityType, change?: ChangeType) => {
    change = change || { forcelocalUpdate: !customs_id };
    const update = {
      ...state.shipment.customs as CustomsType,
      commodities: (state.shipment.customs?.commodities || []).map(
        (item, index) => (index !== cdt_index ? item : { ...item, ...data })
      )
    };

    updateCustoms(state.shipment.customs?.id)(update, change);
  };
  const removeCommodity = (cdt_index: number, customs_id?: string) => async (cdt_id?: string) => {
    const change = { deleted: true, forcelocalUpdate: !customs_id };
    const update = ({
      ...state.shipment.customs as CustomsType,
      commodities: (state.shipment.customs?.commodities || [])
        .filter(({ id }, index) => !!id ? id !== cdt_id : index !== cdt_index)
    });

    if (!isLocalDraft(state.shipment.id) && !!cdt_id) {
      await mutation.discardCommodity.mutateAsync({ id: cdt_id as string });
    }

    updateCustoms(state.shipment.customs?.id)(update, change);
  };

  // requests
  const fetchRates = async () => {
    const { messages, rates, ...data } = state.shipment;

    try {
      loader.setLoading(true);
      const { rates, messages } = await mutation.fetchRates.mutateAsync(data as ShipmentType);
      updateShipment({ rates, messages } as Partial<ShipmentType>);
    } catch (error: any) {
      updateShipment({ rates: [], messages: errorToMessages(error) } as Partial<ShipmentType>);
    }
    setTimeout(() => loader.setLoading(false), 100);
  };
  const buyLabel = async (rate: ShipmentType['rates'][0]) => {
    const { messages, rates, ...data } = state.shipment;
    const selection = (
      isLocalDraft(state.shipment.id)
        ? { service: rate.service, carrier_ids: [rate.carrier_id] }
        : { selected_rate_id: rate.id }
    );

    try {
      loader.setLoading(true);
      const { id } = await mutation.buyLabel.mutateAsync({ ...data, ...selection } as any);
      notifier.notify({ type: NotificationType.success, message: 'Label successfully purchased!' });
      router.push(`${basePath}/shipments/${id}`);
    } catch (error: any) {
      loader.setLoading(false);
      updateShipment({ messages: errorToMessages(error) }, { manuallyUpdated: true });
    }
  };
  const saveDraft = async () => {
    const { ...data } = state.shipment;

    try {
      loader.setLoading(true);
      const { id } = (
        isLocalDraft(state.shipment.id)
          ? await mutation.createShipment.mutateAsync(data as ShipmentType)
          : state.shipment
      );
      notifier.notify({ type: NotificationType.success, message: 'Draft successfully saved!' });
      router.push(`${basePath}/create_label?shipment_id=${id}`);
    } catch (error: any) {
      updateShipment({ messages: errorToMessages(error) } as Partial<ShipmentType>);
      loader.setLoading(false);
    }
  };

  React.useEffect(() => {
    if (updateRate && hasRateRequirements(state.shipment)) {
      setUpdateRate(false);
      fetchRates();
    }
  }, [state.shipment]);

  return {
    state,
    addItems,
    addParcel,
    addCommodities,
    buyLabel,
    fetchRates,
    updateItem,
    updateParcel,
    updateShipment,
    updateCommodity,
    updateCustoms,
    removeCommodity,
    removeParcel,
    removeItem,
    saveDraft,
  };
}
