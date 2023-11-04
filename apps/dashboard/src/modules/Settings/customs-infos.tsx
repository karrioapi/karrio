import CustomsInfoEditModal, { CustomsInfoEditContext } from "@/components/customs-info-edit-modal";
import { useCustomsTemplateMutation, useCustomsTemplates } from "@/context/customs";
import CustomsInfoDescription from "@/components/descriptions/customs-info-description";
import ConfirmModal, { ConfirmModalContext } from "@/components/confirm-modal";
import AuthenticatedPage from "@/layouts/authenticated-page";
import DashboardLayout from "@/layouts/dashboard-layout";
import { useRouter } from "next/dist/client/router";
import { useContext, useEffect } from "react";
import { isNoneOrEmpty } from "@/lib/helper";
import { CustomsType } from "@/lib/types";
import Head from "next/head";
import React from "react";

export { getServerSideProps } from "@/lib/data-fetching";


export default function CustomsInfoPage(pageProps: any) {
  const Component: React.FC<any> = () => {
    const router = useRouter();
    const { confirm: confirmDeletion } = useContext(ConfirmModalContext);
    const { editCustomsInfo } = useContext(CustomsInfoEditContext);
    const mutation = useCustomsTemplateMutation();
    const { query, setFilter, filter } = useCustomsTemplates();
    const [initialized, setInitialized] = React.useState(false);

    const remove = (id: string) => async () => {
      await mutation.deleteCustomsTemplate.mutateAsync({ id });
    };

    useEffect(() => {
      if (!initialized && query.isFetched && !isNoneOrEmpty(router.query.modal)) {
        const customsTemplate: any = (query.data?.customs_templates?.edges || [])
          .find(c => c.node.id === router.query.modal);
        if (customsTemplate || router.query.modal === 'new') {
          editCustomsInfo({ customsTemplate });
        }
        setInitialized(true);
      }
    }, [router.query.modal, query.isFetched]);

    return (
      <>

        <header className="px-0 py-6">
          <span className="title is-4">Customs</span>
          <button className="button is-primary is-small is-pulled-right" onClick={() => editCustomsInfo()}>
            <span>Create customs info</span>
          </button>
        </header>

        {((query.data?.customs_templates.edges || []).length > 0) && <div className="table-container">
          <table className="table is-fullwidth">

            <tbody className="templates-table">
              <tr>
                <td className="is-size-7" colSpan={2}>CUSTOMS INFO TEMPLATES</td>
                <td className="action"></td>
              </tr>

              {(query.data?.customs_templates.edges || []).map(({ node: template }) => (

                <tr key={`${template.id}-${Date.now()}`}>
                  <td className="template">
                    <p className="is-subtitle is-size-6 my-1 has-text-weight-semibold">{template.label}</p>
                    <CustomsInfoDescription customs={template.customs as CustomsType} />
                  </td>
                  <td className="default is-vcentered">
                    {template.is_default && <span className="is-size-7 has-text-weight-semibold">
                      <span className="icon has-text-success"><i className="fas fa-check"></i></span> Default customs
                    </span>}
                  </td>
                  <td className="action is-vcentered pr-0">
                    <div className="buttons is-justify-content-end">
                      <button className="button is-white" onClick={() => editCustomsInfo({
                        customsTemplate: template as any,
                      })}>
                        <span className="icon is-small">
                          <i className="fas fa-pen"></i>
                        </span>
                      </button>
                      <button className="button is-white" onClick={() => confirmDeletion({
                        label: "Delete Customs info template",
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
              {(query.data?.customs_templates.edges || []).length} results
            </span>

            <div className="buttons has-addons is-centered is-pulled-right">
              <button className="button is-small"
                onClick={() => setFilter({ ...filter, offset: (filter.offset || 0) - 20 })}
                disabled={!query.data?.customs_templates.page_info.has_previous_page}>
                <span>Previous</span>
              </button>
              <button className="button is-small"
                onClick={() => setFilter({ ...filter, offset: (filter.offset || 0) + 20 })}
                disabled={!query.data?.customs_templates.page_info.has_next_page}>
                <span>Next</span>
              </button>
            </div>
          </footer>

        </div>}

        {(query.isFetched && (query.data?.customs_templates.edges || []).length == 0) &&
          <div className="card my-6">
            <div className="card-content has-text-centered">
              <p>No customs info template has been added yet.</p>
              <p>Use the <strong>New Customs Info</strong> button above to add</p>
            </div>
          </div>}

      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout>
      <Head><title>{`Customs Templates - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>
      <ConfirmModal>
        <CustomsInfoEditModal>

          <Component />

        </CustomsInfoEditModal>
      </ConfirmModal>
    </DashboardLayout>
  ), pageProps);
}
