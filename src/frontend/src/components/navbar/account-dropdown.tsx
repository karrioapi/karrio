import React, { useState, useRef } from 'react';
import { Link } from "@reach/router";
import { UserInfo } from '@/library/api';


interface AccountDropdownComponent {
    user: UserInfo;
}


const AccountDropdown: React.FC<AccountDropdownComponent> = ({ user }) => {
    const [isActive, setIsActive] = useState(false);
    const btn = useRef<HTMLButtonElement>(null);
    const img = useRef<HTMLImageElement>(null);
    const handleOnClick = (e: React.MouseEvent) => {
        if (!isActive) {
            setIsActive(true);
            document.addEventListener('click', onBodyClick);
        }
        e.stopPropagation();
    };
    const onBodyClick = (e: MouseEvent) => {
        if (e.target !== btn.current && e.target !== img.current) {
            setIsActive(false);
            document.removeEventListener('click', onBodyClick);
        }
    };

    return (
        <div className={`dropdown-wrap is-right ${isActive ? "is-active": ""}`}>

            <span className="indicator"></span>
            <button className="dropdown-button has-image" onClick={handleOnClick} ref={btn}>
                <img src="/static/purpleserver/client/profile.svg" alt="Purplship Profile" ref={img}/>
            </button>
            <div className="drop-menu">
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
                        { user.is_staff && <a href="/admin" className="options-item">
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
