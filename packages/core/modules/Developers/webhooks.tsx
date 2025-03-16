"use client";
import {
  WebhookTestModal,
  useTestWebhookModal,
} from "@karrio/ui/core/modals/webhook-test-modal";
import {
  WebhookEditModal,
  useWebhookModal,
} from "@karrio/ui/core/modals/webhook-edit-modal";
import {
  ConfirmModal,
  useConfirmModalContext,
} from "@karrio/ui/core/modals/confirm-modal";
import { useWebhookMutation, useWebhooks } from "@karrio/hooks/webhook";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import { NotificationType, WebhookType } from "@karrio/types";
import { useNotifier } from "@karrio/ui/core/components/notifier";
import { formatDateTime, isNoneOrEmpty } from "@karrio/lib";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { useSearchParams } from "next/navigation";
import { useEffect } from "react";
import React from "react";

export const generateMetadata = dynamicMetadata("Webhooks");

export default function WebhooksPage(pageProps: any) {
  const Component = (): JSX.Element => {
    const searchParams = useSearchParams();
    const modal = searchParams.get("modal");
    const { query } = useWebhooks();
    const mutation = useWebhookMutation();
    const { notify } = useNotifier();
    const { editWebhook } = useWebhookModal();
    const { testWebhook } = useTestWebhookModal();
    const { confirm: confirmDeletion } = useConfirmModalContext();
    const [initialized, setInitialized] = React.useState(false);

    const remove = (id: string) => async () => {
      await mutation.deleteWebhook.mutateAsync({ id });
    };
    const toggle =
      ({ disabled, id }: WebhookType) =>
        async () => {
          try {
            await mutation.updateWebhook.mutateAsync({ id, disabled: !disabled });
            notify({
              type: NotificationType.success,
              message: `webhook ${!disabled ? "activated" : "deactivated"}!`,
            });
          } catch (message: any) {
            notify({ type: NotificationType.error, message });
          }
        };

    useEffect(() => {
      if (query.isFetched && !initialized && !isNoneOrEmpty(modal)) {
        const webhook = query.data?.webhooks.edges.find(
          (c) => c.node.id === modal,
        );
        webhook && editWebhook({ webhook } as any);
        setInitialized(true);
      }
    }, [modal, query.isFetched]);

    return (
      <>
        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <span className="title is-4">Developers</span>
          <div>
            <button
              className="button is-small is-default is-pulled-right"
              onClick={() => editWebhook()}
            >
              <span className="icon">
                <i className="fas fa-plus"></i>
              </span>
              <span>Add endpoint</span>
            </button>
          </div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/developers" shallow={false} prefetch={false}>
                <span>Overview</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink
                href="/developers/apikeys"
                shallow={false}
                prefetch={false}
              >
                <span>API Keys</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
              <AppLink
                href="/developers/webhooks"
                shallow={false}
                prefetch={false}
              >
                <span>Webhooks</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink
                href="/developers/events"
                shallow={false}
                prefetch={false}
              >
                <span>Events</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/developers/logs" shallow={false} prefetch={false}>
                <span>Logs</span>
              </AppLink>
            </li>
          </ul>
        </div>

        {(query.data?.webhooks.edges || []).length > 0 && (
          <>
            <div className="table-container">
              <table className="webhooks-table table is-fullwidth">
                <tbody>
                  <tr>
                    <td className="url is-size-7 is-vcentered">URL</td>
                    <td className="mode is-size-7 is-vcentered">MODE</td>
                    <td className="last_event is-size-7 is-vcentered">
                      LAST EVENT
                    </td>
                    <td className="action pr-1"></td>
                  </tr>

                  {(query.data?.webhooks.edges || []).map(
                    ({ node: webhook }) => (
                      <tr key={webhook.id}>
                        <td
                          className="url is-vcentered is-clickable"
                          onClick={() => editWebhook({ webhook })}
                        >
                          <span className="is-subtitle is-size-7 has-text-weight-semibold has-text-grey text-ellipsis">
                            {webhook.url}
                          </span>
                        </td>
                        <td
                          className="mode is-vcentered is-centered is-clickable p-1"
                          onClick={() => editWebhook({ webhook })}
                        >
                          <span
                            className={`tag ${webhook.test_mode ? "is-warning" : "is-success"} is-centered`}
                          >
                            {webhook.test_mode ? "test" : "live"}
                          </span>
                        </td>
                        <td
                          className="last-event is-vcentered is-clickable"
                          onClick={() => editWebhook({ webhook })}
                        >
                          <span className="is-subtitle is-size-7 has-text-weight-semibold has-text-grey text-ellipsis">
                            {webhook.last_event_at
                              ? formatDateTime(webhook.last_event_at as any)
                              : "No recent event"}
                          </span>
                        </td>
                        <td className="action is-flex is-justify-content-end px-0">
                          <button
                            className="button is-white"
                            onClick={toggle(webhook)}
                          >
                            <span
                              className={`icon is-medium ${webhook.disabled ? "has-text-grey" : "has-text-success"}`}
                            >
                              <i
                                className={`fas fa-${webhook.disabled ? "toggle-off" : "toggle-on"} fa-lg`}
                              ></i>
                            </span>
                          </button>
                          <button
                            className="button is-white"
                            onClick={() => testWebhook({ webhook })}
                          >
                            <span className="icon is-small">
                              <i className="fas fa-flask"></i>
                            </span>
                          </button>
                          <button
                            className="button is-white"
                            onClick={() =>
                              confirmDeletion({
                                label: "Delete Webhook endpoint",
                                identifier: webhook.id as string,
                                onConfirm: remove(webhook.id as string),
                              })
                            }
                          >
                            <span className="icon is-small">
                              <i className="fas fa-trash"></i>
                            </span>
                          </button>
                        </td>
                      </tr>
                    ),
                  )}
                </tbody>
              </table>
            </div>
          </>
        )}

        {query.isFetched && (query.data?.webhooks.edges || []).length == 0 && (
          <div className="card my-6">
            <div className="card-content has-text-centered">
              <p>No webhooks added yet.</p>
              <p>
                Use the <strong>Add Enpoint</strong> button above to add
              </p>
            </div>
          </div>
        )}
      </>
    );
  };

  return (
    <>
      <WebhookEditModal>
        <WebhookTestModal>
          <ConfirmModal>
            <Component />
          </ConfirmModal>
        </WebhookTestModal>
      </WebhookEditModal>
    </>
  );
}
