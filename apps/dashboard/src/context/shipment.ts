import { ShipmentFilter, get_shipments, DISCARD_COMMODITY, PartialShipmentMutationInput, PARTIAL_UPDATE_SHIPMENT, DELETE_TEMPLATE, get_shipment, partial_shipment_update, discard_commodity, discard_customs, discard_parcel, GET_SHIPMENTS, GET_SHIPMENT, ChangeShipmentStatusMutationInput, CHANGE_SHIPMENT_STATUS, change_shipment_status, DISCARD_PARCEL } from "@karrio/graphql";
import { gqlstr, handleFailure, insertUrlParam, isNoneOrEmpty, onError } from "@/lib/helper";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ShipmentType } from "@/lib/types";
import { useKarrio } from "@/lib/client";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = ShipmentFilter & { setVariablesToURL?: boolean };

export function useShipments({ setVariablesToURL = false, ...initialData }: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<ShipmentFilter>({ ...PAGINATION, ...initialData });
  const fetch = (variables: { filter: ShipmentFilter }) => karrio.graphql$.request<get_shipments>(
    gqlstr(GET_SHIPMENTS), { variables }
  );

  // Queries
  const query = useQuery(
    ['shipments', filter],
    () => fetch({ filter }),
    { keepPreviousData: true, staleTime: 5000, onError },
  );

  function setFilter(options: ShipmentFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof ShipmentFilter]) ? acc : {
        ...acc,
        [key]: (["carrier_name", "status", "service"].includes(key)
          ? ([].concat(options[key as keyof ShipmentFilter]).reduce(
            (acc, item: string) => (
              typeof item == 'string'
                ? [].concat(acc, item.split(',') as any)
                : [].concat(acc, item)
            ), []
          ))
          : (["offset", "first"].includes(key)
            ? parseInt(options[key as keyof ShipmentFilter])
            : options[key as keyof ShipmentFilter]
          )
        )
      };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (query.data?.shipments.page_info.has_next_page) {
      const _filter = { ...filter, offset: filter.offset as number + 20 };
      queryClient.prefetchQuery(
        ['shipments', _filter],
        () => fetch({ filter: _filter }),
      )
    }
  }, [query.data, filter.offset, queryClient])

  return {
    query,
    filter,
    setFilter,
  };
}

export function useShipment(id: string) {
  const karrio = useKarrio();

  // Queries
  const query = useQuery({
    queryKey: ['shipments', id],
    queryFn: () => karrio.graphql$.request<get_shipment>(gqlstr(GET_SHIPMENT), { variables: { id } }),
    enabled: !!id && id !== 'new',
    onError,
  });

  return {
    query,
  };
}

export function useShipmentMutation(id?: string) {
  const queryClient = useQueryClient();
  const karrio = useKarrio();
  const invalidateCache = () => {
    queryClient.invalidateQueries(['shipments']);
    queryClient.invalidateQueries(['shipments', id]);
  };

  // Mutations
  // REST requests
  const fetchRates = useMutation(
    ({ id, ...data }: ShipmentType) => handleFailure((id !== undefined && id !== 'new')
      ? karrio.rest$.shipments.rates({ id, shipmentRateData: data as any }).then(({ data: { rates, messages } }) => ({ rates, messages }))
      : karrio.rest$.proxy.fetchRates({ rateRequest: (data as any) }).then(({ data: { rates, messages } }) => ({ rates, messages }))
    ),
    { onSuccess: invalidateCache, onError }
  );
  const buyLabel = useMutation(
    ({ id, selected_rate_id, ...shipment }: ShipmentType) => handleFailure((id !== undefined && id !== 'new')
      ? karrio.rest$.shipments.purchase({ id, shipmentPurchaseData: { selected_rate_id } as any }).then(({ data }) => data)
      : karrio.rest$.shipments.create({ shipmentData: (shipment as any) }).then(({ data }) => data)
    ),
    { onSuccess: invalidateCache, onError }
  );
  const voidLabel = useMutation(
    ({ id }: ShipmentType) => handleFailure(
      karrio.rest$.shipments.cancel({ id }).then(({ data }) => data)
    ),
    { onSuccess: invalidateCache, onError }
  );
  const createShipment = useMutation(
    (data: ShipmentType) => handleFailure(
      karrio.rest$.shipments.create({ shipmentData: (data as any) }).then(({ data }) => data)
    ),
    { onSuccess: invalidateCache, onError }
  );

  // GraphQL requests
  const updateShipment = useMutation(
    (data: PartialShipmentMutationInput) => karrio.graphql$.request<partial_shipment_update>(
      gqlstr(PARTIAL_UPDATE_SHIPMENT), { data }
    ),
    { onSuccess: invalidateCache }
  );
  const discardCustoms = useMutation(
    (data: { id: string }) => karrio.graphql$.request<discard_customs>(
      gqlstr(DELETE_TEMPLATE), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const discardCommodity = useMutation(
    (data: { id: string }) => karrio.graphql$.request<discard_commodity>(
      gqlstr(DISCARD_COMMODITY), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const discardParcel = useMutation(
    (data: { id: string }) => karrio.graphql$.request<discard_parcel>(
      gqlstr(DISCARD_PARCEL), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const changeStatus = useMutation(
    (data: ChangeShipmentStatusMutationInput) => karrio.graphql$.request<change_shipment_status>(
      gqlstr(CHANGE_SHIPMENT_STATUS), { data }
    ),
    { onSuccess: invalidateCache }
  );

  return {
    buyLabel,
    voidLabel,
    fetchRates,
    changeStatus,
    createShipment,
    updateShipment,
    discardCommodity,
    discardCustoms,
    discardParcel,
  };
}
