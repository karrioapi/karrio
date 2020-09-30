import React, { Fragment } from 'react';
import { Router } from "@reach/router";
import Shipments from '@/views/shipments';
import Providers from '@/views/providers';
import Settings from '@/views/settings';
import Profile from '@/views/profile';
import ExpandedSidebar from '@/components/sidebars/expanded-sidebar';
import Navbar from '@/components/navbar/navbar';
import '@/assets/scss/main.scss';

const App: React.FC = () => {
    return (
        <Fragment>
            <ExpandedSidebar />

            <div className="plex-wrapper">
                <div className="wrapper-inner">
                    <Navbar />

                    <div className="dashboard-content">
                        <Router>
                            <Shipments path="/" />
                            <Providers path="providers" />
                            <Settings path="settings" />
                            <Profile path="profile" />
                        </Router>
                    </div>

                </div>
            </div>
        </Fragment>
    );
}

export default App;