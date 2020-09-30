import React, { Fragment } from 'react';
import { Router } from "@reach/router";
import Home from '@/views/home';
import ExpandedSidebar from '@/components/sidebars/expanded-sidebar';
import Navbar from '@/components/navbar/navbar';
import '@/assets/css/App.scss';
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
                            <Home path="/" />
                        </Router>
                    </div>

                </div>
            </div>
        </Fragment>
    );
}

export default App;