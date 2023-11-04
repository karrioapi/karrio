import { OrganizationType, useOrganizationMutation, useOrganizations } from '@/context/organization';
import { useCreateOrganizationModal } from '@/components/create-organization-modal';
import { useAcceptInvitation } from '@/components/accept-invitation-modal';
import React, { useContext, useEffect, useRef, useState } from 'react';
import { useAPIMetadata } from '@/context/api-metadata';
import { useAPIToken } from '@/context/api-token';
import { isNoneOrEmpty } from '@/lib/helper';
import { Loading } from '@/components/loader';
import { useRouter } from 'next/router';
import { p } from '@/lib/client';
import Image from 'next/image';


const OrganizationDropdown: React.FC = () => {
  const trigger = useRef<HTMLInputElement>(null);
  const router = useRouter();
  const { query } = useAPIToken();
  const mutation = useOrganizationMutation();
  const { setLoading } = useContext(Loading);
  const { organizations, organization } = useOrganizations();
  const { metadata: { ALLOW_MULTI_ACCOUNT } } = useAPIMetadata();
  const { acceptInvitation } = useAcceptInvitation();
  const { createOrganization } = useCreateOrganizationModal();
  const [isActive, setIsActive] = useState<boolean>(false);
  const [selected, setSelected] = useState<OrganizationType>();
  const [initialized, setInitialized] = useState<boolean>(false);

  const handleOnClick = (e: React.MouseEvent) => {
    setIsActive(!isActive);
    if (!isActive) { document.addEventListener('click', onBodyClick); }
    else { document.removeEventListener('click', onBodyClick); }
  };
  const onBodyClick = (e: MouseEvent) => {
    if (!trigger.current?.contains(e.target as Node)) {
      setIsActive(false);
      document.removeEventListener('click', onBodyClick);
    }
  };
  const select = (org: OrganizationType) => async (e: any) => {
    if (!isActive) {
      setIsActive(true);
      document.addEventListener('click', onBodyClick);
    }
    e.preventDefault();
    e.stopPropagation();

    if (org.id === selected?.id) return;
    setLoading(true);
    setSelected(org);
    mutation.changeActiveOrganization(org.id).then(() => setLoading(false));
    setIsActive(false);
  };
  const create = async () => {
    createOrganization({
      onChange: (orgId: string) => {
        setIsActive(false);
        return mutation.changeActiveOrganization(orgId);
      }
    });
  };

  useEffect(() => { setSelected(organization); }, [organization]);
  useEffect(() => {
    if (!initialized && !isNoneOrEmpty(router.query.accept_invitation)) {
      acceptInvitation({ onChange: orgId => mutation.changeActiveOrganization(orgId) });
      setInitialized(true);
    }
    if (router.query && isNoneOrEmpty(router.query.accept_invitation)) {
      setInitialized(true);
    }
  }, [initialized, router.query]);

  return (
    <>
      {((organizations || []).length > 0) &&
        <div className={`dropdown ${isActive ? 'is-active' : ''}`} style={{ width: '100%' }}>
          <div className="dropdown-trigger control has-icons-left" style={{ width: '100%' }}>
            <div className="select is-fullwidth" aria-haspopup="true" aria-controls="dropdown-menu" onClick={handleOnClick} ref={trigger}>
              <input
                type="text"
                className="input is-clickable has-text-grey has-text-weight-semibold"
                value={selected?.name || "All Organizations"}
                onChange={_ => _}
                readOnly
              />
            </div>

            <span className="icon is-left">
              <i className="fas fa-store"></i>
            </span>
          </div>

          <div className="dropdown-menu" id="dropdown-menu" role="menu" style={{ width: '100%' }}>
            <div className="dropdown-content is-menu">
              {/* Organization list */}
              {(organizations || []).map(org => (
                <a
                  key={`org-${org?.id}-${new Date()}`}
                  onClick={select(org)}
                  className={`dropdown-item ${(org?.id === selected?.id) ? 'is-active' : ''}`}
                >
                  <i className="fas fa-store"></i>
                  <span className="px-2">{org?.name}</span>
                </a>
              ))}

              {/* Create organization action */}
              {ALLOW_MULTI_ACCOUNT && <a onClick={() => create()} className="dropdown-item">
                <i className="fas fa-plus"></i>
                <span className="px-2">New organization</span>
              </a>}

            </div>
          </div>
        </div>}

      {(query.isFetched && (organizations || []).length === 0) &&
        <Image src={p`/icon.svg`} className="mt-2" width="70" height="100" alt="logo" />}
    </>
  );
};

export default OrganizationDropdown;
