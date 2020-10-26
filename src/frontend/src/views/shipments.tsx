import React, { Fragment, useEffect } from 'react';
import { View } from '@/library/types';
import { Address } from '@purplship/purplship';
import { PaginatedShipments, state } from '@/library/api';


interface ShipmentsView extends View {
  shipments?: PaginatedShipments;
}

const Shipments: React.FC<ShipmentsView> = ({ shipments }) => {
  useEffect(() => { if(shipments === undefined ) state.fetchShipments(); }, []);
  const update = (url?: string | null) => async (_: React.MouseEvent) => {
      await state.fetchShipments(url as string);
  };

  return (
    <Fragment>

      <header className="px-2 pt-1 pb-6">
        <h4 className="subtitle is-4">Shipments</h4>
      </header>

      <div className="table-container">
        <table className="table is-fullwidth">

          <thead className="shipments-table">
            <tr>
              <th className="carrier">Carriers</th>
              <th className="mode">Mode</th>
              <th className="recipient">Recipient</th>
              <th className="creation">Created</th>
              <th className="status">Status</th>
            </tr>
          </thead>

          <tbody>

            {shipments?.results.map(shipment => (
              <tr key={shipment.id}>
                <td><span className="tag is-primary is-light">{shipment.carrier_name || "Not Selected"}</span></td>
                <td className="mode is-vcentered">
                  {shipment.test_mode ? <span className="tag is-warning is-centered">Test</span> : <></>}
                </td>
                <td>{formatAddress(shipment.recipient)}</td>
                <td>{formatDate(shipment.created_at)}</td>
                <td><span className="tag is-info is-light">{shipment.status?.toString().toUpperCase()}</span></td>
              </tr>
            ))}

          </tbody>

        </table>
      </div>

      {(shipments?.count == 0) && <div className="card my-6">

        <div className="card-content has-text-centered">
          <p>No shipment has been created yet.</p>
          <p>Use the <strong>API</strong> to create your first shipment.</p>
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

    </Fragment>
  );
};

function formatAddress(address: Address): string {
  return [
    address.person_name,
    address.city,
    address.postal_code,
    address.country_code
  ].filter(a => a !== null && a !== "").join(', ');
}

function formatDate(date: string): string {
  let [month, day, year] = (new Date(date)).toLocaleDateString().split("/");
  return `${day}/${month}/${year}`;
}

export default Shipments;