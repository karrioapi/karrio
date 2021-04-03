import React, { useContext, useRef, useState } from 'react';
import { View } from '@/library/types';
import GenerateAPIModal from '@/components/generate-api-dialog';
import { TokenData } from '@/components/data/token-query';

interface APISettingsView extends View { }

const APISettings: React.FC<APISettingsView> = () => {
  const { token } = useContext(TokenData)
  const [isRevealed, setIsRevealed] = useState<boolean>(false);
  const tokenInput = useRef<HTMLInputElement>(null);

  const copy = (_: React.MouseEvent) => {
    tokenInput.current?.select();
    document.execCommand("copy");
  };

  return (
    <>

      <header className="px-2 pt-1 pb-4">
        <span className="subtitle is-4">API Key</span>
      </header>

      <hr />

      <div className="columns py-6">
        <div className="column is-5">
          <p className="subtitle is-6 py-1">Token</p>
          <p className="is-size-7 pr-6">Use this key to authenticate your API calls.</p>
          <p className="is-size-7 pr-6"><strong>Warning:</strong> must be kept securely. Click regenerate to revoke old keys.</p>
        </div>

        <div className="column is-5">
          <div className="field">
            <div className="control">
              <input className="input is-small"
                type="text"
                title={isRevealed ? "Click to Copy" : ""}
                value={isRevealed ? token?.key : "......................."}
                style={{ maxWidth: "80%" }}
                ref={tokenInput}
                readOnly
              />
              <button className="button is-small is-light" onClick={copy} disabled={!isRevealed}>
                <span className="icon is-small"><i className="fas fa-copy"></i></span>
              </button>
              <button className="button is-small is-light" onClick={() => setIsRevealed(!isRevealed)}>
                {isRevealed ?
                  <span className="icon is-small"><i className="fas fa-eye-slash"></i></span> :
                  <span className="icon is-small"><i className="fas fa-eye"></i></span>}
              </button>
            </div>
          </div>
          <GenerateAPIModal>
            <span>Regenerate API key...</span>
          </GenerateAPIModal>
        </div>
      </div>

    </>
  );
}

export default APISettings;