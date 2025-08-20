import {
  GET_API_KEYS,
  CREATE_API_KEY,
  DELETE_API_KEY,
} from "@karrio/types/graphql/queries";
import {
  gqlstr,
  onError,
} from "@karrio/lib";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useNotifier } from "@karrio/ui/core/components/notifier";
import { useLoader } from "@karrio/ui/core/components/loader";
import { useAuthenticatedQuery, useKarrio } from "./karrio";
import { NotificationType } from "@karrio/types";
import { useForm } from "@tanstack/react-form";

type APIKeyType = {
  object_type: string;
  key: string;
  label: string;
  test_mode: boolean;
  created: string;
  permissions: string[];
};

type GetAPIKeys = {
  api_keys: APIKeyType[];
};

type CreateAPIKey = {
  create_api_key: {
    api_key?: APIKeyType;
    errors: { field: string; messages: string[] }[];
  };
};

type DeleteAPIKey = {
  delete_api_key: {
    label?: string;
    errors: { field: string; messages: string[] }[];
  };
};

type CreateAPIKeyMutationInput = {
  password: string;
  label: string;
  permissions?: string[];
};

type DeleteAPIKeyMutationInput = {
  password: string;
  key: string;
};

export type { APIKeyType };

export function useAPIKeys() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const fetch = () => karrio.graphql.request<GetAPIKeys>(gqlstr(GET_API_KEYS));

  const query = useAuthenticatedQuery({
    queryKey: ["api_keys"],
    queryFn: fetch,
    keepPreviousData: true,
    staleTime: 5000,
    refetchInterval: 120000,
    onError,
  });

  return {
    query,
  };
}

export function useAPIKeyMutation() {
  const queryClient = useQueryClient();
  const karrio = useKarrio();
  const invalidateCache = () => {
    // Invalidate all related queries to ensure data refresh
    queryClient.invalidateQueries({ queryKey: ["api_keys"] });
    // Force refetch to ensure UI updates immediately
    queryClient.refetchQueries({ queryKey: ["api_keys"] });
  };

  const createAPIKey = useMutation(
    (data: CreateAPIKeyMutationInput) =>
      karrio.graphql.request<CreateAPIKey>(gqlstr(CREATE_API_KEY), { data }),
    { onSuccess: invalidateCache, onError },
  );

  const deleteAPIKey = useMutation(
    (data: DeleteAPIKeyMutationInput) =>
      karrio.graphql.request<DeleteAPIKey>(gqlstr(DELETE_API_KEY), { data }),
    { onSuccess: invalidateCache, onError },
  );

  return {
    createAPIKey,
    deleteAPIKey,
  };
}

type APIKeyFormData = {
  password: string;
  label: string;
  permissions: string[];
};

const DEFAULT_STATE: APIKeyFormData = {
  password: "",
  label: "",
  permissions: [],
};

export function useAPIKeyForm() {
  const loader = useLoader();
  const notifier = useNotifier();
  const mutation = useAPIKeyMutation();

  const form = useForm({
    defaultValues: DEFAULT_STATE,
    onSubmit: async ({ value }) => {
      try {
        loader.setLoading(true);
        const { create_api_key: { api_key, errors } } = await mutation.createAPIKey.mutateAsync(value);

        if (errors && errors.length > 0) {
          const errorMessages = errors.map(e => e.messages.join(", ")).join("; ");
          notifier.notify({
            type: NotificationType.error,
            message: errorMessages,
          });
        } else {
          notifier.notify({
            type: NotificationType.success,
            message: "API key created successfully!",
          });
          form.reset();
          return api_key;
        }
      } catch (error: any) {
        notifier.notify({ type: NotificationType.error, message: error.message || "Failed to create API key" });
      } finally {
        loader.setLoading(false);
      }
    },
  });

  const deleteAPIKey = async (key: string, password: string) => {
    if (confirm("Are you sure you want to delete this API key? This action cannot be undone.")) {
      try {
        loader.setLoading(true);
        const { delete_api_key: { errors } } = await mutation.deleteAPIKey.mutateAsync({ key, password });

        if (errors && errors.length > 0) {
          const errorMessages = errors.map(e => e.messages.join(", ")).join("; ");
          notifier.notify({
            type: NotificationType.error,
            message: errorMessages,
          });
        } else {
          notifier.notify({
            type: NotificationType.success,
            message: "API key deleted successfully!",
          });
        }
      } catch (error: any) {
        notifier.notify({ type: NotificationType.error, message: error.message || "Failed to delete API key" });
      } finally {
        loader.setLoading(false);
      }
    }
  };

  return {
    form,
    deleteAPIKey,
    save: form.handleSubmit,
    DEFAULT_STATE,
  };
}
