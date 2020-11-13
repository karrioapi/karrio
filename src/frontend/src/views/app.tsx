import React, { Fragment } from 'react';
import { Router } from "@reach/router";
import Shipments from '@/views/shipments';
import Connections from '@/views/connections';
import Settings from '@/views/settings';
import APILogs from '@/views/api_logs';
import ExpandedSidebar from '@/components/sidebars/expanded-sidebar';
import BoardFooter from '@/components/footer/board-footer';
import Navbar from '@/components/navbar/navbar';
import Notifier from '@/components/notifier';
import { PaginatedLogs, state, } from '@/library/api';
import { Logs, Reference } from '@/library/context';
import '@/assets/scss/main.scss';
import '@/assets/custom.scss';
import 'prismjs';
import 'prismjs/components/prism-json';
import 'prismjs/themes/prism.css';
import 'prismjs/themes/prism-solarizedlight.css';
import { References } from '@purplship/purplship';

const App: React.FC = () => {
    const user = state.user;
    const token = state.token;
    const references = state.references;
    const shipments = state.shipments;
    const connections = state.connections;
    const logs = state.logs;

    return (
        <Fragment>
            <Reference.Provider value={references as References}>
            <Logs.Provider value={logs as PaginatedLogs}>
                <ExpandedSidebar user={user} />

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
                            </Router>
                        </div>

                    </div>
                </div>

                <BoardFooter />
            </Logs.Provider>
            </Reference.Provider>
        </Fragment>
    );
};

export default App;