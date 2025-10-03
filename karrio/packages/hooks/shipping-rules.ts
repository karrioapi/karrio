import {
  GET_SHIPPING_RULES,
  GET_SHIPPING_RULE,
  DELETE_SHIPPING_RULE,
  UPDATE_SHIPPING_RULE,
  CREATE_SHIPPING_RULE,
  DeleteMutationInput,
} from "@karrio/types/graphql/ee";
import {
  gqlstr,
  insertUrlParam,
  isNoneOrEmpty,
  onError,
  p,
} from "@karrio/lib";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useForm } from "@tanstack/react-form";
import { useNotifier } from "@karrio/ui/core/components/notifier";
import { useLoader } from "@karrio/ui/core/components/loader";
import { useRouter } from "next/navigation";
import { NotificationType } from "@karrio/types";
import { useAppMode } from "./app-mode";
import { useAuthenticatedQuery, useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };

// Temporary type placeholders until types are generated
type ShippingRuleFilter = {
  offset?: number;
  first?: number;
  keyword?: string;
  is_active?: boolean;
  priority?: number;
};

type GetShippingRules = {
  shipping_rules: {
    page_info: {
      count: number;
      has_next_page: boolean;
      has_previous_page: boolean;
      start_cursor: string;
      end_cursor: string;
    };
    edges: {
      node: ShippingRuleType;
    }[];
  };
};

type GetShippingRule = {
  shipping_rule: ShippingRuleType;
};

type ShippingRuleType = {
  object_type: string;
  id: string;
  name: string;
  slug: string;
  priority: number;
  is_active: boolean;
  description?: string;
  conditions: {
    destination?: {
      country_code?: string;
      postal_code?: string[];
    };
    carrier_id?: string;
    service?: string;
    weight?: {
      min?: number;
      max?: number;
      unit?: string;
    };
    rate_comparison?: {
      compare: string;
      operator: string;
      value: number;
    };
    address_type?: {
      type: string;
    };
    value?: number;
    metadata?: any;
  };
  actions: {
    select_service?: {
      carrier_code?: string;
      carrier_id?: string;
      service_code?: string;
      strategy: string;
    };
    block_service?: boolean;
  };
  metadata?: any;
  created_at: string;
  updated_at: string;
};

type CreateShippingRule = {
  create_shipping_rule: {
    shipping_rule?: { id: string };
    errors: { field: string; messages: string[] }[];
  };
};

type UpdateShippingRule = {
  update_shipping_rule: {
    shipping_rule?: { id: string };
    errors: { field: string; messages: string[] }[];
  };
};

type CreateShippingRuleMutationInput = {
  name: string;
  description?: string;
  priority?: number;
  is_active?: boolean;
  conditions?: any;
  actions?: any;
  metadata?: any;
};

type UpdateShippingRuleMutationInput = CreateShippingRuleMutationInput & {
  id: string;
};

type FilterType = ShippingRuleFilter & { setVariablesToURL?: boolean };

export type { ShippingRuleType };

export function useShippingRules({
  setVariablesToURL = false,
  ...initialData
}: FilterType = {}) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const [filter, _setFilter] = React.useState<ShippingRuleFilter>({
    ...PAGINATION,
    ...initialData,
  });
  const fetch = (variables: { filter: ShippingRuleFilter }) =>
    karrio.graphql.request<GetShippingRules>(gqlstr(GET_SHIPPING_RULES), { variables });

  // Queries
  const query = useAuthenticatedQuery({
    queryKey: ["shipping_rules", filter],
    queryFn: () => fetch({ filter }),
    keepPreviousData: true,
    staleTime: 5000,
    refetchInterval: 120000,
    onError,
  });

  function setFilter(options: ShippingRuleFilter) {
    const params = Object.keys(options).reduce((acc, key) => {
      if (["modal"].includes(key)) return acc;
      return isNoneOrEmpty(options[key as keyof ShippingRuleFilter])
        ? acc
        : {
          ...acc,
          [key]: ["offset", "first"].includes(key)
            ? parseInt((options as any)[key])
            : options[key as keyof ShippingRuleFilter],
        };
    }, PAGINATION);

    if (setVariablesToURL) insertUrlParam(params);
    _setFilter(params);

    return params;
  }

  React.useEffect(() => {
    if (query.data?.shipping_rules.page_info.has_next_page) {
      const _filter = { ...filter, offset: (filter.offset as number) + 20 };
      queryClient.prefetchQuery(["shipping_rules", _filter], () =>
        fetch({ filter: _filter }),
      );
    }
  }, [query.data, filter.offset, queryClient]);

  return {
    query,
    get filter() {
      return filter;
    },
    setFilter,
  };
}

export function useShippingRule({
  id,
  setVariablesToURL = false,
}: { id?: string; setVariablesToURL?: boolean } = {}) {
  const karrio = useKarrio();
  const [shippingRuleId, _setShippingRuleId] = React.useState<string>(id || "new");

  // Queries
  const query = useAuthenticatedQuery({
    queryKey: ["shipping_rules", id],
    queryFn: () => karrio.graphql.request<GetShippingRule>(gqlstr(GET_SHIPPING_RULE), { variables: { id: shippingRuleId } }),
    enabled: shippingRuleId !== "new",
    onError,
  });

  function setShippingRuleId(shippingRuleId: string) {
    if (setVariablesToURL) insertUrlParam({ id: shippingRuleId });
    _setShippingRuleId(shippingRuleId);
  }

  return {
    query,
    shippingRuleId,
    setShippingRuleId,
  };
}

export function useShippingRuleMutation() {
  const queryClient = useQueryClient();
  const karrio = useKarrio();
  const invalidateCache = () => {
    queryClient.invalidateQueries(["shipping_rules"]);
  };

  // Mutations
  const createShippingRule = useMutation(
    (data: CreateShippingRuleMutationInput) =>
      karrio.graphql.request<CreateShippingRule>(gqlstr(CREATE_SHIPPING_RULE), { data }),
    { onSuccess: invalidateCache, onError },
  );
  const updateShippingRule = useMutation(
    (data: UpdateShippingRuleMutationInput) =>
      karrio.graphql.request<UpdateShippingRule>(gqlstr(UPDATE_SHIPPING_RULE), { data }),
    { onSuccess: invalidateCache, onError },
  );
  const deleteShippingRule = useMutation(
    (data: { id: string }) =>
      karrio.graphql.request<DeleteMutationInput>(gqlstr(DELETE_SHIPPING_RULE), {
        data,
      }),
    { onSuccess: invalidateCache, onError },
  );

  return {
    createShippingRule,
    updateShippingRule,
    deleteShippingRule,
  };
}

type ShippingRuleDataType = (
  | CreateShippingRuleMutationInput
  | UpdateShippingRuleMutationInput
) & {
  id?: string;
};

const DEFAULT_STATE = {
  name: "",
  description: "",
  priority: 1,
  is_active: true,
  // Use empty objects instead of fields set to null so we can
  // reliably detect which sections are actually active/populated.
  conditions: {},
  actions: {},
  metadata: {},
} as ShippingRuleDataType;

export function useShippingRuleForm({ id }: { id?: string } = {}) {
  const router = useRouter();
  const karrio = useKarrio();
  const loader = useLoader();
  const { basePath } = useAppMode();
  const notifier = useNotifier();
  const mutation = useShippingRuleMutation();
  const [isNew, setIsNew] = React.useState<boolean>(true);
  const { query } = useShippingRule({ id });

  const current = query.data?.shipping_rule;
  const isLocalDraft = (id?: string) => isNoneOrEmpty(id) || id === "new";

  const form = useForm({
    defaultValues: DEFAULT_STATE,
    onSubmit: async ({ value }) => {
      try {
        loader.setLoading(true);
        const {
          id: formId,
          ...restValue
        } = value;

        // Remove read-only fields that shouldn't be sent to the API
        const {
          object_type,
          slug,
          created_at,
          updated_at,
          ...data
        } = restValue as any;

        // Filter out any undefined/null values for cleaner mutation data
        const cleanData = Object.entries(data).reduce((acc, [key, val]) => {
          if (val !== null && val !== undefined) {
            acc[key] = val;
          }
          return acc;
        }, {} as any);

        if (isLocalDraft(formId)) {
          const {
            create_shipping_rule: { shipping_rule },
          } = await mutation.createShippingRule.mutateAsync(
            cleanData as CreateShippingRuleMutationInput,
          );
          notifier.notify({
            type: NotificationType.success,
            message: "Shipping rule saved!",
          });
        } else {
          await mutation.updateShippingRule.mutateAsync({
            id: formId,
            ...cleanData,
          } as UpdateShippingRuleMutationInput);
          notifier.notify({
            type: NotificationType.success,
            message: "Shipping rule saved!",
          });
        }
      } catch (error: any) {
        notifier.notify({ type: NotificationType.error, message: error });
      } finally {
        loader.setLoading(false);
      }
    },
  });

  const deleteShippingRule = async () => {
    if (!current?.id) return;
    // Consumers should trigger a ConfirmationDialog before calling this
    try {
      loader.setLoading(true);
      await mutation.deleteShippingRule.mutateAsync({ id: current.id });
      notifier.notify({ type: NotificationType.success, message: "Shipping rule deleted!" });
      router.push(p`${basePath}/automation`.replace("//", "/"));
    } catch (error: any) {
      notifier.notify({ type: NotificationType.error, message: error });
    } finally {
      loader.setLoading(false);
    }
  };

  const handleChange = (changes: Partial<ShippingRuleDataType>) => {
    Object.entries(changes).forEach(([key, value]) => {
      form.setFieldValue(key as any, value);
    });
  };

  const handleConditionChange = (field: string, value: any) => {
    const currentConditions = form.getFieldValue("conditions") || {};
    form.setFieldValue("conditions", { ...currentConditions, [field]: value });
  };

  const handleActionChange = (field: string, value: any) => {
    const currentActions = form.getFieldValue("actions") || {};
    form.setFieldValue("actions", { ...currentActions, [field]: value });
  };

  const handleWeightChange = (field: string, value: any) => {
    const currentConditions = form.getFieldValue("conditions") || {};
    const currentWeight = currentConditions.weight || {};
    form.setFieldValue("conditions", {
      ...currentConditions,
      weight: { ...currentWeight, [field]: value }
    });
  };

  const handleSelectServiceChange = (field: string, value: any) => {
    const currentActions = form.getFieldValue("actions") || {};
    const currentSelectService = currentActions.select_service || {};
    form.setFieldValue("actions", {
      ...currentActions,
      select_service: { ...currentSelectService, [field]: value }
    });
  };

  const handleDestinationChange = (field: string, value: any) => {
    const currentConditions = form.getFieldValue("conditions") || {};
    const currentDestination = currentConditions.destination || {};
    form.setFieldValue("conditions", {
      ...currentConditions,
      destination: { ...currentDestination, [field]: value }
    });
  };

  const handleRateComparisonChange = (field: string, value: any) => {
    const currentConditions = form.getFieldValue("conditions") || {};
    const currentRateComparison = currentConditions.rate_comparison || {};
    form.setFieldValue("conditions", {
      ...currentConditions,
      rate_comparison: { ...currentRateComparison, [field]: value }
    });
  };

  React.useEffect(() => {
    setIsNew(id === "new");
  }, [id]);

  React.useEffect(() => {
    if (query.isFetched && id !== "new" && current) {
      // Reset form with the fetched data
      const formData = {
        ...DEFAULT_STATE,
        ...current,
        id: current.id,
      };

      // Set field values for existing data
      Object.entries(formData).forEach(([key, value]) => {
        form.setFieldValue(key as any, value);
      });
    }
  }, [current, query.isFetched, id, form]);

  return {
    form,
    isNew,
    query,
    current,
    shippingRule: form.state.values,
    DEFAULT_STATE,
    save: form.handleSubmit,
    deleteShippingRule,
    handleChange,
    handleConditionChange,
    handleActionChange,
    handleWeightChange,
    handleSelectServiceChange,
    handleDestinationChange,
    handleRateComparisonChange,
  };
}
