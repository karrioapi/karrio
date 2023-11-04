import OrganizationManagement from "@/components/organization-management";
import SubscriptionManagement from "@/components/subscription-management";
import InviteMemberProvider from "@/components/invite-member-modal";
import CloseAccountAction from "@/components/close-account-action";
import Tabs, { TabStateProvider } from "@/components/generic/tabs";
import ProfileUpdateInput from "@/components/profile-update-input";
import PasswordManagement from "@/components/password-management";
import AuthenticatedPage from "@/layouts/authenticated-page";
import EmailManagement from "@/components/email-management";
import DashboardLayout from "@/layouts/dashboard-layout";
import ConfirmModal from "@/components/confirm-modal";
import Head from "next/head";

export { getServerSideProps } from "@/lib/data-fetching";


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
        <header className="px-0 py-4">
          <span className="title is-4">Settings</span>
        </header>

        <Tabs>
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

          {MULTI_ORGANIZATIONS && <div>
            <InviteMemberProvider>
              <OrganizationManagement />
            </InviteMemberProvider>
          </div>}

          {(pageProps as any).subscription && <div>
            <SubscriptionManagement />
          </div>}

        </Tabs>
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
