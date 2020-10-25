import React, { Fragment, useEffect } from 'react';
import { View } from '@/library/types';
import { PaginatedConnections, state } from '@/library/api';
import ConnectProviderModal from '@/components/connect-provider-modal';
import { Reference } from '@/library/context';
import DisconnectProviderButton from '@/components/disconnect-provider-button';

interface ConnectionsView extends View {
  connections?: PaginatedConnections;
}

const Connections: React.FC<ConnectionsView> = ({ connections }) => {
  useEffect(() => { if(connections === undefined) state.fetchConnections(); }, []);
  return (
    <Fragment>

      <header className="px-2 pt-1 pb-6">
        <span className="subtitle is-4">Carrier Connections</span>
        <ConnectProviderModal className="button is-success is-pulled-right">
          <span>Connect a Carrier</span>
        </ConnectProviderModal>
      </header>

      {(connections?.count == 0) && <div className="card my-6">

        <div className="card-content has-text-centered">
          <p>No carriers have been connected yet.</p>
          <p>Use the <strong>Connect a Carrier</strong> button above to add a new connection</p>
        </div>

      </div>}

      <div className="table-container">
        <table className="table is-fullwidth">

          <tbody className="connections-table">
            <Reference.Consumer>
              {ref => (Object.values(ref || {}).length > 0) && connections?.results.map((settings) => (

                <tr key={settings.id}>
                  <td className="carrier"><div className="box">{ref.carriers[settings.carrier_name]}</div></td>
                  <td className="mode is-vcentered">
                    {settings.test ? <span className="tag is-warning is-centered">Test</span> : <></>}
                  </td>
                  <td className="details"></td>
                  <td className="action is-vcentered">
                    <div className="buttons is-centered">
                      <ConnectProviderModal className="button" connection={settings}>
                        <span className="icon is-small">
                          <i className="fas fa-pen"></i>
                        </span>
                      </ConnectProviderModal>
                      <DisconnectProviderButton connection={settings}>
                        <span className="icon is-small">
                          <i className="fas fa-trash"></i>
                        </span>
                      </DisconnectProviderButton>
                    </div>
                  </td>
                </tr>

              ))}
            </Reference.Consumer>
          </tbody>

        </table>
      </div>

    </Fragment>
  );
}

export default Connections;