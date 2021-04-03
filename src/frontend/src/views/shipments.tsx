import React, { useContext, useEffect } from 'react';
import { View } from '@/library/types';
import ShipmentMenu from '@/components/shipment-menu';
import { useNavigate } from '@reach/router';
import { formatAddress, formatDate, isNone } from '@/library/helper';
import CarrierBadge from '@/components/carrier-badge';
import ShipmentMutation from '@/components/data/shipment-mutation';
import { Shipments } from '@/components/data/shipments-query';
import { Loading } from '@/components/loader';
import { Notify } from '@/components/notifier';


interface ShipmentsView extends View { }

const ShipmentPage: React.FC<ShipmentsView> = ShipmentMutation<ShipmentsView>(() => {
  const navigate = useNavigate();
  const { setLoading } = useContext(Loading);
  const { loading, results, load, loadMore, previous, next } = useContext(Shipments);

  const createLabel = (_: React.MouseEvent) => navigate('buy_label/new');

  useEffect(() => { !loading && load(); }, []);
  useEffect(() => { setLoading(loading); });

  const { notify } = useContext(Notify);
  (window as any).noti = () => notify({ message: 'Tracker successfully added!' })

  return (
    <>

      <header className="px-2 pt-1 pb-6">
        <span className="subtitle is-4">Shipments</span>
        <a className="button is-success is-pulled-right" onClick={createLabel}>
          <span>Create Label</span>
        </a>
      </header>

      <div className="table-container">
        <table className="table is-fullwidth">

          <thead className="shipments-table">
            <tr>
              <th className="carrier has-text-centered">Carriers</th>
              <th className="mode">Mode</th>
              <th className="recipient">Recipient</th>
              <th className="creation has-text-centered">Created</th>
              <th className="status has-text-centered">Status</th>
              <th className="action"></th>
            </tr>
          </thead>

          <tbody>

            {results.map(shipment => (
              <tr key={shipment.id}>
                <td className="is-vcentered">
                  <CarrierBadge carrier={shipment.carrier_name as string} className="tag" style={{ width: '100%', minWidth: '120px' }} />
                </td>
                <td className="mode is-vcentered">
                  {shipment.test_mode ? <span className="tag is-warning is-centered">Test</span> : <></>}
                </td>
                <td className="is-vcentered">
                  <p className="is-subtitle is-size-6 my-1 has-text-weight-semibold has-text-grey">{formatAddress(shipment.recipient)}</p>
                </td>
                <td className="is-vcentered has-text-centered">{formatDate(shipment.created_at)}</td>
                <td className="is-vcentered">
                  <span className="tag is-info is-light" style={{ width: '100%' }}>{shipment.status?.toString().toUpperCase()}</span>
                </td>
                <td className="is-vcentered">
                  <ShipmentMenu shipment={shipment} style={{ width: '100%' }} />
                </td>
              </tr>
            ))}

          </tbody>

        </table>
      </div>

      {(!loading && results.length == 0) && <div className="card my-6">

        <div className="card-content has-text-centered">
          <p>No shipment has been created yet.</p>
          <p>Use the <strong>API</strong> to create your first shipment.</p>
        </div>

      </div>}

      <footer className="px-2 py-2 is-vcentered">
        <div className="buttons has-addons is-centered">
          <button className="button is-small" onClick={() => loadMore(previous)} disabled={isNone(previous)}>
            <span>Previous</span>
          </button>
          <button className="button is-small" onClick={() => loadMore(next)} disabled={isNone(next)}>
            <span>Next</span>
          </button>
        </div>
      </footer>

    </>
  );
});

export default ShipmentPage;