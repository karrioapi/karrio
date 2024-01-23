import { useSystemConnectionMutation, useSystemConnections } from '@karrio/hooks/system-connection';
import { ConnectionDescription } from '../components/connection-description';
import { CarrierNameBadge } from '../components/carrier-name-badge';
import { useAppMode } from '@karrio/hooks/app-mode';
import { NotificationType } from '@karrio/types';
import { Notify } from '../components/notifier';
import React, { useContext } from 'react';
import { jsonify } from '@karrio/lib';


export const SystemConnectionList: React.FC = () => {
  const { testMode } = useAppMode();
  const { notify } = useContext(Notify);
  const { query } = useSystemConnections();
  const { updateSystemConnection } = useSystemConnectionMutation();

  const toggle = ({ enabled, id }: any) => async () => {
    try {
      await updateSystemConnection.mutateAsync({ id, enable: !enabled });
      notify({
        type: NotificationType.success,
        message: `system carrier connection ${!enabled ? 'enabled' : 'disabled'}!`
      });
    } catch (message: any) {
      notify({ type: NotificationType.error, message });
    }
  };

  return (
    <>

      {((query.data?.system_connections || []).length > 0) && <>
        <div className="table-container">
          <table className="table is-fullwidth">

            <tbody className="system-connections-table">
              <tr>
                <td className="is-size-7" colSpan={testMode ? 4 : 3}>ACCOUNTS</td>
              </tr>

              {(query.data?.system_connections || []).map((connection) => (

                <tr key={`connection-${connection.id}-${Date.now()}`}>
                  <td className="carrier is-vcentered pl-1">
                    <CarrierNameBadge
                      carrier_name={connection.carrier_name}
                      display_name={connection.display_name}
                      className="box p-3 has-text-weight-bold"
                      customTheme={!!connection.config?.brand_color ? '' : undefined}
                      style={JSON.parse(jsonify({
                        background: connection.config?.brand_color,
                        color: connection.config?.text_color
                      }))}
                    />
                  </td>
                  {testMode && <td className="mode is-vcentered">
                    <span className="tag is-warning is-centered">Test</span>
                  </td>}
                  <td className="details">
                    <ConnectionDescription connection={connection} />
                  </td>
                  <td className="action has-text-right is-vcentered">
                    <button className="button is-white is-large" onClick={toggle(connection)}>
                      <span className={`icon is-medium ${connection.enabled ? 'has-text-success' : 'has-text-grey'}`}>
                        <i className={`fas fa-${connection.enabled ? 'toggle-on' : 'toggle-off'} fa-lg`}></i>
                      </span>
                    </button>
                  </td>
                </tr>

              ))}
            </tbody>

          </table>
        </div>
      </>}

      {((query.data?.system_connections || []).length == 0) && <div className="card my-6">

        <div className="card-content has-text-centered">
          <p>The administrators have not provided any system wide carrier connections.</p>
        </div>

      </div>}

    </>
  );
};
