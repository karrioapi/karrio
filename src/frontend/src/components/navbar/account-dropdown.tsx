import React from 'react';

interface AccountDropdownComponent {
}

const AccountDropdown: React.FC<AccountDropdownComponent> = () => {
    return (
        <div className="dropdown-wrap dropdown is-right">
            <div className="dropdown-trigger">
                <span className="indicator"></span>
                <button className="dropdown-button has-image">
                    <img src="/static/purpleserver/client/profile.svg" alt="" />
                </button>
            </div>
            <div className="dropdown-menu" role="menu">
                <div className="dropdown-content menu-inner">
                    <div className="menu-header">
                        <h3>Menu</h3>
                    </div>
                    <div className="options-items">
                        <a className="options-item">
                            <i data-feather="file-text"></i>
                            <div className="option-content">
                                <span>My Invoices</span>
                                <span>View your invoices</span>
                            </div>
                        </a>
                        <a className="options-item">
                            <i data-feather="user"></i>
                            <div className="option-content">
                                <span>My Profile</span>
                                <span>View your profile</span>
                            </div>
                        </a>
                        <a className="options-item">
                            <i data-feather="briefcase"></i>
                            <div className="option-content">
                                <span>My Teams</span>
                                <span>View your teams</span>
                            </div>
                        </a>
                        <a className="options-item">
                            <i data-feather="lock"></i>
                            <div className="option-content">
                                <span>Logout</span>
                                <span>Logout from your account</span>
                            </div>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default AccountDropdown;
