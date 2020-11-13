import React, { Fragment, useState } from 'react';
import { View } from '@/library/types';
import GenerateAPIModal from '@/components/generate-api-dialog';
import CloseAccountAction from '@/components/close-account-action';
import { UserInfo } from '@/library/api';
import ProfileUpdateInput from '@/components/profile-update-input';

interface SettingsView extends View {
  token: string;
  user: UserInfo;
}

const Settings: React.FC<SettingsView> = ({ token, user }) => {
  const [isRevealed, setIsRevealed] = useState<boolean>(false);
  const copy = (e: React.MouseEvent) => {
    (e.target as HTMLInputElement).select();
    document.execCommand("copy");
  }

  return (
    <Fragment>

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
          <ProfileUpdateInput label="Email Address" propertyKey="email" inputType="email" user={user} />
          <ProfileUpdateInput label="Name (Optional)" propertyKey="full_name" inputType="text" user={user} />
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
          <p className="subtitle is-6 py-1">API Key</p>
          <p className="is-size-7 pr-6">Use this key to authenticate your API calls.</p>
          <p className="is-size-7 pr-6"><strong>Warning:</strong> must be kept securely. Click regenerate to revoke old keys.</p>
        </div>

        <div className="column is-5">
          <div className="field">
            <div className="control">
              <input className="input is-small" 
                type="text" 
                title={ isRevealed ? "Click to Copy" : "" }
                onClick={isRevealed ? copy : () =>{}}
                value={ isRevealed ? token : "..........."}
                style={{maxWidth: "80%"}} 
                readOnly
                />
              <button className="button is-small mr-1" onClick={() => setIsRevealed(!isRevealed) }>
                { isRevealed ? "hide" : "reveal" }
              </button>
            </div>
          </div>
          <GenerateAPIModal>
            <span>Regenerate API key...</span>
          </GenerateAPIModal>
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

    </Fragment>
  );
}

export default Settings;