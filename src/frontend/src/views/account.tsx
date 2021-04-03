import React from 'react';
import { View } from '@/library/types';
import CloseAccountAction from '@/components/close-account-action';
import ProfileUpdateInput from '@/components/profile-update-input';

interface AccountView extends View { }

const Account: React.FC<AccountView> = () => {

  return (
    <>

      <header className="px-2 pt-1 pb-4">
        <span className="subtitle is-4">Manage Account</span>
      </header>

      <hr />

      <div className="columns py-6">
        <div className="column is-5 pr-6">
          <p className="subtitle is-6 py-1">Profile</p>
          <p className="is-size-7 pr-6">Your email address is your identity on Purplship and is used to log in.</p>
        </div>

        <div className="column is-7">
          <ProfileUpdateInput label="Email Address" propertyKey="email" inputType="email" />
          <ProfileUpdateInput label="Name (Optional)" propertyKey="full_name" inputType="text" />
        </div>
      </div>

      <hr />

      <div className="columns py-6">
        <div className="column is-5">
          <p className="subtitle is-6 py-1">Password</p>
        </div>

        <div className="column is-5">
          <a href="/password_change" className="button is-primary is-small">Change your password</a>
        </div>
      </div>

      <hr />

      <div className="columns py-6">
        <div className="column is-5">
          <p className="subtitle is-6 py-1">Close Account</p>
          <p className="is-size-7">
            <strong>Warning:</strong> You will lose access to your Purplship services
          </p>
        </div>

        <div className="column is-5">
          <CloseAccountAction>
            <span>Close this account...</span>
          </CloseAccountAction>
        </div>
      </div>

    </>
  );
}

export default Account;