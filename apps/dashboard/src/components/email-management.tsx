import { request_email_change_request_email_change_errors } from 'karrio/graphql';
import React, { useContext, useRef, useState } from 'react';
import { useUser, useUserMutation } from '@/context/user';
import Notifier, { Notify } from '@/components/notifier';
import { useLoader } from '@/components/loader';
import { NotificationType } from '@/lib/types';

interface EmailManagementComponent { }

const EmailManagement: React.FC<EmailManagementComponent> = ({ children }) => {
  const mutation = useUserMutation();
  const { notify } = useContext(Notify);
  const { loading, setLoading } = useLoader();
  const { query: { data: { user } = {} } } = useUser();
  const email = useRef<HTMLInputElement>(null);
  const password = useRef<HTMLInputElement>(null);
  const [isActive, setIsActive] = useState<boolean>(false);
  const [errors, setErrors] = useState<request_email_change_request_email_change_errors[]>([]);

  const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
    evt.preventDefault();
    try {
      setLoading(true);
      await mutation.requestEmailChange.mutateAsync({
        email: email.current?.value as string,
        password: password.current?.value as string,
        redirect_url: `${location.origin}/email/change`,
      });
      notify({ type: NotificationType.success, message: "Email change request sent!" });
      setIsActive(false);
    } catch (error: any) {
      setErrors(Array.isArray(error) ? error : [error]);
    }
    setLoading(false);
  };
  const close = (evt: React.MouseEvent) => {
    evt.preventDefault();
    setIsActive(false);
  };
  const handleKeyPress = (e: React.KeyboardEvent) => {
    const isValid = (e.target as any).checkValidity();
    if (e.key !== 'Enter' || loading) return;
    e.preventDefault();
    isValid && handleSubmit(e as any);
  };

  return (
    <>
      <Notifier>
        <div className="field">
          <label className="label">Email</label>
          <p className="is-size-7 has-text-weight-semibold" style={{ maxWidth: "60%" }}>{user?.email}</p>
          <a className="is-size-7 has-text-info" onClick={() => setIsActive(true)}>Change email</a>
        </div>

        <div className={`modal ${isActive ? "is-active" : ""}`}>
          <div className="modal-background"></div>
          {isActive && <form className="modal-card" onSubmit={handleSubmit} onKeyPress={handleKeyPress}>
            <section className="modal-card-body modal-form">
              <div className="form-floating-header p-4">
                <span className="has-text-weight-bold is-size-6">Change your email</span>
              </div>
              <div className="p-3 my-4"></div>

              {(errors as any[]).filter(({ message }) => message).map(({ message }, key) => (
                <p key={key} className="has-text-danger is-size-7">{message}</p>
              ))}

              <p className="is-size-6 mt-3 mb-1 has-text-weight-bold">1. Enter a new email</p>
              <p className="is-size-7 mb-5">We’ll send you an email to the new address to verify that you own it.</p>

              <div className="field">
                <input className="input is-small"
                  id="email"
                  name="name"
                  type="text"
                  placeholder="Email"
                  required
                  ref={email}
                />
                {errors.filter(error => error.field === 'email').map(({ messages }) => (
                  messages.map((message, index) => <p key={index} className="has-text-danger is-size-7">{message}</p>)
                ))}
                {(errors as any[]).filter(({ validation }) => validation && validation.email).map(({ validation }, key) => (
                  <p key={key} className="has-text-danger is-size-7">{validation['email'] as string}</p>
                ))}
              </div>

              <hr className="my-4" style={{ height: '1px' }} />

              <p className="is-size-6 mt-3 mb-1 has-text-weight-bold">2. Enter your current password</p>
              <p className="is-size-7 mb-5">Enter the password you currently use to login.</p>

              <div className="field">
                <input className="input is-small"
                  id="id_password"
                  name="password"
                  type="password"
                  placeholder="Password"
                  required
                  ref={password}
                />
                {errors.filter(error => error.field === 'password').map(({ messages }) => (
                  messages.map((message, index) => <p key={index} className="has-text-danger is-size-7">{message}</p>)
                ))}
                {(errors as any[]).filter(({ validation }) => validation && validation.password).map(({ validation }, key) => (
                  <p key={key} className="has-text-danger is-size-7">{validation['password'] as string}</p>
                ))}
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

export default EmailManagement;
