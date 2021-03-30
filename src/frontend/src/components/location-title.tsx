import { Reference } from '@/library/context';
import { Location } from '@reach/router';
import React, { useContext } from 'react';

interface LocationTitleComponent { }

const LocationTitle: React.FC<LocationTitleComponent> = () => {
    const References = useContext(Reference);
    
    return (
        <Location>
            {({location}) => {
                let title = '';

                if (location.pathname.includes('/api_logs')) {
                    title = '| API Logs';
                } else if (location.pathname.includes('/buy_label/')) {
                    title = '| Buy Label';
                } else if(location.pathname === '/configurations/parcels') {
                    title = '| Parcels';
                } else if(location.pathname === '/configurations/addresses') {
                    title = '| Addresses';
                } else if(location.pathname === '/configurations/carriers') {
                    title = '| Carrier Connections';
                } else if(location.pathname === '/configurations/customs_infos') {
                    title = '| Customs Info';
                } else if(location.pathname === '/settings/account') {
                    title = '| User Account';
                } else if(location.pathname === '/settings/api') {
                    title = '| API Key';
                }  else if(location.pathname === '/trackers') {
                    title = '| Shipment Trackers';
                } else if(location.pathname === '/') {
                    title = '| Shipments';
                }

                document.title = `${References?.APP_NAME} ${title}`;
                return <></>;
            }}
        </Location>
    );
};

export default LocationTitle;
