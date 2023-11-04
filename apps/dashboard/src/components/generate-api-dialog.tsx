import React, { useContext, useRef, useState } from 'react';
import { useAPITokenMutation } from '@/context/api-token';
import Notifier, { Notify } from '@/components/notifier';
import { useLoader } from '@/components/loader';
import { NotificationType } from '@/lib/types';
import { useUser } from '@/context/user';


const GenerateAPIModal: React.FC = ({ children }) => {
  const { notify } = useContext(Notify);
  const mutation = useAPITokenMutation();
  const { loading, setLoading } = useLoader();
  const password = useRef<HTMLInputElement>(null);
  const { query: { data: { user } = {} } } = useUser();
  const [isActive, setIsActive] = useState<boolean>(false);

  const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
    evt.preventDefault();
    try {
      setLoading(true);
      await mutation.updateToken.mutateAsync({ refresh: true, password: password.current?.value });
      setLoading(false);
      setIsActive(false);
      notify({ type: NotificationType.success, message: "New token generated successfully!" });
    } catch (err) {
      setLoading(false);
    }
  };
  const close = (evt: React.MouseEvent) => {
    evt.preventDefault();
    setIsActive(false);
  }

  return (
    <>
      <Notifier>
        <div onClick={() => setIsActive(true)}>
          {children}
        </div>

        <div className={`modal ${isActive ? "is-active" : ""}`}>
          <div className="modal-background"></div>
          {isActive && <form className="modal-card" onSubmit={handleSubmit}>
            <section className="modal-card-body modal-form">
              <div className="form-floating-header p-4">
                <span className="has-text-weight-bold is-size-6">Regenerate API key</span>
              </div>
              <div className="p-3 my-4"></div>

              <div className="notification is-warning is-light">
                This action will disable the current API key and generate a new one.
                We recommend reviewing your security history for events related to this key.
                Any webhook endpoints created with this key will stay active, even after the key is regenerated.
              </div>

              <hr className="mt-1 mb-2" style={{ height: '1px' }} />

              <p className="is-size-6 mt-3 mb-1 has-text-weight-bold">Additional authentication required</p>
              <p className="is-size-7 mb-5">To continue, please enter your password.</p>

              <div className="field">
                <label className="label">Email</label>
                <input className="input is-small"
                  id="email"
                  name="name"
                  type="text"
                  value={user?.email}
                  disabled
                />
              </div>

              <div className="field">
                <label className="label">Password</label>
                <input className="input is-small"
                  id="id_password"
                  name="password"
                  type="password"
                  placeholder="Password"
                  required
                  ref={password}
                />
              </div>

              <div className="p-3 my-5"></div>
              <div className="form-floating-footer has-text-centered p-1">
                <button className="button is-default m-1 is-small" onClick={close} disabled={loading}>
                  <span>Cancel</span>
                </button>
                <button className={`button is-primary ${loading ? 'is-loading' : ''} m-1 is-small`}
                  disabled={loading} type="submit">
                  <span>Confirm</span>
                </button>
              </div>
            </section>
          </form>}
          <button className="modal-close is-large has-background-dark" aria-label="close" onClick={close}></button>
        </div>
      </Notifier>
    </>
  )
};

export default GenerateAPIModal;
