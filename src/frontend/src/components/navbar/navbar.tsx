import React from 'react';
import AccountDropdown from '@/components/navbar/account-dropdown';

interface NavbarComponent {
}

const Navbar: React.FC<NavbarComponent> = () => {
    return (
        <div className="static-nav">
            <div className="nav-start">

                <div className="nav-item mobile-item is-flex">
                    <button className="menu-icon v-2 mobile-sidebar-trigger">
                        <span></span>
                    </button>
                </div>

                <div className="field">
                    <div className="control has-icon">
                        <input type="text" className="input search-field" placeholder="Search for transactions, accounts..." />
                        <div className="form-icon">
                            <i data-feather="search"></i>
                        </div>
                        <div className="search-results has-slimscroll"></div>
                    </div>
                </div>
            </div>
            <div className="nav-end">

                <div className="nav-item mobile-item is-flex mobile-search-trigger">
                    <i data-feather="search"></i>
                </div>

                <AccountDropdown />

            </div>

            <div className="mobile-search">
                <div className="field">
                    <div className="control has-icon has-icon-right">
                        <input type="text" className="input search-field" placeholder="Search for transactions, accounts..." />
                        <div className="form-icon">
                            <i data-feather="search"></i>
                        </div>
                        <div className="form-icon right-icon mobile-search-trigger">
                            <i data-feather="x"></i>
                        </div>
                        <div className="search-results has-slimscroll"></div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Navbar;
