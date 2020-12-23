import React, { Fragment, useEffect, useState } from 'react';
import { View } from '@/library/types';
import { Connection, ConnectionData, PaginatedConnections, state } from '@/library/api';
import ConnectProviderModal from '@/components/connect-provider-modal';
import DisconnectProviderButton from '@/components/disconnect-provider-button';
import CarrierBadge from '@/components/carrier-badge';

interface ConnectionsView extends View {
  connections?: PaginatedConnections;
}

const Connections: React.FC<ConnectionsView> = ({ connections }) => {
  const [loading, setLoading] = useState<boolean>(false);

  const update = (url?: string | null) => async (_?: React.MouseEvent) => {
    await state.fetchConnections(url as string);
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
    if ((connections === undefined || connections?.fetched === false) && loading === false) {
      setLoading(true);
      state.fetchConnections().catch(_ => _).then(() => setLoading(false));
    }
  }, connections?.results);

  return (
    <Fragment>

      <header className="px-2 pt-1 pb-6">
        <span className="subtitle is-4">Carriers</span>
        <ConnectProviderModal className="button is-success is-pulled-right">
          <span>Connect a Carrier</span>
        </ConnectProviderModal>
      </header>

      <div className="table-container">
        <table className="table is-fullwidth">

          <thead className="connections-table">
            <tr>
              <th colSpan={4}>Carrier Connections</th>
              <th className="action"></th>
            </tr>
          </thead>

          <tbody className="connections-table">
            {connections?.results.map((connection) => (

              <tr key={connection.id}>
                <td className="carrier">
                  <CarrierBadge name={connection.carrier_name as string} className="box has-text-weight-bold" />
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
      </div>

    </Fragment>
  );
}

export default Connections;