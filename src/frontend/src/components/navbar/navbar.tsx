import React from 'react';
import AccountDropdown from '@/components/navbar/account-dropdown';
import { UserInfo } from '@/library/api';

interface NavbarComponent {
    user: UserInfo;
}

const Navbar: React.FC<NavbarComponent> = ({ user }) => {
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
                        <input type="text" className="input search-field" placeholder="Search for shipments..." />
                        <div className="form-icon">
                            <i className="fas fa-search"></i>
                        </div>
                        <div className="search-results has-slimscroll"></div>
                    </div>
                </div>
            </div>
            <div className="nav-end">

                <div className="nav-item mobile-item is-flex mobile-search-trigger">
                    <i className="fas fa-search"></i>
                </div>

                <AccountDropdown user={user} />

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
    );
}

export default Navbar;
