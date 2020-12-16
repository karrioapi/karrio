import React, { useEffect, useState } from 'react';
import { View } from '@/library/types';
import { PaginatedShipments, state } from '@/library/api';
import ShipmentMenu from '@/components/shipment-menu';
import { useNavigate } from '@reach/router';
import { formatAddress, formatDate } from '@/library/helper';
import CarrierBadge from '@/components/carrier-badge';


interface ShipmentsView extends View {
  shipments?: PaginatedShipments;
}

const Shipments: React.FC<ShipmentsView> = ({ shipments }) => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState<boolean>(false);
  const update = (url?: string | null) => async (_: React.MouseEvent) => {
    await state.fetchShipments(url as string);
  };
  const createLabel = (_: React.MouseEvent) => {
    navigate('buy_label/new');
    state.setLabelData();
  };
  useEffect(() => {
    if ((shipments === undefined || shipments?.fetched === false) && loading === false) {
      setLoading(true);
      state.fetchShipments().catch(_ => _).then(() => setLoading(false));
    }
  }, shipments?.results);

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

            {shipments?.results.map(shipment => (
              <tr key={shipment.id}>
                <td className="is-vcentered">
                  <CarrierBadge name={shipment.carrier_name as string} className="tag" style={{ width: '100%', minWidth: '120px' }} />
                </td>
                <td className="mode is-vcentered">
                  {shipment.test_mode ? <span className="tag is-warning is-centered">Test</span> : <></>}
                </td>
                <td className="is-vcentered">{formatAddress(shipment.recipient)}</td>
                <td className="is-vcentered">{formatDate(shipment.created_at)}</td>
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

      {(!loading && shipments?.count == 0) && <div className="card my-6">

        <div className="card-content has-text-centered">
          <p>No shipment has been created yet.</p>
          <p>Use the <strong>API</strong> to create your first shipment.</p>
        </div>

      </div>}

      {loading && <div className="card my-6">

        <div className="card-content has-text-centered">
          <span className="icon has-text-info is-large">
            <i className="fas fa-spinner fa-pulse"></i>
          </span>
        </div>

      </div>}

      <footer className="px-2 py-2 is-vcentered">
        <div className="buttons has-addons is-centered">
          <button className="button is-small" onClick={update(shipments?.previous)} disabled={shipments?.previous === null}>
            <span>Previous</span>
          </button>
          <button className="button is-small" onClick={update(shipments?.next)} disabled={shipments?.next === null}>
            <span>Next</span>
          </button>
        </div>
      </footer>

    </>
  );
};

export default Shipments;