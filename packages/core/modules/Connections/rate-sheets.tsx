"use client";
import { LabelTemplateEditModalProvider } from "@karrio/ui/core/modals/label-template-edit-modal";
import { RateSheetEditModalProvider } from "@karrio/ui/core/modals/rate-sheet-edit-modal";
import { ConnectProviderModal } from "@karrio/ui/core/modals/connect-provider-modal";
import { RateSheetModalEditor } from "@karrio/ui/core/modals/rate-sheet-editor";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import { RateSheetList } from "@karrio/ui/core/forms/rate-sheet-list";
import { useRateSheetMutation } from "@karrio/hooks/rate-sheet";
import { ConfirmModal } from "@karrio/ui/core/modals/confirm-modal";
import { AppLink } from "@karrio/ui/core/components/app-link";
import { ModalProvider } from "@karrio/ui/core/modals/modal";
import { bundleContexts } from "@karrio/hooks/utils";

export const generateMetadata = dynamicMetadata("Rate Sheets");
const ContextProviders = bundleContexts([
  ModalProvider,
  ConfirmModal,
  ConnectProviderModal,
  LabelTemplateEditModalProvider,
  RateSheetEditModalProvider,
]);

export default function ConnectionsPage(pageProps: any) {
  const Component = (): JSX.Element => {
    const mutation = useRateSheetMutation();

    return (
      <>
        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <span className="title is-4">Carriers</span>
          <div>
            <RateSheetModalEditor
              onSubmit={(_) => mutation.createRateSheet.mutateAsync(_)}
              trigger={
                <button className="button is-small">
                  <span>Add rate sheet</span>
                </button>
              }
            />
          </div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/connections" shallow={false} prefetch={false}>
                <span>Your Accounts</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink
                href="/connections/system"
                shallow={false}
                prefetch={false}
              >
                <span>System Accounts</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
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

        <RateSheetList />
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
