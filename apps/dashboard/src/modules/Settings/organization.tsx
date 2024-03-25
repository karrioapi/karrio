import { OrganizationManagement } from "@karrio/ui/forms/organization-management";
import { InviteMemberProvider } from "@karrio/ui/modals/invite-member-modal";
import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { ConfirmModal } from "@karrio/ui/modals/confirm-modal";
import { DashboardLayout } from "@/layouts/dashboard-layout";
import { AppLink } from "@karrio/ui/components/app-link";
import Head from "next/head";

export { getServerSideProps } from "@/context/main";


export default function AccountPage(pageProps: any) {
  const { APP_NAME, MULTI_ORGANIZATIONS } = (pageProps as any).metadata || {};

  const Component: React.FC = () => {

    return (
      <>

        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <span className="title is-4">Settings</span>
          <div></div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/settings/account" shallow={false} prefetch={false}>
                <span>Account</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/settings/profile" shallow={false} prefetch={false}>
                <span>Profile</span>
              </AppLink>
            </li>
            {MULTI_ORGANIZATIONS && <li className={`is-capitalized has-text-weight-semibold is-active`}>
              <AppLink href="/settings/organization" shallow={false} prefetch={false}>
                <span>Organization</span>
              </AppLink>
            </li>}
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/settings/addresses" shallow={false} prefetch={false}>
                <span>Addresses</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/settings/parcels" shallow={false} prefetch={false}>
                <span>Parcels</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/settings/templates" shallow={false} prefetch={false}>
                <span>Templates</span>
              </AppLink>
            </li>
          </ul>
        </div>

        {MULTI_ORGANIZATIONS && <div>
          <InviteMemberProvider>
            <OrganizationManagement />
          </InviteMemberProvider>
        </div>}
      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout>
      <Head><title>{`Organization Settings - ${APP_NAME}`}</title></Head>

      <ConfirmModal>
        <Component />
      </ConfirmModal>

    </DashboardLayout>
  ), pageProps)
}
