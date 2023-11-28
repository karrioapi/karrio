import { useOrganizationInvitation } from '@karrio/hooks/organization';
import { Notifier, Notify } from '../components/notifier';
import React, { useContext, useState } from 'react';
import { NotificationType } from '@karrio/types';
import { Loading } from '../components/loader';
import { removeUrlParam } from '@karrio/lib';
import { useUser } from '@karrio/hooks/user';
import { useRouter } from 'next/router';

type OperationType = { onChange?: (orgId: string) => void; };
interface AcceptInvitationInterface {
  acceptInvitation: (operation?: OperationType) => void;
}

export const AcceptInvitationContext = React.createContext<AcceptInvitationInterface>({} as AcceptInvitationInterface);

export const AcceptInvitationProvider: React.FC<{ children?: React.ReactNode }> = ({ children }) => {
  const router = useRouter();
  const { query: { data: { user } = {} } } = useUser();
  const { notify } = useContext(Notify);
  const { loading, setLoading } = useContext(Loading);
  const [isActive, setIsActive] = useState<boolean>(false);
  const [key, setKey] = useState<string>(`invite-${Date.now()}`);
  const { accept_invitation } = router.query as { accept_invitation: string };
  const [operation, setOperation] = useState<OperationType>({} as OperationType);
  const { query: { error, data: { organization_invitation } = {} }, ...mutation } = useOrganizationInvitation(accept_invitation);

  const acceptInvitation = (operation?: OperationType) => {
    setKey(`invite-${Date.now()}`);
    operation && setOperation(operation);
    setIsActive(true);
  };
  const close = ({ updated, orgId }: any | { updated?: boolean }) => {
    setIsActive(false);
    setKey(`invite-${Date.now()}`);
    (updated && operation?.onChange) && operation.onChange(orgId);
    removeUrlParam('accept_invitation');
  };
  const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
    evt.preventDefault();
    setLoading(true);
    try {
      const data = await mutation.acceptInvitation.mutateAsync({ guid: accept_invitation });
      const orgId = data?.accept_organization_invitation.organization?.id
      setTimeout(() => close({ updated: true, orgId }), 500);
    } catch (message: any) {
      notify({ type: NotificationType.error, message });
    }
    setLoading(false);
  };

  return (
    <>
      <AcceptInvitationContext.Provider value={{ acceptInvitation }}>
        {children}
      </AcceptInvitationContext.Provider>

      <Notifier>
        <div className={`modal ${isActive ? "is-active" : ""}`} key={key}>
          <div className="modal-background"></div>
          {isActive && <form className="modal-card" onSubmit={handleSubmit}>
            <section className="modal-card-body modal-form">
              <div className="form-floating-header p-4">
                <span className="has-text-weight-bold is-size-6">Accept Invitation</span>
              </div>
              <div className="p-3 my-4"></div>

              {!!error &&
                <p className="is-size-6 has-text-centered">
                  Error, invalid or expired organization invitation token!
                </p>}

              {!error && organization_invitation?.invitee_identifier !== user?.email &&
                <p className="is-size-6 has-text-centered">
                  The invitation is not for this account.
                </p>}

              {organization_invitation?.invitee_identifier === user?.email &&
                <p className="is-size-6 has-text-centered">
                  Click Confirm to accept the invitation to <strong>{organization_invitation?.organization_name}</strong>.
                </p>}

              <div className="p-3 my-5"></div>
              <div className="form-floating-footer has-text-centered p-1">
                <button className="button is-default m-1 is-small" onClick={close}>
                  <span>Dismiss</span>
                </button>
                {organization_invitation?.invitee_identifier === user?.email &&
                  <button className="button is-primary m-1 is-small" type="submit" disabled={loading}>
                    <span>Confirm</span>
                  </button>}
              </div>
            </section>
          </form>}

          <button className="modal-close is-large has-background-dark" aria-label="close" onClick={close}></button>
        </div>
      </Notifier>
    </>
  )
};

export function useAcceptInvitation() {
  return useContext(AcceptInvitationContext);
}
