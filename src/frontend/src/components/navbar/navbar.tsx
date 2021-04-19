import React, { useContext } from 'react';
import AccountDropdown from '@/components/navbar/account-dropdown';
import { UserData, UserType } from '@/components/data/user-query';

interface NavbarComponent { }

const Navbar: React.FC<NavbarComponent> = () => {
    const { user } = useContext(UserData)
    const openSidebar = (e: React.MouseEvent) => {
        e.preventDefault();
        document.querySelector('.plex-sidebar')?.classList.add('is-mobile-active');
    };

    return (
        <div className="static-nav">
            <div className="nav-start">

                <div className="nav-item mobile-item is-flex">
                    <button className="menu-icon v-2 mobile-sidebar-trigger" onClick={openSidebar}>
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

                <AccountDropdown user={user || {} as UserType} />

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
