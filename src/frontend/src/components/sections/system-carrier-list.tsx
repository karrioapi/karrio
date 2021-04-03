import React, { Fragment, useContext, useEffect } from 'react';
import CarrierBadge from '@/components/carrier-badge';
import { SystemConnections } from '@/components/data/system-connections-query';
import { Loading } from '@/components/loader';

interface SystemConnectionListView { }

const SystemConnectionList: React.FC<SystemConnectionListView> = () => {
  const { setLoading } = useContext(Loading);
  const { system_connections, loading, load } = useContext(SystemConnections);

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
          {(system_connections || []).map((connection) => (

            <tr key={connection.id}>
              <td className="carrier">
                <CarrierBadge carrier={connection.carrier_name} className="box has-text-weight-bold" />
              </td>
              <td className="mode is-vcentered">
                {connection.test ? <span className="tag is-warning is-centered">Test</span> : <></>}
              </td>
              <td className="details">
                <div className="content is-small">
                  <ul>
                    <li>carrier id: <span className="tag is-info is-light" title="carrier nickname">{connection.carrier_id}</span></li>
                  </ul>
                </div>
              </td>
            </tr>

          ))}
        </tbody>

      </table>

      {((system_connections).length == 0) && <div className="card my-6">

        <div className="card-content has-text-centered">
          <p>The administrators have not provided any system wide carrier connections.</p>
        </div>

      </div>}

    </Fragment>
  );
}

export default SystemConnectionList;