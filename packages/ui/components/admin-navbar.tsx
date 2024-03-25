import { ShortcutDropdown } from './shortcut-dropdown';
import { AccountDropdown } from './account-dropdown';
import { SearchBar } from '../forms/search-bar';
import { AppLink } from './app-link';
import { p } from '@karrio/lib';
import Image from 'next/image';
import React from 'react';

interface NavbarComponent {
}

export const AdminNavbar: React.FC<NavbarComponent> = ({ }) => {
  const openSidebar = (e: React.MouseEvent) => {
    e.preventDefault();
    document.querySelector('.plex-sidebar')?.classList.add('is-mobile-active');
    document.querySelector('.sidebar-menu-button')?.classList.add('is-mobile-active');
  };

  return (
    <>
      <nav className="navbar is-align-items-center is-justify-content-space-between px-4" role="navigation" aria-label="main navigation">
        <div className="navbar-brand is-flex-grow-1 is-align-items-center">

          <div className="nav-item mobile-item is-flex px-2">
            <button className="menu-icon v-2 mobile-sidebar-trigger" onClick={openSidebar}>
              <span></span>
            </button>
          </div>

          <AppLink href="/" className="px-2" shallow={false} prefetch={false}>
            <Image src={p`/icon.svg`} width="20" height="60" alt="logo" />
          </AppLink>

        </div>

        <div className="navbar-menu is-flex-grow-2 px-2">
          <div className="navbar-start is-flex-grow-1">
            <SearchBar />
          </div>

          <div className="navbar-end is-flex-grow-1 is-align-items-center">

            <div className="nav-item">
              <ShortcutDropdown />
            </div>
            <div className="nav-item">
              <AccountDropdown />
            </div>

          </div>
        </div>

        {/* <div className="mobile-search">
          <div className="field">
            <div className="control has-icon has-icon-right">
              <input type="text" className="input search-field" placeholder="Search for shipments..." />
              <div className="form-icon">
                <i className="fas fa-search"></i>
              </div>
              <div className="form-icon right-icon mobile-search-trigger">
                <i className="fas fa-clear"></i>
              </div>
              <div className="search-results has-slimscroll"></div>
            </div>
          </div>
        </div> */}
      </nav>
    </>
  );
}
