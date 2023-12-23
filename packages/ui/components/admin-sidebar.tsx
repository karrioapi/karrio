import { useAPIMetadata } from '@karrio/hooks/api-metadata';
import { useRouter } from 'next/dist/client/router';
import { useAppMode } from '@karrio/hooks/app-mode';
import { formatRef, p } from '@karrio/lib';
import React, { useRef } from 'react';
import { AppLink } from './app-link';
import getConfig from 'next/config';
import Image from 'next/image';

const { publicRuntimeConfig } = getConfig();

interface AdminSidebarComponent { }

export const AdminSidebar: React.FC<AdminSidebarComponent> = () => {
  const router = useRouter();
  const sidebar = useRef<HTMLDivElement>(null);
  const dismissAction = useRef<HTMLButtonElement>(null);
  const { basePath } = useAppMode();
  const { metadata } = useAPIMetadata();

  const dismiss = (e: React.MouseEvent) => {
    e.preventDefault();
    sidebar.current?.classList.remove('is-mobile-active');
    dismissAction.current?.classList.remove('is-mobile-active');
  };
  const isActive = (path: string) => {
    if (path === "/admin") return path === router.pathname;
    return router.pathname.includes(`${basePath}${path}`.replace('//', '/'));
  };
  const activeClass = (path: string) => isActive(path) ? 'is-active' : '';

  return (
    <div className="plex-sidebar admin-sidebar" ref={sidebar}>

      <div className="admin-sidebar-menu card px-0 ml-2">

        <header className="admin-sidebar-header p-3 has-background-light">
          <div className="media">
            <div className="media-left">
              <figure className="image is-32x32">
                <Image src={p`/carriers/${metadata?.APP_NAME || 'X'}_icon.svg`} width={32} height={32} alt="app icon" />
              </figure>
            </div>
            <div className="media-content" style={{ overflow: 'hidden' }}>
              <p className="title is-size-6 text-ellipsis">{formatRef(metadata?.APP_NAME)?.toLocaleLowerCase()}</p>
              <p className="subtitle is-size-7">{location.host}</p>
            </div>
          </div>
        </header>
        <button className="button sidebar-menu-button" onClick={dismiss} ref={dismissAction}>
          <span className="icon is-small">
            <i className="fas fa-times"></i>
          </span>
        </button>

        <hr className='my-0' style={{ height: '1px' }} />

        <div className="sidebar-menu has-slimscroll py-2" style={{ height: "calc(100% - 60px)" }}>
          <AppLink href="/admin" className={"menu-item px-3 " + activeClass("/admin")} shallow={false} prefetch={false}>
            <i className={`fa fa-layer-group mr-2 ${isActive("/admin") ? "" : 'has-text-grey'}`}></i>
            <span className="has-text-weight-bold">Platform details</span>
          </AppLink>
          <AppLink href="/admin/carrier_connections" className={"menu-item px-3 " + activeClass("/admin/carrier_connections")} shallow={false} prefetch={false}>
            <i className={`fa fa-truck mr-2 ${isActive("/admin/carrier_connections") ? "" : 'has-text-grey'}`}></i>
            <span className="has-text-weight-bold">Carrier connections</span>
          </AppLink>
          <AppLink href="/admin/user_accounts" className={"menu-item px-3 " + activeClass("/admin/user_accounts")} shallow={false} prefetch={false}>
            <i className={`fa fa-user-lock mr-2 ${isActive("/admin/user_accounts") ? "" : 'has-text-grey'}`}></i>
            <span className="has-text-weight-bold">Users and permissions</span>
          </AppLink>

          {metadata?.MULTI_ORGANIZATIONS && <>
            <AppLink href="/admin/organization_accounts" className={"menu-item px-3 " + activeClass("/admin/organization_accounts")} shallow={false} prefetch={false}>
              <i className={`fa fa-users mr-2 ${isActive("/admin/organization_accounts") ? "" : 'has-text-grey'}`}></i>
              <span className="has-text-weight-bold">Organization accounts</span>
            </AppLink>
          </>}
          {!metadata?.MULTI_ORGANIZATIONS && <>
            <button className={"button is-white menu-item px-3"} disabled>
              <i className={`fa fa-users mr-2 has-text-grey`}></i>
              <span className="has-text-weight-bold">Organization accounts</span>
            </button>
          </>}

          <AppLink href="/admin/surcharges" className={"menu-item px-3 " + activeClass("/admin/surcharges")} shallow={false} prefetch={false}>
            <i className={`fa fa-percent mr-2 ${isActive("/admin/surcharges") ? "" : 'has-text-grey'}`}></i>
            <span className="has-text-weight-bold">Surcharge and discounts</span>
          </AppLink>

          <button className={"button is-white menu-item px-3"} disabled>
            <i className={`fas fa-file-alt mr-2 has-text-grey`}></i>
            <span className="has-text-weight-bold">Platform activity log</span>
          </button>
        </div>

      </div>
    </div>
  );
}
