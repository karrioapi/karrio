import { commodityMatch, errorToMessages, getShipmentCommodities, handleFailure, isEqual, isNone, isNoneOrEmpty, jsonify, onError, toNumber, useLocation } from "@karrio/lib";
import { NotificationType, ShipmentType, ParcelType, CustomsType, CommodityType, Collection, DEFAULT_CUSTOMS_CONTENT } from "@karrio/types";
import { useBatchOperationMutation } from "./batch-operations";
import { useNotifier } from "@karrio/ui/components/notifier";
import { BatchShipmentData } from "@karrio/types/rest/api";
import { useLoader } from "@karrio/ui/components/loader";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useShipmentMutation } from "./shipment";
import { useAppMode } from "./app-mode";
import React from "react";

type BatchShipmentFormProps = {
  shipmentList: ShipmentType[];
}
type ChangeType = {
  deleted?: boolean,
  created?: boolean,
  manuallyUpdated?: boolean,
  forcelocalUpdate?: boolean,
};
type BatchShipmentDataType = { shipments: ShipmentType[] };

// -----------------------------------------------------------
// Bulk shipments hook
// -----------------------------------------------------------
//#region

const DEFAULT_STATE = { shipments: [] as ShipmentType[] } as BatchShipmentDataType;

function reducer(state: Partial<BatchShipmentDataType>, { name, value }: { name: string, value: Partial<BatchShipmentDataType> }): BatchShipmentDataType {
  switch (name) {
    case 'full':
      return { ...(value as BatchShipmentDataType) };
    default:
      let newState = { ...state, ...(value as Partial<BatchShipmentDataType>) } as BatchShipmentDataType;
      return { ...state, ...(newState as BatchShipmentDataType) };
  }
}

export function useBatchShipmentForm({ shipmentList }: BatchShipmentFormProps) {
  const loader = useLoader();
  const notifier = useNotifier();
  const queryClient = useQueryClient();
  const mutation = useBatchOperationMutation();
  const shipmentMutation = useShipmentMutation();
  const [updateRate, setUpdateRate] = React.useState<[number, boolean]>([0, false]);
  const [batch, dispatch] = React.useReducer(reducer, DEFAULT_STATE, () => DEFAULT_STATE);

  // state computation
  const isLocalDraft = (id?: string) => isNoneOrEmpty(id) || id === 'new';
  const hasRateRequirements = (shipment: ShipmentType) => {
    return (
      !isNoneOrEmpty(shipment.recipient.address_line1) &&
      !isNoneOrEmpty(shipment.shipper.address_line1) &&
      shipment.parcels.length > 0
    );
  };
  const shouldFetchRates = (shipment_index: number) => (changes: ShipmentType) => {
    return (
      (!isNone(changes.shipper) && batch.shipments[shipment_index].shipper.address_line1 !== changes.shipper.address_line1) ||
      (!isNone(changes.shipper) && batch.shipments[shipment_index].shipper.country_code !== changes.shipper.country_code) ||
      (!isNone(changes.shipper) && batch.shipments[shipment_index].shipper.city !== changes.shipper.city) ||

      (!isNone(changes.recipient) && batch.shipments[shipment_index].recipient.address_line1 !== changes.recipient.address_line1) ||
      (!isNone(changes.recipient) && batch.shipments[shipment_index].recipient.country_code !== changes.recipient.country_code) ||
      (!isNone(changes.recipient) && batch.shipments[shipment_index].recipient.city !== changes.recipient.city)
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
  const syncOptionsChanges = (shipment_index: number) => (changes: Partial<ShipmentType>): Partial<ShipmentType> => {
    let options = changes.options || batch.shipments[shipment_index].options || {};
    const parcels = changes.parcels || batch.shipments[shipment_index].parcels;
    const customs = "customs" in changes ? changes.customs : batch.shipments[shipment_index].customs;
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

    if (declared_value > 0 && declared_value !== batch.shipments[shipment_index].options.declared_value) {
      options = { ...options, declared_value };
    }

    if (!isNone(currency) && currency !== batch.shipments[shipment_index].options.currency) {
      options = { ...options, currency };
    }

    // ignore if options hasn't changed
    if (isEqual(options, batch.shipments[shipment_index].options)) return changes

    return { ...changes, options };
  };
  const syncCustomsChanges = (shipment_index: number) => (changes: Partial<ShipmentType>): Partial<ShipmentType> => {
    const shipper = changes.shipper || batch.shipments[shipment_index].shipper;
    const recipient = changes.recipient || batch.shipments[shipment_index].recipient;
    const isIntl = (
      (!isNone(shipper?.country_code) && !isNone(recipient?.country_code)) &&
      (shipper.country_code !== recipient.country_code)
    );

    const parcels = changes.parcels || batch.shipments[shipment_index].parcels;
    const isDocument = parcels.every(p => p.is_document);
    const requireCustoms = isIntl && !isDocument;
    const hasCustomsChanges = "customs" in changes;
    const hasParcelsChanges = "parcels" in changes;
    const customsExists = !!batch.shipments[shipment_index].customs;

    let skip = !requireCustoms;
    if (!requireCustoms && customsExists) skip = false;
    if (requireCustoms && hasCustomsChanges) skip = true;
    if (requireCustoms && !hasCustomsChanges && hasParcelsChanges) skip = false;

    if (skip) return changes;
    if (isDocument) return { ...changes, customs: null };
    if (!isIntl) return { ...changes, customs: null };

    const customsItems = batch.shipments[shipment_index].customs?.commodities || [];
    const parcelItems = getShipmentCommodities({ parcels } as any, customsItems);
    const commodities = (
      (isNone(changes.parcels) ? customsItems : parcelItems) || parcelItems
    );

    if (commodities.length === 0) return changes;

    const options = changes.options || batch.shipments[shipment_index].options;
    const currency = (batch.shipments[shipment_index].customs?.duty?.currency || options?.currency);
    const paid_by = (batch.shipments[shipment_index].customs?.duty?.paid_by || batch.shipments[shipment_index].payment?.paid_by);
    const incoterm = (batch.shipments[shipment_index].customs?.incoterm || (paid_by == 'sender' ? 'DDP' : 'DDU'));
    const declared_value = (options?.declared_value || batch.shipments[shipment_index].customs?.duty?.declared_value);
    const account_number = (batch.shipments[shipment_index].customs?.duty?.account_number || batch.shipments[shipment_index].payment?.account_number);

    const customs: any = {
      ...(batch.shipments[shipment_index].customs || DEFAULT_CUSTOMS_CONTENT),
      ...(incoterm ? { incoterm } : {}),
      commodities,
      duty: {
        ...(batch.shipments[shipment_index].customs?.duty || DEFAULT_CUSTOMS_CONTENT.duty),
        ...(paid_by ? { paid_by } : {}),
        ...(currency ? { currency } : {}),
        ...(declared_value ? { declared_value } : {}),
        ...(account_number ? { account_number } : {}),
      },
    };


    return { ...changes, customs };
  };
  const syncCustomsDuty = (shipment_index: number) => (changes: Partial<ShipmentType>): Partial<ShipmentType> => {
    const options = changes.options || batch.shipments[shipment_index].options || {};
    const customs = "customs" in changes ? changes.customs : batch.shipments[shipment_index].customs;

    if (!customs) return changes;

    const declared_value = options.declared_value || customs!.duty.declared_value;
    const duty = { ...customs!.duty, declared_value };

    // ignore if duty hasn't changed
    if (isEqual(duty, customs.duty)) return changes;

    return { ...changes, customs: { ...customs, duty } as any };
  };

  // Updates
  const updateBatch = (changes: Partial<BatchShipmentDataType>) => {
    dispatch({ name: 'full', value: changes });
  };
  const updateShipment = (shipment_index: number, shipment_id?: string) => async (changes: Partial<ShipmentType>, change: ChangeType = { manuallyUpdated: false, forcelocalUpdate: false }) => {
    if (shouldFetchRates(shipment_index)(changes as any)) { setUpdateRate([shipment_index, true]); }
    changes = { ...syncOptionsChanges(shipment_index)(changes) };
    changes = { ...syncCustomsChanges(shipment_index)(changes) };
    changes = { ...syncCustomsDuty(shipment_index)(changes) };

    const customsDiscarded = (
      "customs" in changes &&
      changes.customs === null &&
      !isNone(batch.shipments[shipment_index].customs)
    );
    const updateLocalState = (
      change?.forcelocalUpdate ||
      // always update local state if it is a new draft
      isLocalDraft(batch.shipments[shipment_index].id) ||
      // only update local state first if it is not a draft and no new object is created or deleted.
      (!isLocalDraft(batch.shipments[shipment_index].id) && !change?.created && !change?.deleted && !change?.manuallyUpdated)
    );
    const uptateServerState = (
      !isLocalDraft(batch.shipments[shipment_index].id) &&
      (!change?.manuallyUpdated || customsDiscarded)
    );

    if (updateLocalState) {
      const update = {
        shipments: batch.shipments.map((shipment, index) => (
          (shipment.id === shipment_id || index === shipment_index) ? { ...shipment, ...changes } : shipment
        ))
      };
      updateBatch(update as any);
    }

    // if it is not a draft and hasn't been manually updated already
    if (uptateServerState) {
      try {
        const invalidCustoms = (
          "customs" in changes && [
            ...(changes.customs?.commodities || []),
            ...(batch.shipments[shipment_index].customs?.commodities || [])
          ].length === 0
        );

        if (invalidCustoms) {
          const { customs, ...data } = changes;
          changes = { ...data };
        }

        let { status, rates, messages, service, carrier_ids, ...data } = changes;
        if (Object.keys(data).length === 0) return; // abort if no data changes

        await shipmentMutation.updateShipment.mutateAsync({ id: batch.shipments[shipment_index].id, ...data } as any)
          .then(({ partial_shipment_update: { shipment } }) => {
            if ((change.created || change.deleted) && shipment) {
              const { messages, rates, ...value } = shipment;
              const update = {
                shipments: batch.shipments.map((shipment, index) => (
                  (shipment.id === shipment_id || index === shipment_index) ? value : shipment
                ))
              };
              updateBatch(update as any);
            }
          });
      } catch (error: any) {
        const update = {
          shipments: batch.shipments.map((shipment, index) => (
            (shipment.id === shipment_id || index === shipment_index) ? { ...shipment, messages: errorToMessages(error) } : shipment
          ))
        };
        updateBatch(update as any);
      }
    }
  };
  const addParcel = (shipment_index: number) => async (data: ParcelType) => {
    const update = { parcels: [...batch.shipments[shipment_index].parcels, data] };
    updateShipment(shipment_index)(update, { created: true });
    setUpdateRate([shipment_index, true]);
  };
  const updateParcel = (shipment_index: number) => (parcel_index: number, parcel_id?: string) => async (data: ParcelType, change?: ChangeType) => {
    if (parcelHasRateUpdateChanges(batch.shipments[shipment_index].parcels[parcel_index], data)) {
      setUpdateRate([shipment_index, true]);
    }

    const update = {
      parcels: batch.shipments[shipment_index].parcels.map((parcel, index) => (
        (parcel.id === parcel_id || index === parcel_index) ? data : parcel
      ))
    };
    updateShipment(shipment_index)(update as any, change);
  };
  const addItems = (shipment_index: number) => (parcel_index: number, parcel_id?: string) => async (items: CommodityType[]) => {
    const ts = Date.now();
    const parcel = (
      batch.shipments[shipment_index].parcels.find(({ id }) => id === parcel_id) || batch.shipments[shipment_index].parcels[parcel_index]
    );
    const indexes = new Set((batch.shipments[shipment_index].parcels[parcel_index].items || []).map(
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

    updateParcel(shipment_index)(parcel_index, parcel_id)(update, { created: true });
  };
  const updateItem = (shipment_index: number) => (parcel_index: number, item_index: number, parcel_id?: string) =>
    async ({ id, ...data }: CommodityType) => {
      const parcel = (
        batch.shipments[shipment_index].parcels.find(({ id }) => id === parcel_id) || batch.shipments[shipment_index].parcels[parcel_index]
      );
      const update = {
        ...parcel,
        items: parcel.items.map(
          (item, index) => (index !== item_index ? item : { ...item, ...data })
        )
      };

      updateParcel(shipment_index)(parcel_index, parcel_id)(update);
    };
  const removeParcel = (shipment_index: number) => (parcel_index: number, parcel_id?: string) => async () => {
    const update = {
      parcels: batch.shipments[shipment_index].parcels.filter((_, index) => index !== parcel_index)
    };

    if (!isLocalDraft(batch.shipments[shipment_index].id) && !!parcel_id) {
      await shipmentMutation.discardParcel.mutateAsync({ id: parcel_id as string });
    }

    updateShipment(shipment_index)(update, { deleted: true });
    setUpdateRate([shipment_index, true]);
  };
  const removeItem = (shipment_index: number) => (parcel_index: number, item_index: number, item_id?: string) => async () => {
    let change = { deleted: true, forcelocalUpdate: false, manuallyUpdated: false };
    let queue = () => Promise.resolve();
    const parcel = batch.shipments[shipment_index].parcels[parcel_index];
    const update = {
      ...parcel,
      items: parcel.items.filter(({ id }, index) => (
        !!item_id ? id !== item_id : index !== item_index
      ))
    };

    // If shipment is persisted on the server
    if (!isLocalDraft(batch.shipments[shipment_index].id) && !!item_id) {
      const item = parcel.items.find(({ id }) => id === item_id) as CommodityType;
      const commodity = (batch.shipments[shipment_index].customs?.commodities || []).find(
        cdt => !!cdt.id && commodityMatch(item, batch.shipments[shipment_index].customs?.commodities)
      );
      // send a request to remove item/commodity
      await shipmentMutation.discardCommodity.mutateAsync({ id: item!.id });
      if (!!commodity?.id && (batch.shipments[shipment_index].customs?.commodities || []).length > 1) {
        Object.assign(change, { forcelocalUpdate: true, manuallyUpdated: true });
        queue = () => removeCommodity(shipment_index)(-1, batch.shipments[shipment_index].customs?.id)(commodity.id);
      }
    }

    updateParcel(shipment_index)(parcel_index)(update, change);
    queue();
  };
  const updateCustoms = (shipment_index: number) => (customs_id?: string) => async (data: CustomsType | null, change?: ChangeType) => {
    if (!isLocalDraft(batch.shipments[shipment_index].id) && !!customs_id && data === null) {
      await shipmentMutation.discardCustoms.mutateAsync({ id: customs_id as string });
    }

    updateShipment(shipment_index)({ customs: data }, change);
  };
  const addCommodities = (shipment_index: number) => async (items: CommodityType[], customs_id?: string) => {
    const change = { created: true, forcelocalUpdate: !customs_id };
    const customs = batch.shipments[shipment_index].customs as CustomsType;
    const commodities = customs?.commodities || [];
    const update = {
      ...customs,
      commodities: [
        ...commodities,
        ...items.filter((item) => !commodityMatch(item, commodities))
      ]
    };

    updateCustoms(shipment_index)(batch.shipments[shipment_index].customs?.id)(update, change);
  };
  const updateCommodity = (shipment_index: number) => (cdt_index: number, customs_id?: string) => async ({ id, ...data }: CommodityType, change?: ChangeType) => {
    change = change || { forcelocalUpdate: !customs_id };
    const update = {
      ...batch.shipments[shipment_index].customs as CustomsType,
      commodities: (batch.shipments[shipment_index].customs?.commodities || []).map(
        (item, index) => (index !== cdt_index ? item : { ...item, ...data })
      )
    };

    updateCustoms(shipment_index)(batch.shipments[shipment_index].customs?.id)(update, change);
  };
  const removeCommodity = (shipment_index: number) => (cdt_index: number, customs_id?: string) => async (cdt_id?: string) => {
    const change = { deleted: true, forcelocalUpdate: !customs_id };
    const update = ({
      ...batch.shipments[shipment_index].customs as CustomsType,
      commodities: (batch.shipments[shipment_index].customs?.commodities || [])
        .filter(({ id }, index) => !!id ? id !== cdt_id : index !== cdt_index)
    });

    if (!isLocalDraft(batch.shipments[shipment_index].id) && !!cdt_id) {
      await shipmentMutation.discardCommodity.mutateAsync({ id: cdt_id as string });
    }

    updateCustoms(shipment_index)(batch.shipments[shipment_index].customs?.id)(update, change);
  };

  // Requests
  const fetchRates = useMutation(async (shipment_index: number) => {
    const data = JSON.parse(jsonify(batch.shipments[shipment_index])) as ShipmentType;
    try {
      const { rates, messages } = await shipmentMutation.fetchRates.mutateAsync(data);
      await updateShipment(shipment_index)({ rates, messages } as Partial<ShipmentType>);
    } catch (error: any) {
      await updateShipment(shipment_index)({ rates: [], messages: errorToMessages(error) } as Partial<ShipmentType>);
    }
  });
  const buyLabels = useMutation(async () => {
    if (mutation.createShipments.isLoading) return;
    const data = {
      shipments: batch.shipments.map(shipment => ({
        ...JSON.parse(jsonify(shipment)),
        service: shipment.options.preferred_service || shipment.rates?.[0]?.service,
      }))
    } as BatchShipmentData;

    try {
      loader.setLoading(true);
      await mutation.createShipments.mutateAsync(data);
      notifier.notify({ type: NotificationType.success, message: `Batch shipments created.` });
    } catch (error: any) {
      notifier.notify({ type: NotificationType.error, message: error });
      loader.setLoading(false);
    }
  });

  // Effects
  React.useEffect(() => {
    if ((batch?.shipments || []).length === 0 && shipmentList?.length > 0) {
      console.log('> initializing batch...');
      dispatch({ name: 'full', value: { shipments: shipmentList } });
    }
  }, [shipmentList]);
  React.useEffect(() => {
    if (batch?.shipments.length > 0 && !!batch?.shipments.find(shipment => isNone(shipment.id))) {
      console.log('> create missing drafts...');
      Promise
        .all(batch.shipments.map(async shipment => (
          (!!shipment.id && (shipment.rates || []).length > 0)
            ? shipment
            : (await shipmentMutation.createShipment.mutateAsync(shipment as any) as ShipmentType)
        )))
        .then(
          shipments => dispatch({ name: 'full', value: { shipments } })
        )
        .finally(() => {
          queryClient.invalidateQueries(['orders']);
          queryClient.invalidateQueries(['shipments']);
        });
    }
  }, [batch]);
  React.useEffect(() => {
    const [index, hasChanges] = updateRate;
    if (hasChanges && hasRateRequirements(batch.shipments[index])) {
      setUpdateRate([index, false]);
      fetchRates.mutateAsync(index);
    }
  }, [batch.shipments]);

  return {
    batch,
    buyLabels,
    fetchRates,
    addItems,
    addParcel,
    addCommodities,
    updateItem,
    updateParcel,
    updateShipment,
    updateCommodity,
    updateCustoms,
    removeCommodity,
    removeParcel,
    removeItem,
  }
}

//#endregion
