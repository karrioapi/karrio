import { useDocumentTemplateMutation, useDocumentTemplates } from "@/context/document-template";
import TemplateDescription from "@/components/descriptions/template-description";
import ConfirmModal, { ConfirmModalContext } from "@/components/confirm-modal";
import AuthenticatedPage from "@/layouts/authenticated-page";
import DashboardLayout from "@/layouts/dashboard-layout";
import AppLink from "@/components/app-link";
import { useContext } from "react";
import Head from "next/head";
import React from "react";
import { DocumentTemplateType, NotificationType } from "@/lib/types";
import { Notify } from "@/components/notifier";

export { getServerSideProps } from "@/lib/data-fetching";


export default function TemplatesPage(pageProps: any) {
  const Component: React.FC<any> = () => {
    const { notify } = useContext(Notify);
    const mutation = useDocumentTemplateMutation();
    const { confirm: confirmDeletion } = useContext(ConfirmModalContext);
    const { query: { data: { document_templates } = {}, ...query }, filter, setFilter } = useDocumentTemplates();

    const remove = (id: string) => async () => {
      await mutation.deleteDocumentTemplate.mutateAsync({ id });
    };
    const toggle = ({ active, id }: DocumentTemplateType) => async () => {
      try {
        await mutation.updateDocumentTemplate.mutateAsync({ id, active: !active });
        notify({
          type: NotificationType.success,
          message: `template ${!active ? 'enabled' : 'disabled'}!`
        });
      } catch (message: any) {
        notify({ type: NotificationType.error, message });
      }
    };

    return (
      <>

        <header className="px-0 py-6">
          <span className="title is-4">Templates</span>
          <AppLink className="button is-primary is-small is-pulled-right" href="/settings/template?id=new">
            <span>Create template</span>
          </AppLink>
        </header>

        {((document_templates?.edges || [])?.length > 0) && <div className="table-container">
          <table className="table is-fullwidth">

            <tbody className="templates-table">
              <tr>
                <td className="is-size-7">DOCUMENT TEMPLATES</td>
                <td className="action"></td>
              </tr>

              {(document_templates?.edges || []).map(({ node: template }) => (

                <tr key={`${template.id}-${Date.now()}`}>
                  <td className="template">
                    <TemplateDescription template={template} />
                  </td>
                  <td className="action is-vcentered pr-0">
                    <div className="buttons is-justify-content-end">
                      <button className="button is-white" onClick={toggle(template)}>
                        <span className={`icon is-medium ${template.active ? 'has-text-success' : 'has-text-grey'}`}>
                          <i className={`fas fa-${template.active ? 'toggle-on' : 'toggle-off'} fa-lg`}></i>
                        </span>
                      </button>
                      <AppLink className="button is-white" href={`/settings/template?id=${template.id}`}>
                        <span className="icon is-small">
                          <i className="fas fa-pen"></i>
                        </span>
                      </AppLink>
                      <button className="button is-white" onClick={() => confirmDeletion({
                        label: "Delete Document template",
                        identifier: template.id,
                        onConfirm: remove(template.id),
                      })}>
                        <span className="icon is-small">
                          <i className="fas fa-trash"></i>
                        </span>
                      </button>
                    </div>
                  </td>
                </tr>

              ))}
            </tbody>

          </table>

          <footer className="px-2 py-2 is-vcentered">
            <span className="is-size-7 has-text-weight-semibold">
              {(document_templates?.edges || []).length} results
            </span>

            <div className="buttons has-addons is-centered is-pulled-right">
              <button className="button is-small"
                onClick={() => setFilter({ ...filter, offset: (filter.offset || 0 - 20) })}
                disabled={!document_templates?.page_info.has_previous_page}>
                Previous
              </button>
              <button className="button is-small"
                onClick={() => setFilter({ ...filter, offset: (filter.offset || 0 + 20) })}
                disabled={!document_templates?.page_info.has_next_page}>
                Next
              </button>
            </div>
          </footer>

        </div>}

        {(query.isFetched && (document_templates?.edges || [])?.length == 0) && <div className="card my-6">

          <div className="card-content has-text-centered">
            <p>No template has been added yet.</p>
            <p>Use the <strong>Create Template</strong> button above to add</p>
          </div>

        </div>}

      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout>
      <Head><title>{`Document Templates - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>
      <ConfirmModal>

        <Component />

      </ConfirmModal>
    </DashboardLayout>
  ), pageProps);
}
