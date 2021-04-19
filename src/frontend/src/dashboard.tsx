import React from 'react';
import ReactDOM from 'react-dom';
import { graphClient } from '@/library/graphql';
import { ApolloProvider } from '@apollo/client';
import { Router } from "@reach/router";
import ShipmentPage from '@/views/shipments';
import TrackersPage from '@/views/trackers';
import ConnectionsPage from '@/views/connections';
import AddressesPage from '@/views/addresses';
import ParcelsPage from '@/views/parcels';
import APILogPage from '@/views/api-logs';
import Account from '@/views/account';
import APISettings from '@/views/api-settings';
import WebhooksPage from '@/views/webhooks';
import CustomsInfoPage from '@/views/customs-infos';
import UserQuery from '@/components/data/user-query';
import TokenQuery from '@/components/data/token-query';
import APIReferenceQuery from '@/components/data/references-query';
import ParcelTemplatesQuery from '@/components/data/parcel-templates-query';
import AddressTemplatesQuery from '@/components/data/address-templates-query';
import CustomInfoTemplatesQuery from '@/components/data/customs-templates-query';
import TemplatesQuery from '@/components/data/default-templates-query';
import ShipmentsQuery from '@/components/data/shipments-query';
import TrackersQuery from '@/components/data/trackers-query';
import UserConnectionsQuery from '@/components/data/user-connections-query';
import SystemConnectionsQuery from '@/components/data/system-connections-query';
import LabelDataQuery from '@/components/data/shipment-query';
import ExpandedSidebar from '@/components/sidebars/expanded-sidebar';
import LabelCreator from '@/components/label/label-creator';
import Navbar from '@/components/navbar/navbar';
import Loader from '@/components/loader';
import Notifier from '@/components/notifier';
import LocationTitle from '@/components/location-title';
import '@/library/rest';
import 'prismjs';
import 'prismjs/components/prism-json';
import 'prismjs/themes/prism.css';
import 'prismjs/themes/prism-solarizedlight.css';
import '@/style/dashboard.scss';


const DATA_CONTEXTS = [
    UserQuery,
    TokenQuery,
    AddressTemplatesQuery,
    CustomInfoTemplatesQuery,
    ParcelTemplatesQuery,
    APIReferenceQuery,
    ShipmentsQuery,
    LabelDataQuery,
    TrackersQuery,
    UserConnectionsQuery,
    SystemConnectionsQuery,
    TemplatesQuery,
    Loader,
    Notifier,
];


const DashboardContexts: React.FC = ({ children }) => {
    const NestedContexts = DATA_CONTEXTS.reduce((_, Ctx) => <Ctx>{_}</Ctx>, children);

    return (
        <>
            <ApolloProvider client={graphClient}>{NestedContexts}</ApolloProvider>
        </>
    );
}

const Dashboard: React.FC = () => {
    return (
        <DashboardContexts>
            <LocationTitle />
            <ExpandedSidebar />

            <div className="plex-wrapper">
                <div className="wrapper-inner">
                    <Notifier />
                    <Navbar />

                    <div className="dashboard-content">
                        <Router>
                            <ShipmentPage path="/" />
                            <TrackersPage path="/trackers" />

                            <AddressesPage path="configurations/addresses" />
                            <ConnectionsPage path="configurations/carriers" />
                            <ParcelsPage path="configurations/parcels" />
                            <CustomsInfoPage path="configurations/customs_infos" />

                            <Account path="settings/account" />
                            <APILogPage path="api_logs/*" />
                            <APISettings path="settings/api" />
                            <WebhooksPage path="settings/webhooks" />
                            <LabelCreator path="buy_label/:id" />
                        </Router>
                    </div>

                </div>
            </div>

        </DashboardContexts>
    );
};

ReactDOM.render(
    <React.StrictMode>
        <Dashboard />
    </React.StrictMode>,
    document.getElementById('root')
);