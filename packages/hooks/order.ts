import { OrderFilter, get_orders, GET_ORDERS, get_order, GET_ORDER, CreateOrderMutationInput, CreateOrder, CREATE_ORDER, DELETE_ORDER, DeleteOrder, UpdateOrder, UpdateOrderMutationInput, UpdateCommodityInput, CommodityInput, NotificationType, DISCARD_COMMODITY, discard_commodity, UPDATE_ORDER, GET_ORDER_DATA } from "@karrio/types";
import { gqlstr, handleFailure, insertUrlParam, isNoneOrEmpty, onError } from "@karrio/lib";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useNotifier } from "@karrio/ui/components/notifier";
import { useLoader } from "@karrio/ui/components/loader";
import { useRouter } from "next/dist/client/router";
import { OrderType } from "@karrio/types";
import { useAppMode } from "./app-mode";
import { useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };
type FilterType = OrderFilter & { setVariablesToURL?: boolean, isDisabled?: boolean, cacheKey?: string, preloadNextPage?: boolean; };

export function useOrders({ setVariablesToURL = false, isDisabled = false, preloadNextPage = false, cacheKey, ...initialData }: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<OrderFilter>({ ...PAGINATION, ...initialData });
  const fetch = (variables: { filter: OrderFilter }) => karrio.graphql.request<get_orders>(
    gqlstr(GET_ORDERS), { variables }
  );

  // Queries
  const query = useQuery({
    queryKey: [cacheKey || 'orders', filter],
    queryFn: () => fetch({ filter }),
    enabled: !isDisabled,
    keepPreviousData: true,
    staleTime: 5000,
    onError,
  });

  function setFilter(options: OrderFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof OrderFilter]) ? acc : {
        ...acc,
        [key]: (["status", "option_key"].includes(key)
          ? ([].concat(options[key as keyof OrderFilter] as any).reduce(
            (acc, item: string) => (
              typeof item == 'string'
                ? [].concat(acc, item.split(',') as any)
                : [].concat(acc, item)
            ), []
          ))
          : (["offset", "first"].includes(key)
            ? parseInt(options[key as keyof OrderFilter] as any)
            : options[key as keyof OrderFilter]
          )
        )
      };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (preloadNextPage === false) return;
    if (query.data?.orders.page_info.has_next_page) {
      const _filter = { ...filter, offset: filter.offset as number + 20 };
      queryClient.prefetchQuery(
        ['orders', _filter],
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

export function useOrder(id: string, { editable = false } = {}) {
  const karrio = useKarrio();
  const QUERY = gqlstr(editable ? GET_ORDER_DATA : GET_ORDER);

  // Queries
  const query = useQuery({
    queryKey: ['orders', id],
    queryFn: () => karrio.graphql.request<get_order>(QUERY, { variables: { id } }),
    enabled: (!!id && id !== 'new'),
    onError,
  });

  return {
    query,
  };
}

export function useOrderMutation(id?: string) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    queryClient.invalidateQueries(['orders']);
    queryClient.invalidateQueries(['orders', id]);
  };

  // Mutations
  // REST requests
  const cancelOrder = useMutation(
    ({ id }: OrderType) => handleFailure(
      karrio.orders.cancel({ id }).then(({ data }) => data)
    ),
    { onSuccess: invalidateCache, onError }
  );
  const createOrder = useMutation(
    (data: CreateOrderMutationInput) => karrio.graphql.request<CreateOrder>(
      gqlstr(CREATE_ORDER), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const updateOrder = useMutation(
    (data: UpdateOrderMutationInput) => karrio.graphql.request<UpdateOrder>(
      gqlstr(UPDATE_ORDER), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const deleteOrder = useMutation(
    (data: { id: string }) => karrio.graphql.request<DeleteOrder>(gqlstr(DELETE_ORDER), { data }),
    { onSuccess: invalidateCache, onError }
  );
  const deleteLineItem = useMutation(
    (data: { id: string }) => karrio.graphql.request<discard_commodity>(
      gqlstr(DISCARD_COMMODITY), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );

  return {
    cancelOrder,
    createOrder,
    updateOrder,
    deleteOrder,
    deleteLineItem,
  };
}


// -----------------------------------------------------------
// Order Form mutation hooks
// -----------------------------------------------------------
//#region

type OrderDataType = (CreateOrderMutationInput | UpdateOrderMutationInput) & {
  id?: string,
  shipping_to: UpdateOrderMutationInput['shipping_to'] & { id?: string },
  shipping_from?: UpdateOrderMutationInput['shipping_from'] & { id?: string },
  line_items: ((CommodityInput | UpdateCommodityInput) & { id?: string })[],
};
type ChangeType = {
  deleted?: boolean,
  created?: boolean,
  manuallyUpdated?: boolean,
  forcelocalUpdate?: boolean,
};
const DEFAULT_STATE = {
  shipping_to: {},
  line_items: [] as any,
  options: {},
} as OrderDataType;

function reducer(state: Partial<OrderDataType>, { name, value }: { name: string, value: Partial<OrderDataType> }): OrderDataType {
  switch (name) {
    case 'full':
      return { ...(value as OrderDataType) };
    default:
      let newState = { ...state, ...(value as Partial<OrderDataType>) } as OrderDataType;
      Object.entries(value).forEach(([key, val]) => {
        if (val === undefined) delete newState[key as keyof OrderDataType];
      });
      return { ...state, ...(newState as OrderDataType) };
  }
}

export function useOrderForm({ id = 'new' }: { id?: string }) {
  const loader = useLoader();
  const router = useRouter();
  const notifier = useNotifier();
  const { basePath } = useAppMode();
  const mutation = useOrderMutation(id);
  const [isNew, setIsNew] = React.useState<boolean>();
  const { query: { data: { order: current } = {}, ...orderQuery } } = useOrder(id, { editable: true });
  const [order, dispatch] = React.useReducer(reducer, DEFAULT_STATE, () => DEFAULT_STATE);

  // state checks
  const isLocalDraft = (id?: string) => isNoneOrEmpty(id) || id === 'new';

  // Queries
  const query = useQuery({
    queryKey: ['orders', id],
    queryFn: () => (id === 'new' ? { order } : { order: current }),
    enabled: (
      !!id && (id === 'new' || orderQuery.isFetched)
    ),
    onError,
  });

  // Mutations
  const updateOrder = async (changes: Partial<OrderDataType>, change: ChangeType = { manuallyUpdated: false, forcelocalUpdate: false }) => {
    const updateLocalState = (
      change.forcelocalUpdate ||
      // always update local state if it is a new draft
      isLocalDraft(order.id) ||
      // only update local state first if it is not a draft and no new object is created or deleted.
      (!isLocalDraft(order.id) && !change.created && !change.deleted && !change.manuallyUpdated)
    );
    const uptateServerState = (
      !isLocalDraft(order.id) && !!change.deleted
    );

    if (updateLocalState) {
      dispatch({ name: "partial", value: { ...order, ...changes } });
    }

    // if it is not a draft and hasn't been manually updated already
    if (uptateServerState) {
      try {
        let { ...data } = changes;
        if (Object.keys(data).length === 0) return; // abort if no data changes
        await mutation.updateOrder.mutateAsync({ id: order.id, ...data } as any)
          .then(({ update_order: { order } }) => {
            if (change.deleted && order) {
              dispatch({ name: "partial", value: changes });
            }
          });
      } catch (error: any) {
        notifier.notify({ type: NotificationType.error, message: error });
      }
    }
  };
  const addItem = async (data: OrderDataType['line_items'][0]) => {
    const item = order.line_items.find(item => (
      item.parent_id === data.parent_id ||
      item.sku === data.sku ||
      item.hs_code === data.hs_code ||
      item.id === data.id
    ));
    const update = {
      line_items: (!item ? [...order.line_items, data] : order.line_items.map(item => (
        (
          item.parent_id === data.parent_id ||
          item.sku === data.sku ||
          item.hs_code === data.hs_code ||
          item.id === data.id
        ) ? { ...item, ...data } : item
      ))),
    };
    updateOrder(update as any);
  };
  const updateItem = (index: number, item_id?: string | null) => async (data: OrderDataType['line_items'][0], change?: ChangeType) => {
    const update = {
      line_items: order.line_items.map(({ ...item }, idx) => (
        (item.id === item_id || idx === index) ? data : item
      ))
    };
    updateOrder(update as any, change);
  };
  const deleteItem = (index: number, item_id?: string | null) => async () => {
    const update = {
      line_items: order.line_items.filter((_, idx) => idx !== index),
    };

    if (!isLocalDraft(order.id) && !!item_id) {
      await mutation.deleteLineItem.mutateAsync({ id: item_id as string });
    }

    updateOrder(update as any, { deleted: !!item_id });
  };

  // Requests
  const save = async () => {
    const { id, ...data } = order as any;

    try {
      loader.setLoading(true);
      if (isLocalDraft(id)) {
        const { create_order: { order } } = await mutation.createOrder.mutateAsync(data as CreateOrderMutationInput)
        notifier.notify({ type: NotificationType.success, message: 'Order saved!' });
        router.push(`${basePath}/draft_orders/${order?.id}`.replace('//', '/'));
      } else {
        await mutation.updateOrder.mutateAsync({ id, ...data } as UpdateOrderMutationInput)
        notifier.notify({ type: NotificationType.success, message: 'Order saved!' });
      }
    } catch (error: any) {
      notifier.notify({ type: NotificationType.error, message: error });
      loader.setLoading(false);
    }
  }

  React.useEffect(() => { setIsNew(id === 'new'); }, [id]);
  React.useEffect(() => {
    if (orderQuery.isFetched && id !== 'new') {
      dispatch({ name: 'full', value: current as OrderDataType });
    }
  }, [current, orderQuery.isFetched, id]);

  return {
    isNew,
    order,
    query,
    current,
    DEFAULT_STATE,
    save,
    addItem,
    updateItem,
    deleteItem,
    updateOrder,
  }
}

//#endregion
