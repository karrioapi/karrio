import React, { Fragment } from 'react';
import { Router } from "@reach/router";
import Shipments from '@/views/shipments';
import Providers from '@/views/providers';
import Settings from '@/views/settings';
import ExpandedSidebar from '@/components/sidebars/expanded-sidebar';
import BoardFooter from '@/components/footer/board-footer';
import Navbar from '@/components/navbar/navbar';
import { References, Shipment } from '@purplship/purplship';
import { state, UserInfo, Provider } from '@/library/api';
import { Reference } from '@/library/context';
import '@/assets/scss/main.scss';
import '@/assets/custom.scss';

const App: React.FC = () => {
    const user: UserInfo = state.user;
    const token: string = state.token;
    const shipments: Shipment[] = state.shipments;
    const providers: Provider[] = state.providers;
    const references: References = state.references;

    return (
        <Fragment>
            <Reference.Provider value={references}>
                <ExpandedSidebar user={user} />

                <div className="plex-wrapper">
                    <div className="wrapper-inner">
                        <Navbar user={user} />

                        <div className="dashboard-content">
                            <Router>
                                <Shipments shipments={shipments} providers={providers} path="/" />
                                <Providers providers={providers} path="carrier_connections" />
                                <Settings token={token} user={user} path="settings" />
                            </Router>
                        </div>

                    </div>
                </div>

                <BoardFooter />
            </Reference.Provider>
        </Fragment>
    );
}

export default App;