import OrganizationDropdown from '@/components/sidebars/organization-dropdown';
import { useAPIMetadata } from '@/context/api-metadata';
import { useRouter } from 'next/dist/client/router';
import { useAppMode } from '@/context/app-mode';
import AppLink from '@/components/app-link';
import React, { useRef } from 'react';
import getConfig from 'next/config';
import { p } from '@/lib/client';
import Image from 'next/image';

const { publicRuntimeConfig } = getConfig();

interface ExpandedSidebarComponent { }

const ExpandedSidebar: React.FC<ExpandedSidebarComponent> = () => {
  const router = useRouter();
  const sidebar = useRef<HTMLDivElement>(null);
  const { testMode, basePath, switchMode } = useAppMode();
  const { metadata: { MULTI_ORGANIZATIONS, ORDERS_MANAGEMENT, DOCUMENTS_MANAGEMENT } } = useAPIMetadata();
  const [showSettingsMenus, setShowSettingsMenus] = React.useState(false);

  const dismiss = (e: React.MouseEvent) => {
    e.preventDefault();
    sidebar.current?.classList.remove('is-mobile-active');
  };
  const isActive = (path: string) => {
    if (path === basePath) return path === router.pathname;
    return router.pathname.includes(`${basePath}${path}`.replace('//', '/'));
  };
  const activeClass = (path: string) => isActive(path) ? 'is-active' : '';

  return (
    <div className="plex-sidebar" ref={sidebar}>
      <div className="sidebar-header pl-5 mb-4">
        {MULTI_ORGANIZATIONS
          ? <OrganizationDropdown />
          : <Image src={p`/icon.svg`} className="mt-1" width="30" height="100" alt="logo" />}
        <button className="menu-icon v-5 is-open mobile-item is-block mobile-sidebar-trigger ml-2" onClick={dismiss}>
          <span></span>
        </button>
      </div>
      <div className="sidebar-menu has-slimscroll py-2" style={{ height: "calc(100% - 60px)" }}>
        <AppLink href="/" className={"menu-item " + activeClass(basePath)} shallow={false} prefetch={false}>
          <i className={`fa fa-truck pr-3 ${isActive(basePath) ? "" : 'has-text-grey'}`}></i>
          <span className="has-text-weight-semibold">Shipments</span>
        </AppLink>

        <AppLink href="/trackers" className={"menu-item " + activeClass("/trackers")} shallow={false} prefetch={false}>
          <i className={`fa fa-location-arrow pr-3 ${isActive("/trackers") ? "" : 'has-text-grey'}`}></i>
          <span className="has-text-weight-semibold">Trackers</span>
        </AppLink>

        {ORDERS_MANAGEMENT &&
          <AppLink href="/orders" className={"menu-item " + activeClass("/orders")} shallow={false} prefetch={false}>
            <i className={`fa fa-inbox pr-3 ${isActive("/orders") ? "" : 'has-text-grey'}`}></i>
            <span className="has-text-weight-semibold">Orders</span>
          </AppLink>}

        <AppLink href="/connections" className={"menu-item " + activeClass("/connections")} shallow={false} prefetch={false}>
          <i className={`fa fa-th-list pr-3 ${isActive("/connections") ? "" : 'has-text-grey'}`}></i>
          <span className="has-text-weight-semibold">Carriers</span>
        </AppLink>

        {/* Settings */}
        <a className="menu-item menu-item my-0" onClick={() => setShowSettingsMenus(!showSettingsMenus)}>
          <i className={`fa fa-cog pr-3 has-text-grey`}></i>
          <span className="has-text-weight-semibold">Settings</span>
        </a>

        {(showSettingsMenus || window.location.pathname.includes('/settings')) && <>
          <AppLink href="/settings/account" className={"menu-item ml-5 " + activeClass("/settings/account")}>
            <span>Account</span>
          </AppLink>

          <AppLink href="/settings/addresses" className={"menu-item ml-5 " + activeClass("/settings/addresses")} shallow={false} prefetch={false}>
            <span>Addresses</span>
          </AppLink>

          <AppLink href="/settings/parcels" className={"menu-item ml-5 " + activeClass("/settings/parcels")} shallow={false} prefetch={false}>
            <span>Parcels</span>
          </AppLink>

          {DOCUMENTS_MANAGEMENT && <>
            <AppLink href="/settings/templates" className={"menu-item ml-5 " + activeClass("/settings/templates")} shallow={false} prefetch={false}>
              <span>Templates</span>
            </AppLink>
          </>}
        </>}

        <hr className="my-3 mx-5" style={{ height: '1px' }} />

        {testMode ?
          <a className="menu-item mode-menu-item" onClick={switchMode}>
            <i className="fas fa-toggle-on pr-3"></i>
            <span className="mode-menu-item has-text-weight-semibold">Viewing test data</span>
          </a>
          :
          <a className="menu-item has-text-grey" onClick={switchMode}>
            <i className="fas fa-toggle-off pr-3"></i>
            <span className="has-text-weight-semibold">View test data</span>
          </a>
        }

        {/* Developers */}
        <AppLink href="/developers/api" className="menu-item menu-item my-0" shallow={false} prefetch={false}>
          <i className={`fa fa-terminal pr-3 has-text-grey`}></i>
          <span className="has-text-weight-semibold">Developers</span>
        </AppLink>

        {window.location.pathname.includes('/developers') && <>
          <AppLink href="/developers/api" className={"menu-item ml-5 " + activeClass("/developers/api")} shallow={false} prefetch={false}>
            <span>API</span>
          </AppLink>

          <AppLink href="/developers/webhooks" className={"menu-item ml-5 " + activeClass("/developers/webhooks")} shallow={false} prefetch={false}>
            <span>Webhooks</span>
          </AppLink>

          <AppLink href="/developers/events" className={"menu-item ml-5 " + activeClass("/developers/events")} shallow={false} prefetch={false}>
            <span>Events</span>
          </AppLink>

          <AppLink href="/developers/logs" className={"menu-item ml-5 " + activeClass("/developers/logs")} shallow={false} prefetch={false}>
            <span>Logs</span>
          </AppLink>
        </>}
      </div>
      <div style={{ position: 'absolute', bottom: 10, left: 30, right: 10 }}>
        <span className="menu-item has-text-grey-light">
          Version: {publicRuntimeConfig.DASHBOARD_VERSION}
        </span>
      </div>
    </div>
  );
}

export default ExpandedSidebar;
