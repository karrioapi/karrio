"use client";
import { OrganizationManagement } from "@karrio/ui/forms/organization-management";
import { InviteMemberProvider } from "@karrio/ui/modals/invite-member-modal";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import { ConfirmModal } from "@karrio/ui/modals/confirm-modal";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { AppLink } from "@karrio/ui/components/app-link";

export const generateMetadata = dynamicMetadata("Organization Settings");

export default function AccountPage(pageProps: any) {
  const Component = (): JSX.Element => {
    const { metadata } = useAPIMetadata();
    return (
      <>
        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <span className="title is-4">Settings</span>
          <div></div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink
                href="/settings/account"
                shallow={false}
                prefetch={false}
              >
                <span>Account</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink
                href="/settings/profile"
                shallow={false}
                prefetch={false}
              >
                <span>Profile</span>
              </AppLink>
            </li>
            {metadata?.MULTI_ORGANIZATIONS && (
              <li
                className={`is-capitalized has-text-weight-semibold is-active`}
              >

                <AppLink
                  href="/settings/organization"
                  shallow={false}
                  prefetch={false}
                >
                  <span>Organization</span>
                </AppLink>
              </li>
            )}
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink
                href="/settings/addresses"
                shallow={false}
                prefetch={false}
              >
                <span>Addresses</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink
                href="/settings/parcels"
                shallow={false}
                prefetch={false}
              >
                <span>Parcels</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink
                href="/settings/templates"
                shallow={false}
                prefetch={false}
              >
                <span>Templates</span>
              </AppLink>
            </li>
          </ul>
        </div>

        {metadata?.MULTI_ORGANIZATIONS && (
          <div>
            <InviteMemberProvider>
              <OrganizationManagement />
            </InviteMemberProvider>
          </div>
        )}
      </>
    );
  };

  return (
    <>
      <ConfirmModal>
        <Component />
      </ConfirmModal>
    </>
  );
}
