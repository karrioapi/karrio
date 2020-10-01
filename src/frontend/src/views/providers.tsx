import React, { Fragment } from 'react';
import { View } from '@/library/Types';

const Providers: React.FC<View> = () => {
  return (
    <Fragment>

      <header className="px-2 pt-1 pb-6">
        <span className="subtitle is-4">Carrier Accounts</span>
        <button className="button is-success is-pulled-right">Add Carrier Account</button>
      </header>

      <div className="table-container">
        <table className="table is-fullwidth">

          <tbody className="providers-table">
            <tr>
              <td className="carrier">
                <div className="box">UPS</div>
              </td>
              <td className="mode is-vcentered"><span className="tag is-primary is-centered">Test</span></td>
              <td className="details"></td>
              <td className="action is-vcentered">
                <p className="buttons is-centered">
                  <button className="button">
                    <span className="icon is-small">
                      <i className="fas fa-pen"></i>
                    </span>
                  </button>
                  <button className="button">
                    <span className="icon is-small">
                      <i className="fas fa-trash"></i>
                    </span>
                  </button>
                </p>
              </td>
            </tr>
            <tr>
              <td className="carrier"><div className="box">FedEx</div></td>
              <td></td>
              <td className="details"></td>
              <td className="action is-vcentered">
                <p className="buttons is-centered">
                  <button className="button">
                    <span className="icon is-small">
                      <i className="fas fa-pen"></i>
                    </span>
                  </button>
                  <button className="button">
                    <span className="icon is-small">
                      <i className="fas fa-trash"></i>
                    </span>
                  </button>
                </p>
              </td>
            </tr>
          </tbody>

        </table>
      </div>

    </Fragment>
  );
}

export default Providers;