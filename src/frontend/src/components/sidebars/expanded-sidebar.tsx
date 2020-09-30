import React from 'react';

interface ExpandedSidebarComponent {
}

const ExpandedSidebar: React.FC<ExpandedSidebarComponent> = () => {
    return (
        <div className="plex-sidebar">
            <div className="sidebar-header">
                <img src="/static/purpleserver/img/logo.svg" alt="Purplship" width="90"/>
                <button className="menu-icon v-5 is-open mobile-item is-block mobile-sidebar-trigger">
                    <span></span>
                </button>
            </div>
            <div className="sidebar-menu has-slimscroll">
                <a className="menu-item is-active">
                    <span>Home</span>
                </a>
                <a className="menu-item">
                    <span>Shipments</span>
                </a>
                <a className="menu-item">
                    <span>Settings</span>
                </a>
                <div className="naver"></div>
            </div>
        </div>
    );
}

export default ExpandedSidebar;
