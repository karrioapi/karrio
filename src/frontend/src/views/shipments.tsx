import React, { Fragment } from 'react';
import { View } from '@/library/Types';

const Shipments: React.FC<View> = () => {
  return (
    <Fragment>

      <header className="px-2 pt-1 pb-6">
        <h4 className="subtitle is-4">Shipments</h4>
      </header>

      <div className="table-container">
        <table className="table is-fullwidth is-hoverable">

          <thead className="shipments-table">
            <th className="carrier">Carriers</th>
            <th className="mode">Mode</th>
            <th className="recipient">Recipient</th>
            <th className="creation">Created</th>
            <th className="status">Status</th>
          </thead>

          <tbody>
            <tr>
              <td>UPS</td>
              <td><span className="tag is-primary">Test</span></td>
              <td>Jane Doe, Vancouver, BC, Canada</td>
              <td>2020/09/20</td>
              <td><span className="tag is-info is-light">In-Transit</span></td>
            </tr>
            <tr>
              <td>FedEx</td>
              <td></td>
              <td>John Doe, Moncton, NB, Canada</td>
              <td>2020/09/20</td>
              <td><span className="tag is-success is-light">Delivered</span></td>
            </tr>
          </tbody>

        </table>
      </div>

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