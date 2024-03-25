import { WorkspaceConfigForm } from "@karrio/ui/forms/workspace-config-form";
import { CloseAccountAction } from "@karrio/ui/forms/close-account-action";
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
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
              <AppLink href="/settings/account" shallow={false} prefetch={false}>
                <span>Account</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/settings/profile" shallow={false} prefetch={false}>
                <span>Profile</span>
              </AppLink>
            </li>
            {MULTI_ORGANIZATIONS && <li className={`is-capitalized has-text-weight-semibold`}>
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

        <div>

          {/* General preferences section */}
          <WorkspaceConfigForm pageProps={pageProps} />

          <hr style={{ height: '1px' }} />

          {/* Close account section */}
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
        <Component />
      </ConfirmModal>

    </DashboardLayout>
  ), pageProps)
}
