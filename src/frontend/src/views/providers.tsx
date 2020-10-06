import React, { Fragment } from 'react';
import { View } from '@/library/types';
import { Provider } from '@/library/api';
import ConnectProviderModal from '@/components/connect-provider-modal';
import { Reference } from '@/library/context';

interface ProvidersView extends View {
  providers: Provider[];
}

const Providers: React.FC<ProvidersView> = ({ providers }) => {
  return (
    <Fragment>

      <header className="px-2 pt-1 pb-6">
        <span className="subtitle is-4">Carrier Connections</span>
        <ConnectProviderModal className="button is-success is-pulled-right">
          <span>Connect a Carrier</span>
        </ConnectProviderModal>
      </header>

      <div className="table-container">
        <table className="table is-fullwidth">

          <tbody className="providers-table">
            <Reference.Consumer>
            {ref => (Object.values(ref).length > 0) && providers.map((settings) => (

              <tr key={settings.id}>
                <td className="carrier"><div className="box">{ref.carriers[settings.carrierName]}</div></td>
                <td className="mode is-vcentered">
                  {settings.test ? <span className="tag is-primary is-centered">Test</span> : <></>}
                </td>
                <td className="details"></td>
                <td className="action is-vcentered">
                  <div className="buttons is-centered">
                    <ConnectProviderModal className="button" provider={settings}>
                      <span className="icon is-small">
                        <i className="fas fa-pen"></i>
                      </span>
                    </ConnectProviderModal>
                    <button className="button">
                      <span className="icon is-small">
                        <i className="fas fa-trash"></i>
                      </span>
                    </button>
                  </div>
                </td>
              </tr>

            ))}
            </Reference.Consumer>
          </tbody>

        </table>
      </div>

    </Fragment>
  );
}

export default Providers;