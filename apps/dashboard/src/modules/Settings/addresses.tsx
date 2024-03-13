import { formatAddressLocationShort, formatAddressShort, getURLSearchParams, isNoneOrEmpty } from "@karrio/lib";
import { AddressEditModal, AddressEditContext } from "@karrio/ui/modals/address-edit-modal";
import { useAddressTemplateMutation, useAddressTemplates } from "@karrio/hooks/address";
import { GoogleGeocodingScript } from "@karrio/ui/components/google-geocoding-script";
import { ConfirmModal, ConfirmModalContext } from "@karrio/ui/modals/confirm-modal";
import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { DashboardLayout } from "@/layouts/dashboard-layout";
import { AppLink } from "@karrio/ui/components/app-link";
import { Loading } from "@karrio/ui/components/loader";
import React, { useContext, useEffect } from "react";
import { useRouter } from "next/dist/client/router";
import { AddressType } from "@karrio/types";
import Head from "next/head";

export { getServerSideProps } from '@/context/main';


export default function AddressPage(pageProps: any) {
  const { APP_NAME, MULTI_ORGANIZATIONS } = (pageProps as any).metadata || {};

  const Component: React.FC = () => {
    const router = useRouter();
    const { setLoading } = useContext(Loading);
    const { confirm } = useContext(ConfirmModalContext);
    const { editAddress } = useContext(AddressEditContext);
    const { deleteAddressTemplate } = useAddressTemplateMutation();
    const [initialized, setInitialized] = React.useState(false);
    const { query: { data: { address_templates } = {}, ...query }, filter, setFilter } = useAddressTemplates({
      setVariablesToURL: true,
    });

    const remove = (id: string) => async () => {
      await deleteAddressTemplate.mutateAsync({ id });
    };
    const updateFilter = (extra: Partial<any> = {}) => {
      const query = {
        ...filter,
        ...getURLSearchParams(),
        ...extra
      };

      setFilter(query);
    };

    useEffect(() => { updateFilter(); }, [router.query]);
    useEffect(() => { setLoading(query.isFetching); }, [query.isFetching]);
    useEffect(() => {
      if (query.isFetched && !initialized && !isNoneOrEmpty(router.query.modal)) {
        const templates = address_templates?.edges || [];
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
          <div>
            <button className="button is-primary is-small is-pulled-right" onClick={() => editAddress()}>
              <span>Create address</span>
            </button>
          </div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold`}>
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

        {((address_templates?.edges || []).length > 0) && <>
          <div className="table-container">
            <table className="table is-fullwidth">
              <tbody className="address-templates-table">

                <tr>
                  <td className="template is-size-7">LABEL</td>
                  <td className="address is-size-7">ADDRESS</td>
                  <td className="email is-size-7">EMAIL</td>
                  <td className="default is-size-7"></td>
                  <td className="action pr-0"></td>
                </tr>

                {(address_templates?.edges || []).map(({ node: template }) => (

                  <tr key={`${template.id}-${Date.now()}`}>
                    <td className="template is-vcentered is-size-7 has-text-weight-bold text-ellipsis">
                      <span className="text-ellipsis" title={template.label}>{template.label}</span>
                    </td>
                    <td className="address is-vcentered is-size-7 has-text-weight-bold has-text-grey text-ellipsis">
                      <span className="text-ellipsis" title={formatAddressShort(template.address as AddressType)}>
                        {formatAddressShort(template.address as AddressType)}
                      </span>
                      <br />
                      <span className="has-text-weight-medium">
                        {formatAddressLocationShort(template.address as AddressType)}
                      </span>
                    </td>
                    <td className="email is-vcentered is-size-7 has-text-weight-bold text-ellipsis">
                      <span className="text-ellipsis" title={template.address.email || ''}>{template.address.email}</span>
                    </td>
                    <td className="default is-vcentered has-text-right">
                      {template.is_default && <span className="is-size-7 has-text-weight-semibold">
                        <span className="icon has-text-success"><i className="fas fa-check"></i></span> default
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
          </div>

          <footer className="px-2 py-2 is-vcentered">
            <span className="is-size-7 has-text-weight-semibold">
              {(address_templates?.edges || []).length} results
            </span>

            <div className="buttons has-addons is-centered is-pulled-right">
              <button className="button is-small"
                onClick={() => updateFilter({ offset: (filter.offset as number - 25) })}
                disabled={filter.offset == 0}>
                Previous
              </button>
              <button className="button is-small"
                onClick={() => updateFilter({ offset: (filter.offset as number + 25) })}
                disabled={!address_templates?.page_info.has_next_page}>
                Next
              </button>
            </div>
          </footer>
        </>}

        {(query.isFetched && (address_templates?.edges || []).length == 0) &&
          <div className="card my-6">

            <div className="card-content has-text-centered">
              <p>{`There aren't any results for that query.`}</p>
              <p>{`Create a new address`}</p>
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
