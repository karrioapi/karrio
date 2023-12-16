import { OrganizationManagement } from "@karrio/ui/forms/organization-management";
import { SubscriptionManagement } from "@karrio/ui/forms/subscription-management";
import { InviteMemberProvider } from "@karrio/ui/modals/invite-member-modal";
import { CloseAccountAction } from "@karrio/ui/forms/close-account-action";
import { ProfileUpdateInput } from "@karrio/ui/forms/profile-update-input";
import { PasswordManagement } from "@karrio/ui/forms/password-management";
import { Tabs, TabStateProvider } from "@karrio/ui/components/tabs";
import { EmailManagement } from "@karrio/ui/forms/email-management";
import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { ConfirmModal } from "@karrio/ui/modals/confirm-modal";
import { DashboardLayout } from "@/layouts/dashboard-layout";
import Head from "next/head";
import { AppLink } from "@karrio/ui/components/app-link";

export { getServerSideProps } from "@/context/main";


export default function AccountPage(pageProps: any) {
  const { APP_NAME, MULTI_ORGANIZATIONS } = (pageProps as any).metadata || {};
  const tabs: string[] = [
    'Account',
    ...(MULTI_ORGANIZATIONS ? ['Organization'] : []),
    ...((pageProps as any).subscription ? ['Billing'] : []),
  ];

  const Component: React.FC = () => {

    return (
      <>

        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <span className="title is-4">Settings</span>
          <div></div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
              <AppLink href="/settings/account" shallow={false} prefetch={false}>
                <span>Account</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/settings/organization" shallow={false} prefetch={false}>
                <span>Organization</span>
              </AppLink>
            </li>
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


        <div>
          <div className="columns py-6 my-4">
            <div className="column is-5 pr-6">
              <p className="subtitle is-6 py-1">Profile</p>
              <p className="is-size-7 pr-6">Your email address is your identity on {APP_NAME} and is used to log in.</p>
            </div>

            <div className="column is-7">
              <EmailManagement />
              <ProfileUpdateInput label="Name (Optional)" propertyKey="full_name" inputType="text" />
            </div>
          </div>

          <hr style={{ height: '1px' }} />

          <div className="columns py-6 my-4">
            <div className="column is-5 pr-6">
              <p className="subtitle is-6 py-1">Password</p>
              <p className="is-size-7 pr-6">You can change your password.</p>
            </div>

            <PasswordManagement />
          </div>

          <hr style={{ height: '1px' }} />

          <div className="columns py-6 my-4">
            <div className="column is-5">
              <p className="subtitle is-6 py-1">Close Account</p>
              <p className="is-size-7">
                <strong>Warning:</strong> You will lose access to your {APP_NAME} services
              </p>
            </div>

            <div className="column is-5">
              <CloseAccountAction>
                <span>Close this account...</span>
              </CloseAccountAction>
            </div>
          </div>
        </div>
      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout>
      <Head><title>{`Account Settings - ${APP_NAME}`}</title></Head>

      <ConfirmModal>
        <TabStateProvider tabs={tabs} setSelectedToURL>
          <Component />
        </TabStateProvider>
      </ConfirmModal>

    </DashboardLayout>
  ), pageProps)
}
