import { ShortcutDropdown } from './shortcut-dropdown';
import { AccountDropdown } from './account-dropdown';
import { SearchBar } from '../forms/search-bar';
import React from 'react';

interface NavbarComponent { }

export const Navbar: React.FC<NavbarComponent> = ({ }) => {
  const openSidebar = (e: React.MouseEvent) => {
    e.preventDefault();
    document.querySelector('.plex-sidebar')?.classList.add('is-mobile-active');
    document.querySelector('.sidebar-menu-button')?.classList.add('is-mobile-active');
  };

  return (
    <>

      <div className="static-nav">
        <div className="nav-start">

          <div className="nav-item mobile-item is-flex">
            <button className="menu-icon v-2 mobile-sidebar-trigger" onClick={openSidebar}>
              <span></span>
            </button>
          </div>

          <SearchBar />

        </div>
        <div className="nav-end">

          <div className="nav-item mobile-item is-flex mobile-search-trigger">
            <i className="fas fa-search"></i>
          </div>

          <ShortcutDropdown />

          <AccountDropdown />

        </div>

        <div className="mobile-search">
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
        </div>

      </div>
    </>
  );
}
