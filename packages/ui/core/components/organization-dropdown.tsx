import {
  OrganizationType,
  useOrganizationMutation,
  useOrganizations,
} from "@karrio/hooks/organization";
import { useCreateOrganizationDialog } from "@karrio/ui/components/create-organization-dialog";
import React, { useContext, useEffect, useRef, useState } from "react";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { useAPIToken } from "@karrio/hooks/api-token";
import { useSearchParams } from "next/navigation";
import { isNoneOrEmpty } from "@karrio/lib";
import { Loading } from "./loader";
import { p } from "@karrio/lib";
import Image from "next/image";

export const OrganizationDropdown = (): JSX.Element => {
  const trigger = useRef<HTMLButtonElement>(null);
  const searchParams = useSearchParams();
  const { query } = useAPIToken();
  const mutation = useOrganizationMutation();
  const { setLoading } = useContext(Loading);
  const { organizations, organization } = useOrganizations();
  const {
    metadata: { ALLOW_MULTI_ACCOUNT },
  } = useAPIMetadata();
  const { createOrganization } = useCreateOrganizationDialog();
  const [isActive, setIsActive] = useState<boolean>(false);
  const [selected, setSelected] = useState<OrganizationType>();
  const [initialized, setInitialized] = useState<boolean>(false);

  const handleOnClick = (e: React.MouseEvent) => {
    setIsActive(!isActive);
    if (!isActive) {
      document.addEventListener("click", onBodyClick);
    } else {
      document.removeEventListener("click", onBodyClick);
    }
  };
  const onBodyClick = (e: MouseEvent) => {
    if (!trigger.current?.contains(e.target as Node)) {
      setIsActive(false);
      document.removeEventListener("click", onBodyClick);
    }
  };
  const select = (org: OrganizationType) => async (e: any) => {
    if (!isActive) {
      setIsActive(true);
      document.addEventListener("click", onBodyClick);
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
      },
    });
  };

  useEffect(() => {
    setSelected(organization);
  }, [organization]);
  // Note: Invite acceptance is now handled inline on /accept-invite

  return (
    <>
      {(organizations || []).length > 0 && (
        <div
          className={`dropdown ${isActive ? "is-active" : ""}`}
          style={{ widows: "100%" }}
        >
          <div className="dropdown-trigger">
            <button
              className="button is-white has-text-weight-bold has-text-grey select pr-4"
              aria-haspopup="true"
              aria-controls="dropdown-menu"
              onClick={handleOnClick}
              ref={trigger}
            >
              <span className="icon">
                <i className="fas fa-store"></i>
              </span>
              <span className="mr-4">{selected?.name || ""}</span>
            </button>
          </div>

          <div
            className="dropdown-menu"
            id="dropdown-menu"
            role="menu"
            style={{ minWidth: "calc(100%)" }}
          >
            <div className="dropdown-content is-menu">
              {/* Organization list */}
              {(organizations || []).map((org) => (
                <a
                  key={`org-${org?.id}-${new Date()}`}
                  onClick={select(org)}
                  className={`dropdown-item ${org?.id === selected?.id ? "is-active" : ""}`}
                >
                  <i className="fas fa-store"></i>
                  <span className="px-2">{org?.name}</span>
                </a>
              ))}

              {/* Create organization action */}
              {ALLOW_MULTI_ACCOUNT && (
                <a onClick={() => create()} className="dropdown-item">
                  <i className="fas fa-plus"></i>
                  <span className="px-2">New organization</span>
                </a>
              )}
            </div>
          </div>
        </div>
      )}

      {query.isFetched && (organizations || []).length === 0 && (
        <Image
          src={p`/icon.svg`}
          className="mt-2"
          width={30}
          height={40}
          alt="logo"
        />
      )}
    </>
  );
};
