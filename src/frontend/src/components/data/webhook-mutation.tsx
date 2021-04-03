import { Operation, Webhook, WebhookData } from '@/api';
import { handleFailure } from '@/library/helper';
import { RestClient } from '@/library/rest';
import React, { useContext } from 'react';


export type WebhookMutator<T> = T & {
  addWebhook: (data: WebhookData) => Promise<Webhook>;
  updateWebhook: (data: Partial<Webhook>) => Promise<Webhook>;
  removeWebhook: (id: string) => Promise<Operation>;
}

const WebhookMutation = <T extends {}>(Component: React.FC<WebhookMutator<T>>) => (
  ({ children, ...props }: any) => {
    const purplship = useContext(RestClient);

    const addWebhook = async (data: WebhookData) => handleFailure(
      purplship.webhooks.create({ data })
    );
    const updateWebhook = async ({ id, ...data }: Partial<Webhook>) => handleFailure(
      purplship.webhooks.update({ id: id as string, data: data as any })
    );
    const removeWebhook = async (id: string) => handleFailure(
      purplship.webhooks.remove({ id })
    );

    return (
      <Component {...props}
        addWebhook={addWebhook}
        updateWebhook={updateWebhook}
        removeWebhook={removeWebhook}
      >
        {children}
      </Component>
    );
  }
);

export default WebhookMutation;
