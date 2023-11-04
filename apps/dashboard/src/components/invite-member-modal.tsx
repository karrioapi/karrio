import React, { useContext, useEffect, useRef, useState } from 'react';
import { useOrganizationMutation, useOrganizations } from '@/context/organization';
import { validationMessage, validityCheck } from '@/lib/helper';
import InputField from '@/components/generic/input-field';
import Notifier, { Notify } from '@/components/notifier';
import { useLoader } from '@/components/loader';
import { NotificationType } from '@/lib/types';
import { p } from '@/lib/client';

type OperationType = {
  onChange?: () => void;
};
interface InviteMemberInterface {
  sendInvites: (operation?: OperationType) => void;
}

export const InviteMemberContext = React.createContext<InviteMemberInterface>({} as InviteMemberInterface);

const InviteMemberProvider: React.FC<{}> = ({ children }) => {
  const form = useRef<HTMLFormElement>(null);
  const { notify } = useContext(Notify);
  const mutation = useOrganizationMutation();
  const { loading, setLoading } = useLoader();
  const { organization } = useOrganizations();
  const [isActive, setIsActive] = useState<boolean>(false);
  const [key, setKey] = useState<string>(`invite-${Date.now()}`);
  const [operation, setOperation] = useState<OperationType>({} as OperationType);
  const [emails, setEmails] = useState<string[]>([]);
  const [isValid, setIsValid] = React.useState<boolean>(true);

  const sendInvites = (operation?: OperationType) => {
    operation && setOperation(operation);
    setIsActive(true);
    setKey(`invite-${Date.now()}`);
  };
  const close = ({ updated }: any | { updated?: boolean }) => {
    setIsActive(false);
    setEmails([]);
    setKey(`invite-${Date.now()}`);
    (updated && operation?.onChange) && operation.onChange();
  };
  const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
    evt.preventDefault();
    setLoading(true);
    try {
      await mutation.sendOrganizationInvites.mutateAsync({
        redirect_url: location.origin + p`/accept-invite`,
        org_id: organization!.id,
        emails,
      });
      notify({ type: NotificationType.success, message: 'Invitations sent successfully!' });
      close({ updated: true });
    } catch (message: any) {
      notify({ type: NotificationType.error, message });
    }
    setLoading(false);
  };
  const handleKeyPress = (e: React.KeyboardEvent) => {
    const isValid = (e.target as any).checkValidity();
    if (e.key !== 'Enter' || loading || emails.length === 0) return;
    e.preventDefault();
    setIsValid(isValid);
    isValid && handleSubmit(e as any);
  };

  useEffect(() => { form.current && setIsValid(form.current!.checkValidity()); }, [emails]);

  return (
    <>
      <InviteMemberContext.Provider value={{ sendInvites }}>
        {children}
      </InviteMemberContext.Provider>

      <Notifier>
        <div className={`modal ${isActive ? "is-active" : ""}`} key={key}>
          <div className="modal-background"></div>
          {isActive &&
            <form className="modal-card"
              onChange={e => setIsValid((e.target as any).checkValidity())}
              onKeyPress={handleKeyPress}
              onSubmit={handleSubmit}
              ref={form}
            >
              <section className="modal-card-body modal-form">
                <div className="form-floating-header p-4">
                  <span className="has-text-weight-bold is-size-6">Invite team members</span>
                </div>
                <div className="p-3 my-4"></div>

                <InputField
                  type="email"
                  label="Enter team member email addresses"
                  placeholder="john@mail.com, jane@mail.com, etc."
                  defaultValue=""
                  fieldClass="mt-6"
                  onChange={e => setEmails(e.target.value.split(',').map(e => e.trim()))}
                  onInvalid={validityCheck(validationMessage('Please enter a valid email list'))}
                  multiple
                  required
                />

                <div className="p-3 my-5"></div>
                <div className="form-floating-footer has-text-centered p-1">
                  <button className="button is-default m-1 is-small" onClick={close} disabled={loading}>
                    <span>Cancel</span>
                  </button>
                  <button className={`button is-primary ${loading ? 'is-loading' : ''} m-1 is-small`}
                    disabled={!isValid || loading || emails.length === 0} type="submit">
                    <span>Send invites</span>
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

export function useInviteMember() {
  return useContext(InviteMemberContext);
}

export default InviteMemberProvider;
