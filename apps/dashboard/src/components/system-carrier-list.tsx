import { useSystemConnectionMutation, useSystemConnections } from '@/context/system-connection';
import ConnectionDescription from '@/components/descriptions/connection-description';
import CarrierNameBadge from '@/components/carrier-name-badge';
import { Notify } from '@/components/notifier';
import { NotificationType } from '@/lib/types';
import React, { useContext } from 'react';


const SystemConnectionList: React.FC = () => {
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

      {((query.data?.system_connections || []).length > 0) && <table className="table is-fullwidth">

        <tbody className="system-connections-table">
          <tr>
            <td className="is-size-7" colSpan={4}>ACCOUNTS</td>
          </tr>

          {(query.data?.system_connections || []).map((connection) => (

            <tr key={`connection-${connection.id}-${Date.now()}`}>
              <td className="carrier is-vcentered pl-0">
                <CarrierNameBadge
                  carrier_name={connection.carrier_name}
                  display_name={connection.display_name}
                  className="box has-text-weight-bold"
                />
              </td>
              <td className="mode is-vcentered">
                {connection.test_mode ? <span className="tag is-warning is-centered">Test</span> : <></>}
              </td>
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

      </table>}

      {((query.data?.system_connections || []).length == 0) && <div className="card my-6">

        <div className="card-content has-text-centered">
          <p>The administrators have not provided any system wide carrier connections.</p>
        </div>

      </div>}

    </>
  );
};

export default SystemConnectionList;
