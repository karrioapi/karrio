"use client";
import { LabelTemplateEditModalProvider } from "@karrio/ui/core/modals/label-template-edit-modal";
import { ConnectProviderModal } from "@karrio/ui/core/modals/connect-provider-modal";
import { SystemConnectionList } from "@karrio/ui/core/forms/system-carrier-list";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import { ConfirmModal } from "@karrio/ui/core/modals/confirm-modal";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { ModalProvider } from "@karrio/ui/core/modals/modal";
import { bundleContexts } from "@karrio/hooks/utils";

export const generateMetadata = dynamicMetadata("System Connections");
const ContextProviders = bundleContexts([
  ModalProvider,
  ConfirmModal,
  ConnectProviderModal,
  LabelTemplateEditModalProvider,
]);

export default function Page() {
  const Component = (): JSX.Element => {
    return (
      <>
        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <span className="title is-4">Carriers</span>
          <div></div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/connections" shallow={false} prefetch={false}>
                <span>Your Accounts</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
              <AppLink
                href="/connections/system"
                shallow={false}
                prefetch={false}
              >
                <span>System Accounts</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink
                href="/connections/rate-sheets"
                shallow={false}
                prefetch={false}
              >
                <span>Rate Sheets</span>
              </AppLink>
            </li>
          </ul>
        </div>

        <SystemConnectionList />
      </>
    );
  };

  return (
    <>
      <ContextProviders>
        <Component />
      </ContextProviders>
    </>
  );
}
