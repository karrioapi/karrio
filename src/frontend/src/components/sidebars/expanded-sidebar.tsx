import React from 'react';
import NavLink from '@/components/navlink';
import { UserInfo } from '@/library/api';

interface ExpandedSidebarComponent {
    user: UserInfo;
}

const ExpandedSidebar: React.FC<ExpandedSidebarComponent> = ({ user }) => {
    return (
        <div className="plex-sidebar">
            <div className="sidebar-header">
                <img src="/static/purpleserver/img/logo.svg" alt="Purplship" width="80" />
                <button className="menu-icon v-5 is-open mobile-item is-block mobile-sidebar-trigger">
                    <span></span>
                </button>
            </div>
            <div className="sidebar-profile">
                <div className="avatar-container">
                    <div className="avatar-wrapper">
                        <div className="avatar">
                            <img src="/static/purpleserver/client/profile.svg" alt="" />
                        </div>
                        <h3>{user.full_name}</h3>
                        <p>{user.email}</p>
                    </div>
                </div>
            </div>
            <div className="sidebar-menu has-slimscroll pb-6">
                <NavLink to="/">
                    <span>Shipments</span>
                </NavLink>
                <NavLink to="carrier_connections">
                    <span>Carrier Connections</span>
                </NavLink>
                <a className="menu-item" target="_blank" href="/api">
                    <span>API Reference</span>
                    <i className="fas fa-external-link-alt has-text-primary px-1 mx-1"></i>
                </a>

                <div className="menu-item menu-label my-0">
                    <span>Developers</span>
                </div>

                <NavLink className="menu-item ml-6" to="api_logs">
                    <span>Logs</span>
                </NavLink>

                <NavLink className="menu-item bottom-menu-item" to="settings">
                    <i className="fas fa-cog"></i>
                    <span>Settings</span>
                </NavLink>
            </div>
        </div>
    );
}

export default ExpandedSidebar;
