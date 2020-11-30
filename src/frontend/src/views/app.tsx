import React, { Fragment } from 'react';
import { References } from '@purplship/purplship';
import { Router } from "@reach/router";
import Shipments from '@/views/shipments';
import Connections from '@/views/connections';
import Settings from '@/views/settings';
import APILogs from '@/views/api_logs';
import ExpandedSidebar from '@/components/sidebars/expanded-sidebar';
import LabelCreator from '@/components/label/label-creator';
import BoardFooter from '@/components/footer/board-footer';
import Navbar from '@/components/navbar/navbar';
import Notifier from '@/components/notifier';
import { PaginatedLogs, state, UserInfo, } from '@/library/api';
import { Logs, Reference, User } from '@/library/context';
import 'prismjs';
import 'prismjs/components/prism-json';
import 'prismjs/themes/prism.css';
import 'prismjs/themes/prism-solarizedlight.css';
import '@/assets/app.scss';

const App: React.FC = () => {
    const user = state.user;
    const token = state.token;
    const references = state.references;
    const shipments = state.shipments;
    const connections = state.connections;
    const logs = state.logs;
    const labelData = state.labelData;

    return (
        <Fragment>
            <Reference.Provider value={references as References}>
            <Logs.Provider value={logs as PaginatedLogs}>
            <User.Provider value={user as UserInfo}>
                <ExpandedSidebar />

                <div className="plex-wrapper">
                    <div className="wrapper-inner">
                        <Notifier />
                        <Navbar user={user} />

                        <div className="dashboard-content">
                            <Router>
                                <Shipments shipments={shipments} path="/" />
                                <Connections connections={connections} path="carrier_connections" />
                                <Settings token={token} user={user} path="settings" />
                                <APILogs path="api_logs/*" logs={logs}/>
                                <LabelCreator data={labelData} path="buy_label/:id" />
                            </Router>
                        </div>

                    </div>
                </div>

                <BoardFooter />
            </User.Provider>
            </Logs.Provider>
            </Reference.Provider>
        </Fragment>
    );
};

export default App;