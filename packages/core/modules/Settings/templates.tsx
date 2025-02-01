"use client";
import {
  useDocumentTemplateMutation,
  useDocumentTemplates,
} from "@karrio/hooks/document-template";
import {
  ConfirmModal,
  ConfirmModalContext,
} from "@karrio/ui/modals/confirm-modal";
import { TemplateDescription } from "@karrio/ui/components/template-description";
import { DocumentTemplateType, NotificationType } from "@karrio/types";
import { dynamicMetadata } from "@karrio/core/components/metadata";
import { useConfirmModal } from "@karrio/ui/modals/confirm-modal";
import { useNotifier } from "@karrio/ui/components/notifier";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { AppLink } from "@karrio/ui/components/app-link";
import React from "react";

export const generateMetadata = dynamicMetadata("Document Templates");

export default function TemplatesPage(pageProps: any) {
  const Component = (): JSX.Element => {
    const { notify } = useNotifier();
    const { metadata } = useAPIMetadata();
    const mutation = useDocumentTemplateMutation();
    const { confirm: confirmDeletion } = useConfirmModal();
    const {
      query: { data: { document_templates } = {}, ...query },
      filter,
      setFilter,
    } = useDocumentTemplates();

    const remove = (id: string) => async () => {
      await mutation.deleteDocumentTemplate.mutateAsync({ id });
    };
    const toggle =
      ({ active, id }: DocumentTemplateType) =>
        async () => {
          try {
            await mutation.updateDocumentTemplate.mutateAsync({
              id,
              active: !active,
            });
            notify({
              type: NotificationType.success,
              message: `template ${!active ? "enabled" : "disabled"}!`,
            });
          } catch (message: any) {
            notify({ type: NotificationType.error, message });
          }
        };

    return (
      <>
        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <span className="title is-4">Settings</span>
          <div>
            <AppLink
              className="button is-primary is-small is-pulled-right"
              href="/settings/template?id=new"
            >
              <span>Create template</span>
            </AppLink>
          </div>
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
              <li className={`is-capitalized has-text-weight-semibold`}>
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
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
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

        {(document_templates?.edges || [])?.length > 0 && (
          <>
            <div className="table-container">
              <table className="table is-fullwidth">
                <tbody className="templates-table">
                  <tr>
                    <td className="is-size-7">DOCUMENT TEMPLATES</td>
                    <td className="action pr-0"></td>
                  </tr>

                  {(document_templates?.edges || []).map(
                    ({ node: template }) => (
                      <tr key={`${template.id}-${Date.now()}`}>
                        <td className="template">
                          <TemplateDescription template={template} />
                        </td>
                        <td className="action is-vcentered pr-0">
                          <div className="buttons is-justify-content-end">
                            <button
                              className="button is-white"
                              onClick={toggle(template)}
                            >
                              <span
                                className={`icon is-medium ${template.active ? "has-text-success" : "has-text-grey"}`}
                              >
                                <i
                                  className={`fas fa-${template.active ? "toggle-on" : "toggle-off"} fa-lg`}
                                ></i>
                              </span>
                            </button>
                            <AppLink
                              className="button is-white"
                              href={`/settings/template?id=${template.id}`}
                            >
                              <span className="icon is-small">
                                <i className="fas fa-pen"></i>
                              </span>
                            </AppLink>
                            <button
                              className="button is-white"
                              onClick={() =>
                                confirmDeletion({
                                  label: "Delete Document template",
                                  identifier: template.id,
                                  onConfirm: remove(template.id),
                                })
                              }
                            >
                              <span className="icon is-small">
                                <i className="fas fa-trash"></i>
                              </span>
                            </button>
                          </div>
                        </td>
                      </tr>
                    ),
                  )}
                </tbody>
              </table>
            </div>

            <footer className="px-2 py-2 is-vcentered">
              <span className="is-size-7 has-text-weight-semibold">
                {(document_templates?.edges || []).length} results
              </span>

              <div className="buttons has-addons is-centered is-pulled-right">
                <button
                  className="button is-small"
                  onClick={() =>
                    setFilter({ ...filter, offset: filter.offset || 0 - 20 })
                  }
                  disabled={!document_templates?.page_info.has_previous_page}
                >
                  Previous
                </button>
                <button
                  className="button is-small"
                  onClick={() =>
                    setFilter({ ...filter, offset: filter.offset || 0 + 20 })
                  }
                  disabled={!document_templates?.page_info.has_next_page}
                >
                  Next
                </button>
              </div>
            </footer>
          </>
        )}

        {query.isFetched && (document_templates?.edges || [])?.length == 0 && (
          <div className="card my-6">
            <div className="card-content has-text-centered">
              <p>{`There aren't any results for that query.`}</p>
              <p>{`Create a new template`}</p>
            </div>
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
