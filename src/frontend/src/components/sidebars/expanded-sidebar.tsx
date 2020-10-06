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
                            <span className="badge">
                                <i className="fas fa-check"></i>
                            </span>
                        </div>
                        <h3>{user.firstName}</h3>
                        <p>{user.username}</p>
                    </div>
                </div>
            </div>
            <div className="sidebar-menu has-slimscroll">
                <NavLink to="/">
                    <span>Shipments</span>
                </NavLink>
                <NavLink to="carrier_connections">
                    <span>Carrier Connections</span>
                </NavLink>
                <NavLink to="settings">
                    <span>Settings</span>
                </NavLink>
                <a className="menu-item" target="_blank" href="/api">
                    <span>API Reference</span>
                    <i className="fas fa-external-link-alt px-1"></i>
                </a>

                <div className="naver"></div>
            </div>
        </div>
    );
}

export default ExpandedSidebar;
