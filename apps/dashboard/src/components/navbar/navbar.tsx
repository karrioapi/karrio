import ShortcutDropdown from '@/components/navbar/shortcut-dropdown';
import AccountDropdown from '@/components/navbar/account-dropdown';
import ModeIndicator from '@/components/mode-indicator';
import SearchBar from '@/components/navbar/search-bar';
import React from 'react';

interface NavbarComponent {
  showModeIndicator?: boolean;
}

const Navbar: React.FC<NavbarComponent> = ({ showModeIndicator }) => {
  const openSidebar = (e: React.MouseEvent) => {
    e.preventDefault();
    document.querySelector('.plex-sidebar')?.classList.add('is-mobile-active');
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

        {showModeIndicator && <ModeIndicator />}
      </div>
    </>
  );
}

export default Navbar;
