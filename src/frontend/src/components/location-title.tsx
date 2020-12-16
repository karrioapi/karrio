import { Location } from '@reach/router';
import React from 'react';

interface LocationTitleComponent { }

const LocationTitle: React.FC<LocationTitleComponent> = () => {
    return (
        <Location>
            {({location}) => {
                let title = '';

                if (location.pathname.includes('/carrier_connections')) {
                    title = '| Carrier Connections';
                } else if (location.pathname.includes('/api_logs')) {
                    title = '| API Logs';
                } else if (location.pathname.includes('/buy_label/')) {
                    title = '| Buy Label';
                } else if(location.pathname === '/settings') {
                    title = '| User Settings';
                } else if(location.pathname === '/') {
                    title = '| Shipments';
                }

                document.title = `Purplship ${title}`;
                return <></>;
            }}
        </Location>
    );
};

export default LocationTitle;
