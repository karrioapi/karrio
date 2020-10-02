import React, { Fragment } from 'react';
import { View } from '@/library/types';

const Settings: React.FC<View> = () => {
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

        <div className="column is-5">
          <div className="field">
            <label className="label">Email Address</label>
            <div className="control">
              <input className="input is-small" type="email" placeholder="address email" />
            </div>
          </div>
          <div className="field">
            <label className="label">Name (Optional)</label>
            <div className="control">
              <input className="input is-small" type="text" placeholder="Full name" />
            </div>
          </div>
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
        </div>

        <div className="column is-5">
          <div className="field">
            <div className="control">
              <input className="input is-small" type="text" value="............................." style={{maxWidth: "80%"}}/>
              <button className="button is-small">reveal</button>
            </div>
          </div>
          <button className="button is-primary is-small">Regenerate API key...</button>
        </div>
      </div>

      <hr />

      <div className="columns py-6">
        <div className="column is-5">
          <p className="subtitle is-6 py-1">Close Account</p>
          <p className="is-size-7">
            <strong>Warning:</strong> You will lose access to your Purplship's services
          </p>
        </div>

        <div className="column is-5">
          <button className="button is-danger is-light">Close this account...</button>
        </div>
      </div>

    </Fragment>
  );
}

export default Settings;