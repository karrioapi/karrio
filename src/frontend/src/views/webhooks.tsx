import React, { useContext, useEffect } from 'react';
import { View } from '@/library/types';
import EditWebhookModal from '@/components/webhook-edit-modal';
import { Webhooks } from '@/components/data/webhooks-query';
import DeleteItemModal from '@/components/delete-item-modal';
import WebhookMutation from '@/components/data/webhook-mutation';
import { Loading } from '@/components/loader';


interface WebhooksView extends View { }

const WebhooksPage: React.FC<WebhooksView> = WebhookMutation<WebhooksView>(({ removeWebhook }) => {
  const { setLoading } = useContext(Loading);
  const { called, loading, results, load, refetch } = useContext(Webhooks);

  const refresh = () => refetch && refetch();
  const remove = (id: string) => async () => {
    await removeWebhook(id);
    refresh();
  };

  useEffect(() => { !loading && load(); }, []);
  useEffect(() => { setLoading(loading); });

  return (
    <>

      <header className="px-2 pt-1 pb-6">
        <span className="subtitle is-4">Endpoints</span>
        {called && <EditWebhookModal className="button is-success is-pulled-right">
          <span>Add endpoint</span>
        </EditWebhookModal>}
      </header>

      <div className="table-container">
        <table className="table is-fullwidth">

          <thead className="webhooks-table">
            <tr>
              <th className="active">active</th>
              <th className="url">url</th>
              <th className="mode">mode</th>
              <th className="action"></th>
            </tr>
          </thead>

          <tbody>

            {results.map(webhook => (
              <tr key={webhook.id}>
                <td className="active is-vcentered">
                  {webhook.disabled ? <i className="fas fa-circle"></i> : <i className="fas fa-circle is-active"></i>}
                </td>
                <td>
                  <span className="is-subtitle is-size-7 has-text-weight-semibold has-text-grey">{webhook.url}</span>
                </td>
                <td className="mode is-vcentered">
                  <span className={`tag ${webhook.test_mode ? 'is-warning' : 'is-success'} is-centered`}>
                    {webhook.test_mode ? 'test': 'live'}
                  </span>
                </td>
                <td className="action is-vcentered">
                  <div className="buttons is-centered">
                    <EditWebhookModal webhook={webhook} className="button is-light is-info">
                      <span className="icon is-small">
                        <i className="fas fa-pen"></i>
                      </span>
                    </EditWebhookModal>
                    <DeleteItemModal label="Parcel Template" identifier={webhook.id as string} onConfirm={remove(webhook.id as string)}>
                      <span className="icon is-small">
                        <i className="fas fa-trash"></i>
                      </span>
                    </DeleteItemModal>
                  </div>
                </td>
              </tr>
            ))}

          </tbody>

        </table>
      </div>

      {(!loading && results.length == 0) && <div className="card my-6">

        <div className="card-content has-text-centered">
          <p>No webhooks added yet.</p>
          <p>Use the <strong>API</strong> to track your first shipment.</p>
        </div>

      </div>}

      {loading && <div className="card my-6">

        <div className="card-content has-text-centered">
          <span className="icon has-text-info is-large">
            <i className="fas fa-spinner fa-pulse"></i>
          </span>
        </div>

      </div>}

    </>
  );
});


export default WebhooksPage;