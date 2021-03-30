import React, { Fragment, useContext, useEffect, useState } from 'react';
import { Connection, ConnectionData } from '@/library/types';
import ConnectProviderModal from '@/components/connect-provider-modal';
import DisconnectProviderButton from '@/components/disconnect-provider-button';
import CarrierBadge from '@/components/carrier-badge';
import { state } from '@/library/app';
import { UserConnections } from '@/library/context';
import { CarrierSettings } from '@/api';

interface UserConnectionListView { }

const UserConnectionList: React.FC<UserConnectionListView> = () => {
  const connections = useContext(UserConnections)
  const [loading, setLoading] = useState<boolean>(false);

  const update = (url?: string | null) => async (_?: React.MouseEvent) => {
    await state.fetchUserConnections(url as string);
  };
  const toggle = (connection: Connection) => async () => {
    const data = {
      carrier_name: connection.carrier_name,
      carrier_config: { ...connection, active: !connection.active }
    } as ConnectionData;
    await state.updateConnection(connection.id as string, data);
    update(connections?.url)();
  };
  useEffect(() => {
    if (loading === false) {
      setLoading(true);
      state.fetchUserConnections().catch(_ => _).then(() => setLoading(false));
    }
  }, []);

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
          {connections?.results.map((connection) => (

            <tr key={connection.id}>
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
                  <ConnectProviderModal connection={connection} className="button is-light is-info">
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

      {(connections?.count == 0) && <div className="card my-6">

        <div className="card-content has-text-centered">
          <p>No carriers have been connected yet.</p>
          <p>Use the <strong>Connect a Carrier</strong> button above to add a new connection</p>
        </div>

      </div>}

    </Fragment>
  );
}

export default UserConnectionList;