import { ParcelEditModal, ParcelEditContext } from "@karrio/ui/modals/parcel-edit-modal";
import { useParcelTemplateMutation, useParcelTemplates } from "@karrio/hooks/parcel";
import { ConfirmModal, ConfirmModalContext } from "@karrio/ui/modals/confirm-modal";
import { ParcelDescription } from "@karrio/ui/components/parcel-description";
import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { DashboardLayout } from "@/layouts/dashboard-layout";
import { Loading } from "@karrio/ui/components/loader";
import { useRouter } from "next/dist/client/router";
import { useContext, useEffect } from "react";
import { isNoneOrEmpty } from "@karrio/lib";
import Head from "next/head";
import React from "react";

export { getServerSideProps } from "@/context/main";


export default function ParcelsPage(pageProps: any) {
  const Component: React.FC = () => {
    const router = useRouter();
    const { setLoading } = useContext(Loading);
    const mutation = useParcelTemplateMutation();
    const { editParcel } = useContext(ParcelEditContext);
    const [initialized, setInitialized] = React.useState(false);
    const { confirm: confirmDeletion } = useContext(ConfirmModalContext);
    const { query: { data: { parcel_templates } = {}, ...query }, filter, setFilter } = useParcelTemplates();

    const remove = (id: string) => async () => {
      await mutation.deleteParcelTemplate.mutateAsync({ id });
    };

    useEffect(() => { setLoading(query.isFetching); }, [query.isFetching]);
    useEffect(() => {
      if (query.isFetched && !initialized && !isNoneOrEmpty(router.query.modal)) {
        const parcelTemplate = (parcel_templates?.edges || [])
          .find(c => c.node.id === router.query.modal)
          ?.node;
        if (parcelTemplate || router.query.modal === 'new') {
          editParcel({ parcelTemplate } as any);
        }
        setInitialized(true);
      }
      query.isFetched && setInitialized(true);
    }, [router.query.modal, query.isFetched]);

    return (
      <>

        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <span className="title is-4">Parcels</span>
          <div>
            <button className="button is-primary is-small is-pulled-right" onClick={() => editParcel()}>
              <span>Create parcel</span>
            </button>
          </div>
        </header>

        {((parcel_templates?.edges || []).length > 0) && <div className="table-container">
          <table className="table is-fullwidth">

            <tbody className="templates-table">
              <tr>
                <td className="is-size-7" colSpan={2}>PARCEL TEMPLATES</td>
                <td className="action"></td>
              </tr>

              {(parcel_templates?.edges || []).map(({ node: template }) => (

                <tr key={`${template.id}-${Date.now()}`}>
                  <td className="template">
                    <p className="is-subtitle is-size-6 my-1 has-text-weight-semibold">{template.label}</p>
                    <ParcelDescription parcel={template.parcel as any} />
                  </td>
                  <td className="default is-vcentered">
                    {template.is_default && <span className="is-size-7 has-text-weight-semibold">
                      <span className="icon has-text-success"><i className="fas fa-check"></i></span> Default shipping parcel
                    </span>}
                  </td>
                  <td className="action is-vcentered pr-0">
                    <div className="buttons is-justify-content-end">
                      <button className="button is-white" onClick={() => editParcel({
                        parcelTemplate: template as any
                      })}>
                        <span className="icon is-small">
                          <i className="fas fa-pen"></i>
                        </span>
                      </button>
                      <button className="button is-white" onClick={() => confirmDeletion({
                        label: "Delete Parcel template",
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
            <span className="is-size-7 has-text-weight-semibold">{(parcel_templates?.edges || []).length} results</span>

            <div className="buttons has-addons is-centered is-pulled-right">
              <button className="button is-small"
                onClick={() => setFilter({ ...filter, offset: (filter.offset || 0 - 20) })}
                disabled={filter.offset == 0}>
                Previous
              </button>
              <button className="button is-small"
                onClick={() => setFilter({ ...filter, offset: (filter.offset || 0 + 20) })}
                disabled={!parcel_templates?.page_info.has_next_page}>
                Next
              </button>
            </div>
          </footer>

        </div>}

        {(query.isFetched && (parcel_templates?.edges || [])?.length == 0) &&
          <div className="card my-6">

            <div className="card-content has-text-centered">
              <p>No parcel has been added yet.</p>
              <p>Use the <strong>New Parcel</strong> button above to add</p>
            </div>

          </div>}

      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout>
      <Head><title>{`Parcel Templates - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>
      <ConfirmModal>
        <ParcelEditModal>

          <Component />

        </ParcelEditModal>
      </ConfirmModal>
    </DashboardLayout>
  ), pageProps);
}
