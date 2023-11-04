import WebhookTestModal, { useTestWebhookModal } from "@/components/webhook-test-modal";
import WebhookEditModal, { useWebhookModal } from "@/components/webhook-edit-modal";
import ConfirmModal, { ConfirmModalContext } from "@/components/confirm-modal";
import { useWebhookMutation, useWebhooks } from "@/context/webhook";
import AuthenticatedPage from "@/layouts/authenticated-page";
import { formatDateTime, isNoneOrEmpty } from "@/lib/helper";
import { NotificationType, WebhookType } from "@/lib/types";
import DashboardLayout from "@/layouts/dashboard-layout";
import { useRouter } from "next/dist/client/router";
import { Notify } from "@/components/notifier";
import { useContext, useEffect } from "react";
import Head from "next/head";
import React from "react";

export { getServerSideProps } from "@/lib/data-fetching";


export default function WebhooksPage(pageProps: any) {
  const Component: React.FC = () => {
    const router = useRouter();
    const { query } = useWebhooks();
    const mutation = useWebhookMutation();
    const { notify } = useContext(Notify);
    const { editWebhook } = useWebhookModal();
    const { testWebhook } = useTestWebhookModal();
    const { confirm: confirmDeletion } = useContext(ConfirmModalContext);
    const [initialized, setInitialized] = React.useState(false);

    const remove = (id: string) => async () => {
      await mutation.deleteWebhook.mutateAsync({ id });
    };
    const toggle = ({ disabled, id }: WebhookType) => async () => {
      try {
        await mutation.updateWebhook.mutateAsync({ id, disabled: !disabled });
        notify({
          type: NotificationType.success,
          message: `webhook ${!disabled ? 'activated' : 'deactivated'}!`
        });
      } catch (message: any) {
        notify({ type: NotificationType.error, message });
      }
    };

    useEffect(() => {
      if (query.isFetched && !initialized && !isNoneOrEmpty(router.query.modal)) {
        const webhook = query.data?.webhooks.edges.find(c => c.node.id === router.query.modal);
        webhook && editWebhook({ webhook } as any);
        setInitialized(true);
      }
    }, [router.query.modal, query.isFetched]);

    return (
      <>
        <header className="px-0 pb-3 pt-6">
          <span className="title is-4">Endpoints</span>
          <button className="button is-default is-pulled-right" onClick={() => editWebhook()}>
            <span className="icon"><i className="fas fa-plus"></i></span>
            <span>Add endpoint</span>
          </button>
        </header>

        {((query.data?.webhooks.edges || []).length > 0) && <div className="table-container">
          <table className="webhooks-table table is-fullwidth">

            <tbody>
              <tr>
                <td className="url is-size-7">URL</td>
                <td className="mode is-size-7">MODE</td>
                <td className="last_event is-size-7">LAST EVENT</td>
                <td className="action"></td>
              </tr>

              {(query.data?.webhooks.edges || []).map(({ node: webhook }) => (
                <tr key={webhook.id}>
                  <td className="url is-vcentered is-clickable" onClick={() => editWebhook({ webhook })}>
                    <span className="is-subtitle is-size-7 has-text-weight-semibold has-text-grey">{webhook.url}</span>
                  </td>
                  <td className="mode is-vcentered is-centered is-clickable p-1" onClick={() => editWebhook({ webhook })}>
                    <span className={`tag ${webhook.test_mode ? 'is-warning' : 'is-success'} is-centered`}>
                      {webhook.test_mode ? 'test' : 'live'}
                    </span>
                  </td>
                  <td className="last-event is-vcentered is-clickable" onClick={() => editWebhook({ webhook })}>
                    <span className="is-subtitle is-size-7 has-text-weight-semibold has-text-grey">
                      {webhook.last_event_at ? formatDateTime(webhook.last_event_at as any) : "No recent event"}
                    </span>
                  </td>
                  <td className="action is-flex is-justify-content-end px-0">
                    <button className="button is-white" onClick={toggle(webhook)}>
                      <span className={`icon is-medium ${webhook.disabled ? 'has-text-grey' : 'has-text-success'}`}>
                        <i className={`fas fa-${webhook.disabled ? 'toggle-off' : 'toggle-on'} fa-lg`}></i>
                      </span>
                    </button>
                    <button className="button is-white" onClick={() => testWebhook({ webhook })}>
                      <span className="icon is-small">
                        <i className="fas fa-flask"></i>
                      </span>
                    </button>
                    <button className="button is-white" onClick={() => confirmDeletion({
                      label: "Delete Webhook endpoint",
                      identifier: webhook.id as string,
                      onConfirm: remove(webhook.id as string),
                    })}>
                      <span className="icon is-small">
                        <i className="fas fa-trash"></i>
                      </span>
                    </button>
                  </td>
                </tr>
              ))}

            </tbody>

          </table>
        </div>}

        {(query.isFetched && (query.data?.webhooks.edges || []).length == 0) &&
          <div className="card my-6">

            <div className="card-content has-text-centered">
              <p>No webhooks added yet.</p>
              <p>Use the <strong>Add Enpoint</strong> button above to add</p>
            </div>

          </div>}

      </>
    );
  };

  return AuthenticatedPage(<>
    <DashboardLayout showModeIndicator={true}>
      <Head><title>{`Webhooks - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>

      <WebhookEditModal>
        <WebhookTestModal>
          <ConfirmModal>
            <Component />
          </ConfirmModal>
        </WebhookTestModal>
      </WebhookEditModal>

    </DashboardLayout>
  </>, pageProps);
}
