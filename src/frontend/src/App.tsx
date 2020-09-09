import React, { Fragment } from 'react';
import { Router } from "@reach/router";
import NavBar from '@/NavBar';
import Settings from '@/Views/Settings';
import Dashboard from '@/Views/Dashboard';
import Shipments from '@/Views/Shipments';
import '@/css/App.css';

const App: React.FC = () => {
    return (
        <Fragment>
            <NavBar />
            <Router>
                <Shipments path="/" />
                <Dashboard path="dashboard" />
                <Settings path="settings" />
            </Router>
        </Fragment>
    );
}

export default App;