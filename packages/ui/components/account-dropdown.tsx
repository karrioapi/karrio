import { useAPIMetadata } from '@karrio/hooks/api-metadata';
import { useUser } from '@karrio/hooks/user';
import { signOut } from 'next-auth/react';
import { Dropdown } from './dropdown';
import { AppLink } from './app-link';
import React from 'react';

interface AccountDropdownComponent { }


export const AccountDropdown: React.FC<AccountDropdownComponent> = ({ ...props }) => {
  const { references } = useAPIMetadata();
  const { query: { data: { user } = {} } } = useUser();

  return (
    <>
      <Dropdown>

        {/* Dropdown trigger  */}
        <button className="button is-default mx-1" style={{ borderRadius: '50%' }}>
          <span className="icon">
            <i className="is-size-6 fas fa-cog"></i>
          </span>
        </button>

        {/* Dropdown content  */}
        <article className="menu-inner panel is-white p-3 has-background-white" style={{ width: "" }}>
          <div className="menu-inner">
            {user?.full_name !== undefined && user?.full_name !== null && user?.full_name !== '' && <>
              <div className="menu-header">
                <h3>{user?.full_name}</h3>
              </div>
            </>}

            <h6 className="is-size-7 mt-2 has-text-weight-semibold">{user?.email}</h6>

            <div className="options-items">
              <AppLink href="/settings/account" className="options-item px-0">
                <i className="fas fa-cog"></i>
                <div className="option-content">
                  <span>My Account</span>
                </div>
              </AppLink>

              {(user?.is_staff === true) && <a href={references.ADMIN} target="_blank" rel="noreferrer" className="options-item px-0">
                <i className="fas fa-tools"></i>
                <div className="option-content">
                  <span>Admin Console</span>
                </div>
                <span className="icon is-small is-size-7 ml-2">
                  <i className="fas fa-external-link-alt"></i>
                </span>
              </a>}

              <a className="options-item is-vcentered px-0" onClick={() => signOut()}>
                <i className="fas fa-power-off"></i>
                <div className="option-content">
                  <span>Logout</span>
                </div>
              </a>
            </div>
          </div>
        </article>

      </Dropdown>
    </>
  );
}
