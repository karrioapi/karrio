import { useAPIMetadata } from '@/context/api-metadata';
import React, { useState, useRef } from 'react';
import AppLink from '@/components/app-link';
import { signOut } from 'next-auth/react';
import { useUser } from '@/context/user';

interface AccountDropdownComponent { }


const AccountDropdown: React.FC<AccountDropdownComponent> = ({ ...props }) => {
  const { references } = useAPIMetadata();
  const menu = useRef<HTMLDivElement>(null);
  const btn = useRef<HTMLButtonElement>(null);
  const [isActive, setIsActive] = useState(false);
  const { query: { data: { user } = {} } } = useUser();

  const handleOnClick = (e: React.MouseEvent) => {
    setIsActive(!isActive);
    if (!isActive) document.addEventListener('click', onBodyClick);
    else document.removeEventListener('click', onBodyClick);
  };
  const onBodyClick = (e: MouseEvent) => {
    if (!btn.current?.contains(e.target as Node) && !menu.current?.contains(e.target as Node)) {
      setIsActive(false);
      document.removeEventListener('click', onBodyClick);
    }
  };

  return (
    <div className={`dropdown-wrap is-right ${isActive ? "is-active" : ""} m-0`} {...props}>
      <button className="dropdown-button is-rounded button is-small p-1" onClick={handleOnClick} ref={btn}>
        <span className="icon">
          <i className="is-size-6 fas fa-user"></i>
        </span>
      </button>
      <div className="drop-menu" ref={menu}>
        <div className="menu-inner">
          {user?.full_name !== undefined && user?.full_name !== null && user?.full_name !== '' && <>
            <div className="menu-header">
              <h3>{user?.full_name}</h3>
            </div>
          </>}

          <h6 className="is-size-7 mt-2 px-4 has-text-weight-semibold">{user?.email}</h6>

          <div className="options-items">
            <AppLink href="/settings/account" className="options-item">
              <i className="fas fa-cog"></i>
              <div className="option-content">
                <span>My Account</span>
                <span>Manage your account</span>
              </div>
            </AppLink>

            {(user?.is_staff === true) && <a href={references.ADMIN} target="_blank" rel="noreferrer" className="options-item">
              <i className="fas fa-tools"></i>
              <div className="option-content">
                <span>Admin Console</span>
                <span>Access the Administration panel</span>
              </div>
              <span className="icon is-small mt-2 ml-4">
                <i className="fas fa-external-link-alt"></i>
              </span>
            </a>}

            <a className="options-item" onClick={() => signOut()}>
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
