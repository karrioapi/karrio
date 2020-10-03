import React, { Fragment } from 'react';
import { View } from '@/library/types';
import { CarrierSettings } from '@purplship/purplship/dist';

interface ProvidersView extends View {
  carriers: CarrierSettings[];
}

const Providers: React.FC<ProvidersView> = ({ carriers }) => {
  return (
    <Fragment>

      <header className="px-2 pt-1 pb-6">
        <span className="subtitle is-4">Carrier Accounts</span>
        <button className="button is-success is-pulled-right">Add Carrier Account</button>
      </header>

      <div className="table-container">
        <table className="table is-fullwidth">

          <tbody className="providers-table">

            {carriers.map((settings) => (

              <tr id={settings.id}>
                <td className="carrier"><div className="box">{settings.carrierName}</div></td>
                <td className="mode is-vcentered">
                  {settings.test ? <span className="tag is-primary is-centered">Test</span> : <></>}
                </td>
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

            ))}

          </tbody>

        </table>
      </div>

    </Fragment>
  );
}

export default Providers;