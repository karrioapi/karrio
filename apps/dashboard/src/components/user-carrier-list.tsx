import { useCarrierConnectionMutation, useCarrierConnections } from '@/context/user-connection';
import { ConnectProviderModalContext } from '@/components/connect-provider-modal';
import { useLabelTemplateModal } from '@/components/label-template-edit-modal';
import { UpdateCarrierConnectionMutationInput } from '@karrio/graphql';
import { useRateSheetModal } from '@/components/rate-sheet-edit-modal';
import { ConfirmModalContext } from '@/components/confirm-modal';
import CarrierNameBadge from '@/components/carrier-name-badge';
import CopiableLink from '@/components/copiable-link';
import { isNone, isNoneOrEmpty } from '@/lib/helper';
import React, { useContext, useEffect } from 'react';
import { useRouter } from 'next/dist/client/router';
import { Notify } from '@/components/notifier';
import { NotificationType } from '@/lib/types';
import { Loading } from '@/components/loader';
import Spinner from '@/components/spinner';

type ConnectionUpdateType = Partial<UpdateCarrierConnectionMutationInput> & { id: string, carrier_name: string };
interface UserConnectionListView { }

const UserConnectionList: React.FC<UserConnectionListView> = () => {
  const router = useRouter();
  const { notify } = useContext(Notify);
  const ratesModal = useRateSheetModal();
  const labelModal = useLabelTemplateModal();
  const { setLoading } = useContext(Loading);
  const { confirm: confirmDeletion } = useContext(ConfirmModalContext);
  const { editConnection } = useContext(ConnectProviderModalContext);
  const mutation = useCarrierConnectionMutation();
  const { query } = useCarrierConnections();

  const update = ({ carrier_name, ...changes }: ConnectionUpdateType) => async () => {
    try {
      const data = { [carrier_name]: changes };
      await mutation.updateCarrierConnection.mutateAsync(data);
      notify({ type: NotificationType.success, message: `carrier connection updated!` });
    } catch (message: any) {
      notify({ type: NotificationType.error, message });
    }
  };
  const onDelete = (id: string) => async () => {
    try {
      await mutation.deleteCarrierConnection.mutateAsync({ id });
      notify({
        type: NotificationType.success,
        message: `carrier connection deleted!`
      });
    } catch (message: any) {
      notify({ type: NotificationType.error, message });
    }
  };

  useEffect(() => { setLoading(query.isFetching); });
  useEffect(() => {
    if (labelModal.isActive) {
      const connection = (query.data?.user_connections || []).find(c => c.id === labelModal.operation?.connection.id);
      connection && labelModal.editLabelTemplate({
        connection: connection as any, onSubmit: label_template => update({
          id: connection.id, carrier_name: connection.carrier_name, label_template
        } as any)()
      })
    }
  }, [query.data?.user_connections]);
  useEffect(() => {
    if (query.isFetching && !isNoneOrEmpty(router.query.modal)) {
      const connection = (query.data?.user_connections || []).find(c => c.id === router.query.modal);
      connection && editConnection({ connection });
    }
  }, [router.query.modal, query.data?.user_connections]);

  return (
    <>
      {(query.isFetching && !query.isFetched) && <Spinner />}

      {(query.isFetched && (query.data?.user_connections || []).length > 0) && <table className="table is-fullwidth">

        <tbody className="connections-table">
          <tr>
            <td className="is-size-7" colSpan={4}>ACCOUNTS</td>
            <td className="action"></td>
          </tr>

          {query.data!.user_connections.map((connection) => (

            <tr key={`${connection.id}-${Date.now()}`}>
              <td className="carrier pl-0">
                <CarrierNameBadge
                  carrier_name={connection.carrier_name}
                  display_name={connection.display_name}
                  className="box has-text-weight-bold"
                />
              </td>
              <td className="mode is-vcentered">
                {connection.test_mode && <span className="tag is-warning is-centered">Test</span>}
              </td>
              <td className="active is-vcentered">
                <button className="button is-white is-large" onClick={update({
                  id: connection.id,
                  carrier_name: connection.carrier_name,
                  active: !connection.active
                } as any)}>
                  <span className={`icon is-medium ${connection.active ? 'has-text-success' : 'has-text-grey'}`}>
                    <i className={`fas fa-${connection.active ? 'toggle-on' : 'toggle-off'} fa-lg`}></i>
                  </span>
                </button>
              </td>
              <td className="details">
                <div className="content is-small">
                  <ul>
                    <li>
                      <span className="is-size-7 my-1 has-text-weight-semibold">
                        carrier_name: {(connection as any).custom_carrier_name || connection.carrier_name}
                      </span>
                    </li>
                    <li>
                      <span className="is-size-7 my-1 has-text-weight-semibold">
                        carrier_id: <CopiableLink className="button is-white is-small" text={connection.carrier_id} />
                      </span>
                    </li>
                  </ul>
                </div>
              </td>
              <td className="action is-vcentered pr-0">
                <div className="buttons is-justify-content-end">
                  {!isNoneOrEmpty((connection as any).custom_carrier_name) && <button
                    title="edit label"
                    className="button is-white"
                    onClick={() => labelModal.editLabelTemplate({
                      connection: connection as any, onSubmit: label_template => update({
                        id: connection.id,
                        carrier_name: connection.carrier_name,
                        label_template,
                      } as any)()
                    })}>
                    <span className="icon is-small">
                      <i className="fas fa-sticky-note"></i>
                    </span>
                  </button>}
                  {!isNone((connection as any).services) && <button
                    title="edit rates"
                    className="button is-white"
                    onClick={() => ratesModal.editRateSheet({
                      connection: connection as any,
                      onSubmit: services => update({
                        id: connection.id,
                        carrier_name: connection.carrier_name,
                        services,
                      } as any)()
                    })}>
                    <span className="icon is-small">
                      <i className="fas fa-clipboard-list"></i>
                    </span>
                  </button>}
                  <button title="edit account" className="button is-white" onClick={() => editConnection({ connection })}>
                    <span className="icon is-small">
                      <i className="fas fa-pen"></i>
                    </span>
                  </button>
                  <button title="discard connection" className="button is-white" onClick={() => confirmDeletion({
                    identifier: connection.id,
                    label: `Delete Carrier connection`,
                    onConfirm: onDelete(connection.id),
                  })}>
                    <span className="icon is-small">
                      <i className="fas fa-trash"></i>
                    </span>
                  </button>
                </div>
              </td>
            </tr>

          ))}
        </tbody>

      </table>}

      {(query.isFetched && (query.data?.user_connections || []).length == 0) && <div className="card my-6">

        <div className="card-content has-text-centered">
          <p>No carriers have been connected yet.</p>
          <p>Use the <strong>Register a Carrier</strong> button above to add a new connection</p>
        </div>

      </div>}

    </>
  );
}

export default UserConnectionList;
