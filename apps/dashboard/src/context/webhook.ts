import { WebhookFilter, get_webhooks, GET_WEBHOOKS, GET_WEBHOOK, get_webhook } from "@karrio/graphql";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, handleFailure, onError } from "@/lib/helper";
import { Webhook, WebhookData } from "@karrio/rest";
import { useKarrio } from "@/lib/client";
import React from "react";

const PAGE_SIZE = 20;
const PAGINATION = { offset: 0, first: PAGE_SIZE };

export function useWebhooks() {
  const karrio = useKarrio();
  const [filter, setFilter] = React.useState<WebhookFilter>(PAGINATION);

  // Queries
  const query = useQuery(
    ['webhooks'],
    () => karrio.graphql$.request<get_webhooks>(gqlstr(GET_WEBHOOKS), { variables: filter }),
    { keepPreviousData: true, staleTime: 5000, onError },
  );

  return {
    query,
    filter,
    setFilter,
  };
}

export function useWebhook(id: string) {
  const karrio = useKarrio();

  // Queries
  const query = useQuery(
    ['webhooks', id],
    () => karrio.graphql$.request<get_webhook>(gqlstr(GET_WEBHOOK), { data: { id } }),
    { onError }
  );

  return {
    query,
  };
}


export function useWebhookMutation() {
  const queryClient = useQueryClient();
  const karrio = useKarrio();
  const invalidateCache = () => { queryClient.invalidateQueries(['webhooks']) };

  // Mutations
  const createWebhook = useMutation(
    (webhookData: WebhookData) => handleFailure(karrio.rest$.webhooks.create({ webhookData })),
    { onSuccess: invalidateCache, onError }
  );
  const updateWebhook = useMutation(
    ({ id, ...patchedWebhookData }: Partial<Webhook>) => handleFailure(karrio.rest$.webhooks.update({ id, patchedWebhookData } as any)),
    { onSuccess: invalidateCache, onError }
  );
  const deleteWebhook = useMutation(
    (data: { id: string }) => handleFailure(karrio.rest$.webhooks.remove(data)),
    { onSuccess: invalidateCache, onError }
  );
  const testWebhook = useMutation(
    ({ id, payload }: { id: string, payload: object }) => handleFailure(karrio.rest$.webhooks.test({ id, webhookTestRequest: { payload } })),
    { onSuccess: invalidateCache, onError }
  );

  return {
    createWebhook,
    updateWebhook,
    deleteWebhook,
    testWebhook,
  };
}
