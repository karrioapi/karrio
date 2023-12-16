import { AddressEditModal, AddressEditContext } from "@karrio/ui/modals/address-edit-modal";
import { useAddressTemplateMutation, useAddressTemplates } from "@karrio/hooks/address";
import { GoogleGeocodingScript } from "@karrio/ui/components/google-geocoding-script";
import { ConfirmModal, ConfirmModalContext } from "@karrio/ui/modals/confirm-modal";
import { AddressDescription } from "@karrio/ui/components/address-description";
import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { DashboardLayout } from "@/layouts/dashboard-layout";
import { AppLink } from "@karrio/ui/components/app-link";
import { Loading } from "@karrio/ui/components/loader";
import React, { useContext, useEffect } from "react";
import { useRouter } from "next/dist/client/router";
import { isNoneOrEmpty } from "@karrio/lib";
import Head from "next/head";

export { getServerSideProps } from '@/context/main';


export default function AddressPage(pageProps: any) {
  const { APP_NAME, MULTI_ORGANIZATIONS } = (pageProps as any).metadata || {};

  const Component: React.FC = () => {
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

        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <span className="title is-4">Settings</span>
          <div></div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/settings/account" shallow={false} prefetch={false}>
                <span>Account</span>
              </AppLink>
            </li>
            {MULTI_ORGANIZATIONS && <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/settings/organization" shallow={false} prefetch={false}>
                <span>Organization</span>
              </AppLink>
            </li>}
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
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

        {((query?.data?.address_templates?.edges || []).length > 0) &&
          <div className="table-container">
            <table className="table is-fullwidth">
              <tbody className="templates-table">

                <tr>
                  <td className="is-size-7" colSpan={2}>ADDRESS TEMPLATES</td>
                  <td className="action pr-0">
                    <button className="button is-primary is-small is-pulled-right" onClick={() => editAddress()}>
                      <span>Create address</span>
                    </button>
                  </td>
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
      <Head><title>{`Addresses Settings - ${APP_NAME}`}</title></Head>
      <ConfirmModal>
        <AddressEditModal>

          <Component />

        </AddressEditModal>
      </ConfirmModal>
    </DashboardLayout>
  ), pageProps);
}
