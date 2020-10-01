import React from 'react';
import NavLink from '@/components/navlink';


const ExpandedSidebar: React.FC = () => {
    return (
        <div className="plex-sidebar">
            <div className="sidebar-header">
                <img src="/static/purpleserver/img/logo.svg" alt="Purplship" width="80" />
                <button className="menu-icon v-5 is-open mobile-item is-block mobile-sidebar-trigger">
                    <span></span>
                </button>
            </div>
            <div className="py-4"></div>
            <div className="sidebar-menu has-slimscroll">
                <NavLink to="/">
                    <span>Shipments</span>
                </NavLink>
                <NavLink to="providers">
                    <span>Carrier Accounts</span>
                </NavLink>
                <NavLink to="settings">
                    <span>Settings</span>
                </NavLink>

                <div className="naver"></div>
            </div>
        </div>
    );
}

export default ExpandedSidebar;
