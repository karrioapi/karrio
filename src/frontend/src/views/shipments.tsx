import React, { Fragment } from 'react';
import { View } from '@/library/types';
import { Address, Shipment } from '@purplship/purplship/dist';
import { Provider } from '@/library/api';


function formatAddress(address: Address): string {
  return [
    address.personName,
    address.city,
    address.stateCode,
    address.countryCode
  ].filter(a => a !== null && a !== "").join(', ');
}

interface ShipmentsView extends View {
  shipments: Shipment[];
  providers: Provider[];
}

const Shipments: React.FC<ShipmentsView> = ({ shipments, providers }) => {
  const isTest = (carrierId?: string) => {
    return providers.reduce((carrier: Provider, shipmentCarrier: Provider) => {
      return carrier.carrierId === carrierId ? carrier : shipmentCarrier;
    }, {} as Provider).test;
  };

  return (
    <Fragment>

      <header className="px-2 pt-1 pb-6">
        <h4 className="subtitle is-4">Shipments</h4>
      </header>

      <div className="table-container">
        <table className="table is-fullwidth is-hoverable">

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

            {shipments.map(shipment => (
              <tr key={shipment.id}>
                <td>{shipment.carrierName}</td>
                <td className="mode is-vcentered">
                  {isTest(shipment.carrierId) ? <span className="tag is-primary is-centered">Test</span> : <></>}
                </td>
                <td>{formatAddress(shipment.recipient)}</td>
                <td></td>
                <td><span className="tag is-info is-light">{shipment.status}</span></td>
              </tr>
            ))}

          </tbody>

        </table>
      </div>

      {(shipments.length == 0) && <div className="card my-6">

        <div className="card-content has-text-centered">
          <p>No shipment has been created yet.</p>
          <p>Use the use the <strong>API</strong> to create your first shipment.</p>
        </div>

      </div>}

      <footer className="px-2 py-2 is-vcentered">
        <div className="buttons has-addons is-centered">
          <button className="button">
            <i className="fas fa-chevron-left"></i>
          </button>
          <button className="button">1</button>
          <button className="button">
            <i className="fas fa-chevron-right"></i>
          </button>
        </div>
      </footer>

    </Fragment>
  );
};

export default Shipments;