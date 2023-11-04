import { useAddressTemplateMutation, useAddressTemplates } from "@/context/address";
import AddressEditModal, { AddressEditContext } from "@/components/address-edit-modal";
import ConfirmModal, { ConfirmModalContext } from "@/components/confirm-modal";
import AddressDescription from "@/components/descriptions/address-description";
import GoogleGeocodingScript from "@/components/google-geocoding-script";
import AuthenticatedPage from "@/layouts/authenticated-page";
import DashboardLayout from "@/layouts/dashboard-layout";
import React, { useContext, useEffect } from "react";
import { useRouter } from "next/dist/client/router";
import { Loading } from "@/components/loader";
import { isNoneOrEmpty } from "@/lib/helper";
import Head from "next/head";

export { getServerSideProps } from '@/lib/data-fetching';


export default function AddressPage(pageProps: any) {
  const Component: React.FC<any> = () => {
    const router = useRouter();
    const { query } = useAddressTemplates();
    const { setLoading } = useContext(Loading);
    const { confirm } = useContext(ConfirmModalContext);
    const { editAddress } = useContext(AddressEditContext);
    const { deleteAddressTemplate } = useAddressTemplateMutation();
    const [initialized, setInitialized] = React.useState(false);

    const remove = (id: string) => async () => {
      await deleteAddressTemplate.mutateAsync({ id });
    };

    useEffect(() => { setLoading(query.isFetching); });
    useEffect(() => {
      if (query.isFetched && !initialized && !isNoneOrEmpty(router.query.modal)) {
        const templates = query.data?.address_templates?.edges || [];
        const addressTemplate: any = templates
          .find(c => c.node.id === router.query.modal)?.node;
        if (addressTemplate || router.query.modal === 'new') {
          editAddress({ addressTemplate });
        }
        setInitialized(true);
      }
    }, [router.query.modal, query.isFetched]);

    return (
      <>

        <header className="px-0 py-6">
          <span className="title is-4">Addresses</span>
          <button className="button is-primary is-small is-pulled-right" onClick={() => editAddress()}>
            <span>Create address</span>
          </button>
        </header>

        {((query?.data?.address_templates?.edges || []).length > 0) &&
          <div className="table-container">
            <table className="table is-fullwidth">
              <tbody className="templates-table">

                <tr>
                  <td className="is-size-7" colSpan={2}>ADDRESS TEMPLATES</td>
                  <td className="action"></td>
                </tr>

                {query!.data!.address_templates!.edges.map(({ node: template }) => (

                  <tr key={`${template.id}-${Date.now()}`}>
                    <td className="template">
                      <p className="is-subtitle is-size-6 my-1 has-text-weight-semibold">{template.label}</p>
                      <AddressDescription address={template.address as any} />
                    </td>
                    <td className="default is-vcentered">
                      {template.is_default && <span className="is-size-7 has-text-weight-semibold">
                        <span className="icon has-text-success"><i className="fas fa-check"></i></span> Default shipper address
                      </span>}
                    </td>
                    <td className="action is-vcentered pr-0">
                      <div className="buttons is-justify-content-end">
                        <button className="button is-white" onClick={() => editAddress({
                          addressTemplate: template as any,
                        })}>
                          <span className="icon is-small">
                            <i className="fas fa-pen"></i>
                          </span>
                        </button>
                        <button className="button is-white" onClick={() => confirm({
                          label: "Delete Address template",
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
              <span className="is-size-7 has-text-weight-semibold">{query!.data!.address_templates!.edges.length} results</span>

              <div className="buttons has-addons is-centered is-pulled-right">
              </div>
            </footer>

          </div>}

        {(query.isFetched && (query?.data?.address_templates?.edges || []).length == 0) &&
          <div className="card my-6">

            <div className="card-content has-text-centered">
              <p>No address has been added yet.</p>
              <p>Use the <strong>New Address</strong> button above to add</p>
            </div>

          </div>}

      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout>
      <GoogleGeocodingScript />
      <Head><title>{`Address Templates - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>
      <ConfirmModal>
        <AddressEditModal>

          <Component />

        </AddressEditModal>
      </ConfirmModal>
    </DashboardLayout>
  ), pageProps);
}
