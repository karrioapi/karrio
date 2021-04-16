import React, { Fragment, useContext, useEffect, useState } from 'react';
import CarrierBadge from '@/components/carrier-badge';
import { state } from '@/library/api';
import { SystemConnections } from '@/library/context';

interface SystemConnectionListView { }

const SystemConnectionList: React.FC<SystemConnectionListView> = () => {
  const connections = useContext(SystemConnections);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    if (loading === false) {
      setLoading(true);
      state.fetchSystemConnections().catch(_ => _).then(() => setLoading(false));
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
          {(connections?.results || []).map((connection) => (

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

      {((connections.results || []).length == 0) && <div className="card my-6">

        <div className="card-content has-text-centered">
          <p>The administrators have not provided any system wide carrier connections.</p>
        </div>

      </div>}

    </Fragment>
  );
}

export default SystemConnectionList;