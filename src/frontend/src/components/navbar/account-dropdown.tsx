import React, { useState, useRef } from 'react';
import { Link } from "@reach/router";
import { UserInfo } from '@/library/api';


interface AccountDropdownComponent {
    user: UserInfo;
}


const AccountDropdown: React.FC<AccountDropdownComponent> = ({ user }) => {
    const [isActive, setIsActive] = useState(false);
    const menu = useRef<HTMLDivElement>(null);
    const handleBlur = (e: React.FocusEvent) => {
        if (e.relatedTarget == null) {
            setIsActive(false);
        }
    };

    return (
        <div className={`dropdown-wrap is-right ${isActive ? "is-active": ""}`}
            onBlur={handleBlur}
            onClick={() => {setIsActive(true); menu.current?.focus()}}
            >

            <span className="indicator"></span>
            <button className="dropdown-button has-image">
                <img src="/static/purpleserver/client/profile.svg" alt="Purplship Profile" />
            </button>
            <div className="drop-menu" onBlur={() => setIsActive(false)} ref={menu}>
                <div className="menu-inner">
                    <div className="menu-header">
                        <h3>Menu</h3>
                    </div>
                    <div className="options-items">
                        <Link to="settings" className="options-item">
                            <i className="fas fa-user"></i>
                            <div className="option-content">
                                <span>My Account</span>
                                <span>Manage your account</span>
                            </div>
                        </Link>
                        { user.isStaff && <a href="/admin" className="options-item">
                                <i className="fas fa-cog"></i>
                                <div className="option-content">
                                    <span>Console</span>
                                    <span>Access the Administration panel</span>
                                </div>
                            </a>
                        }
                        <a href="/logout" className="options-item">
                            <i className="fas fa-power-off"></i>
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
