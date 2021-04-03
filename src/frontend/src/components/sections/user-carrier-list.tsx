import React, { Fragment, useContext, useEffect } from 'react';
import ConnectProviderModal from '@/components/connect-provider-modal';
import DisconnectProviderButton from '@/components/disconnect-provider-button';
import CarrierBadge from '@/components/carrier-badge';
import { UserConnections, UserConnectionType } from '@/components/data/user-connections-query';
import ConnectionMutation from '@/components/data/connection-mutation';
import { Loading } from '@/components/loader';

interface UserConnectionListView { }

const UserConnectionList: React.FC<UserConnectionListView> = ConnectionMutation<UserConnectionListView>(({ updateConnection }) => {
  const { setLoading } = useContext(Loading);
  const { user_connections, loading, load, refetch } = useContext(UserConnections);

  const update = async (_?: React.MouseEvent) => refetch && await refetch();
  const toggle = ({ __typename, active, id }: UserConnectionType) => async () => {
    const data = {[__typename.toLowerCase()]: { id, active: !active }};
    await updateConnection({ id, ...data });
    update();
  };
  
  useEffect(() => { !loading && load() }, []);
  useEffect(() => { setLoading(loading); });

  return (
    <Fragment>
      <table className="table is-fullwidth">

        <thead className="connections-table">
          <tr>
            <th colSpan={4}>Carrier</th>
            <th className="action"></th>
          </tr>
        </thead>

        <tbody className="connections-table">
          {user_connections.map((connection) => (

            <tr key={`${connection.id}-${Date.now()}`}>
              <td className="carrier">
                <CarrierBadge carrier={connection.carrier_name} className="box has-text-weight-bold" />
              </td>
              <td className="mode is-vcentered">
                {connection.test ? <span className="tag is-warning is-centered">Test</span> : <></>}
              </td>
              <td className="active is-vcentered">
                <button className="button is-white is-large" onClick={toggle(connection)}>
                  <span className={`icon is-medium ${connection.active ? 'has-text-success' : 'has-text-grey'}`}>
                    <i className={`fas fa-${connection.active ? 'toggle-on' : 'toggle-off'} fa-lg`}></i>
                  </span>
                </button>
              </td>
              <td className="details">
                <div className="content is-small">
                  <ul>
                    <li>carrier id: <span className="tag is-info is-light" title="carrier nickname">{connection.carrier_id}</span></li>
                  </ul>
                </div>
              </td>
              <td className="action is-vcentered">
                <div className="buttons is-centered">
                  <ConnectProviderModal connection={connection} className="button is-light is-info" onUpdate={update}>
                    <span className="icon is-small">
                      <i className="fas fa-pen"></i>
                    </span>
                  </ConnectProviderModal>
                  <DisconnectProviderButton connection={connection}>
                    <span className="icon is-small">
                      <i className="fas fa-trash"></i>
                    </span>
                  </DisconnectProviderButton>
                </div>
              </td>
            </tr>

          ))}
        </tbody>

      </table>

      {(user_connections.length == 0) && <div className="card my-6">

        <div className="card-content has-text-centered">
          <p>No carriers have been connected yet.</p>
          <p>Use the <strong>Connect a Carrier</strong> button above to add a new connection</p>
        </div>

      </div>}

    </Fragment>
  );
});

export default UserConnectionList;