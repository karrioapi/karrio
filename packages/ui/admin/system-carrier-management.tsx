import { useSystemCarrierConnectionMutation, useSystemCarrierConnections } from "@karrio/hooks/admin/connections";
import { UpdateConnectionMutationInput } from "@karrio/types/graphql/admin";
import { useConnectCarrierModal } from "../modals/connect-provider-modal";
import { CarrierImage } from "../components/carrier-image";
import { CopiableLink } from "../components/copiable-link";
import { useConfirmModal } from "../modals/confirm-modal";
import { useNotifier } from "../components/notifier";
import { useRouter } from 'next/dist/client/router';
import { NotificationType } from "@karrio/types";
import { useLoader } from "../components/loader";
import { Spinner } from "../components/spinner";
import { isNoneOrEmpty } from "@karrio/lib";
import React from "react";
import { CarrierBadge } from "../components/carrier-badge";


type ConnectionUpdateType = Partial<UpdateConnectionMutationInput> & { id: string, carrier_name: string };
interface SystemCarrierManagementComponent { }

export const SystemCarrierManagement: React.FC<SystemCarrierManagementComponent> = () => {
  const router = useRouter();
  const { notify } = useNotifier();
  const { setLoading } = useLoader();
  const { confirm: confirmDeletion } = useConfirmModal();
  const { editConnection } = useConnectCarrierModal();
  const mutation = useSystemCarrierConnectionMutation();
  const { query: { data: { system_connections = [] } = {}, ...query } } = useSystemCarrierConnections();

  const update = ({ carrier_name, ...changes }: ConnectionUpdateType) => async () => {
    try {
      const data = { [carrier_name]: changes };
      await mutation.updateSystemCarrierConnection.mutateAsync(data);
      notify({ type: NotificationType.success, message: `carrier connection updated!` });
    } catch (message: any) {
      notify({ type: NotificationType.error, message });
    }
  };
  const onDelete = (id: string) => async () => {
    try {
      await mutation.deleteSystemCarrierConnection.mutateAsync({ id });
      notify({
        type: NotificationType.success,
        message: `carrier connection deleted!`
      });
    } catch (message: any) {
      notify({ type: NotificationType.error, message });
    }
  };

  React.useEffect(() => { setLoading(query.isFetching); });
  React.useEffect(() => {
    if (query.isFetching && !isNoneOrEmpty(router.query.modal)) {
      const connection = system_connections.find(c => c.id === router.query.modal);
      connection && editConnection({
        connection: connection as any,
        update: mutation.updateSystemCarrierConnection.mutateAsync,
      });
    }
  }, [router.query.modal, system_connections]);

  return (
    <>
      <div className="card px-0" style={{ maxHeight: '500px', minHeight: '500px' }}>
        <header className="px-3 mt-3 is-flex is-justify-content-space-between">
          <span className="is-title is-size-6 has-text-weight-bold is-vcentered my-2">System carrier accounts</span>
          <div className="is-vcentered">
            <button className="button is-primary is-small is-pulled-right" onClick={() => editConnection({
              create: mutation.createSystemCarrierConnection.mutateAsync,
            })}>
              <span>Add account</span>
            </button>
          </div>
        </header>

        <hr className='my-1' style={{ height: '1px' }} />

        <div className="p-0">

          {(query.isFetching && !query.isFetched) && <Spinner />}

          {(query.isFetched && system_connections.length > 0) && <>
            <div className="table-container px-2" style={{ overflowY: 'auto', maxHeight: '430px' }}>
              <table className="table is-fullwidth">

                <tbody className="admin-connections-table">

                  {system_connections.map((connection) => (

                    <tr key={`${connection.id}-${Date.now()}`}>
                      <td className="carrier is-vcentered pl-1">
                        <CarrierBadge
                          className="has-background-primary has-text-weight-bold has-text-white-bis is-size-7"
                          carrier_name={connection!.carrier_name == 'generic' ? connection.display_name : connection!.carrier_name}
                          width={150}
                          height={40}
                        />
                      </td>
                      <td className="mode is-vcentered">
                        {connection.test_mode && <span className="tag is-warning is-centered">Test</span>}
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
                          <button className="button is-white" onClick={update({
                            id: connection.id,
                            carrier_name: connection.carrier_name,
                            active: !connection.active
                          } as any)}>
                            <span className={`icon is-medium ${connection.active ? 'has-text-success' : 'has-text-grey'}`}>
                              <i className={`fas fa-${connection.active ? 'toggle-on' : 'toggle-off'} fa-lg`}></i>
                            </span>
                          </button>
                          <button
                            title="edit account" className="button is-white"
                            onClick={() => editConnection({
                              connection: connection as any,
                              update: mutation.updateSystemCarrierConnection.mutateAsync,
                            })}
                          >
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

              </table>
            </div>
          </>}

          {(query.isFetched && system_connections.length == 0) && <div className="message is-white my-6">

            <div className="card-content has-text-centered">
              <p>No system carrier connections configured.</p>
              <p>Use the <strong>Add account</strong> button above to add a new connection</p>
            </div>

          </div>}

        </div>
      </div>
    </>
  )
};
