import React, { Fragment } from 'react';
import { References } from '@/api';
import { Router } from "@reach/router";
import Shipments from '@/views/shipments';
import Trackers from '@/views/trackers';
import Connections from '@/views/connections';
import Addresses from '@/views/addresses';
import Parcels from '@/views/parcels';
import APILogs from '@/views/api-logs';
import Account from '@/views/account';
import APISettings from '@/views/api-settings';
import CustomsInfos from '@/views/customs-infos';
import ExpandedSidebar from '@/components/sidebars/expanded-sidebar';
import LabelCreator from '@/components/label/label-creator';
import BoardFooter from '@/components/footer/board-footer';
import Navbar from '@/components/navbar/navbar';
import Notifier from '@/components/notifier';
import LocationTitle from '@/components/location-title';
import { state } from '@/library/app';
import { DefaultTemplates, PaginatedLogs, PaginatedTemplates, UserInfo } from '@/library/types';
import { Templates, Logs, Reference, User, ParcelTemplates, AddressTemplates, UserConnections, SystemConnections } from '@/library/context';
import 'prismjs';
import 'prismjs/components/prism-json';
import 'prismjs/themes/prism.css';
import 'prismjs/themes/prism-solarizedlight.css';
import '@/theme/purpleserver.scss';
import ReactDOM from 'react-dom';

const Dashboard: React.FC = () => {
    const user = state.user;
    const token = state.token;
    const references = state.references;
    const defatultTemplates = state.defaultTemplates;
    const parcelTemplates = state.parcels;
    const addressTemplates = state.addresses;

    const logs = state.logs;
    const labelData = state.labelData;
    const shipments = state.shipments;
    const trackers = state.trackers;
    const systemConnections = state.systemConnections;
    const userConnections = state.userConnections;
    const customsInfos = state.customsInfos;

    return (
        <Fragment>
            <Reference.Provider value={references as References}>
                <Logs.Provider value={logs as PaginatedLogs}>
                    <User.Provider value={user as UserInfo}>
                        <ParcelTemplates.Provider value={parcelTemplates as PaginatedTemplates}>
                            <AddressTemplates.Provider value={addressTemplates as PaginatedTemplates}>
                                <Templates.Provider value={defatultTemplates as DefaultTemplates}>
                                    <UserConnections.Provider value={userConnections}>
                                        <SystemConnections.Provider value={systemConnections}>

                                            <ExpandedSidebar />

                                            <div className="plex-wrapper">
                                                <div className="wrapper-inner">
                                                    <Notifier />
                                                    <Navbar user={user} />

                                                    <div className="dashboard-content">
                                                        <Router>
                                                            <Shipments path="/" shipments={shipments} />
                                                            <Trackers path="/trackers" trackers={trackers} />
                                                            <LabelCreator path="buy_label/:id" data={labelData} />

                                                            <Connections path="configurations/carriers" />
                                                            <Parcels path="configurations/parcels" templates={parcelTemplates} />
                                                            <Addresses path="configurations/addresses" templates={addressTemplates} />
                                                            <CustomsInfos path="configurations/customs_infos" templates={customsInfos} />

                                                            <APILogs path="api_logs/*" logs={logs} />
                                                            <APISettings path="settings/api" token={token} />
                                                            <Account path="settings/account" user={user} />
                                                        </Router>
                                                    </div>

                                                </div>
                                            </div>

                                            <BoardFooter />

                                        </SystemConnections.Provider>
                                    </UserConnections.Provider>
                                </Templates.Provider>
                            </AddressTemplates.Provider>
                        </ParcelTemplates.Provider>
                    </User.Provider>
                </Logs.Provider>
            </Reference.Provider>
            <LocationTitle />
        </Fragment>
    );
};

ReactDOM.render(
    <React.StrictMode>
        <Dashboard />
    </React.StrictMode>,
    document.getElementById('root')
);