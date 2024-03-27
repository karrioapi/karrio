import { formatAddressLocationShort, formatAddressShort, formatCarrierSlug, formatDateTime, isNone, preventPropagation, url$ } from '@karrio/lib';
import { useSystemCarrierConnections } from '@karrio/hooks/admin/connections';
import { useCarrierConnections } from '@karrio/hooks/user-connection';
import { CarrierImage } from '@karrio/ui/components/carrier-image';
import { AuthenticatedPage } from '@/layouts/authenticated-page';
import { DashboardLayout } from '@/layouts/dashboard-layout';
import { useAPIMetadata } from '@karrio/hooks/api-metadata';
import { MenuComponent } from '@karrio/ui/components/menu';
import { AddressType, ManifestType } from '@karrio/types';
import { useLoader } from '@karrio/ui/components/loader';
import { AppLink } from '@karrio/ui/components/app-link';
import { ModalProvider } from '@karrio/ui/modals/modal';
import { useManifests } from '@karrio/hooks/manifests';
import { bundleContexts } from '@karrio/hooks/utils';
import { Spinner } from '@karrio/ui/components';
import { useRouter } from 'next/router';
import Head from 'next/head';
import React from 'react';

export { getServerSideProps } from "@/context/main";

const ContextProviders = bundleContexts([
  ModalProvider,
]);

export default function Page(pageProps: any) {
  const Component: React.FC = () => {

    // General context data         -----------------------------------------------------------
    //#region

    const router = useRouter();
    const loader = useLoader();
    const { metadata } = useAPIMetadata();
    const [allChecked, setAllChecked] = React.useState(false);
    const [selection, setSelection] = React.useState<string[]>([]);
    const { query: { data: { user_connections } = {} } } = useCarrierConnections();
    const { query: { data: { system_connections } = {} } } = useSystemCarrierConnections();
    const { query: { data: { manifests } = {}, ...query }, filter, setFilter } = useManifests({
      preloadNextPage: true,
    });

    //#endregion

    // Helper functions            -----------------------------------------------------------
    //#region

    const updateFilter = (extra: Partial<any> = {}) => {
      const query = {
        ...filter,
        ...extra,
      };

      setFilter(query);
    };
    const updatedSelection = (selectedManifests: string[], current: typeof manifests) => {
      const manifest_ids = (current?.edges || []).map(({ node: manifest }) => manifest.id);
      const selection = selectedManifests.filter(id => manifest_ids.includes(id));
      const selected = selection.length > 0 && selection.length === (manifest_ids || []).length;
      setAllChecked(selected);
      if (selectedManifests.filter(id => !manifest_ids.includes(id)).length > 0) {
        setSelection(selection);
      }
    };
    const handleSelection = (e: React.ChangeEvent) => {
      const { checked, name } = e.target as HTMLInputElement;
      if (name === "all") {
        setSelection(!checked ? [] : (manifests?.edges || []).map(({ node: { id } }) => id));
      } else {
        setSelection(checked ? [...selection, name] : selection.filter(id => id !== name));
      }
    };
    const getCarrier = (manifest: ManifestType) => (
      user_connections?.find(_ => _.id === manifest?.meta?.carrier || _.carrier_id === manifest?.carrier_id)
      || system_connections?.find(_ => _.id === manifest?.meta?.carrier || _.carrier_id === manifest?.carrier_id)
    );

    //#endregion

    React.useEffect(() => { updateFilter(); }, [router.query]);
    React.useEffect(() => { loader.setLoading(query.isLoading); }, [query.isLoading]);
    React.useEffect(() => { updatedSelection(selection, manifests); }, [selection, manifests]);

    return (
      <>

        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <div className="title is-4">
            <span className="title is-4">Manifests</span>
            <span className="tag is-warning is-size-7 has-text-weight-bold mx-2">BETA</span>
          </div>
          <div></div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
              <a>Ready</a>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/manifests/create_manifests"><span>Pending Shipments</span></AppLink>
            </li>
          </ul>
        </div>

        {query.isLoading && <Spinner />}

        {(query.isLoading === false && (manifests?.edges || []).length > 0) && <>
          <div className="table-container">
            <table className="manifests-table table is-fullwidth">

              <tbody>
                <tr>
                  <td className="selector has-text-centered p-0 control is-vcentered" onClick={preventPropagation}>
                    <label className="checkbox p-2">
                      <input
                        name="all"
                        type="checkbox"
                        onChange={handleSelection}
                        checked={allChecked}
                      />
                    </label>
                  </td>

                  {selection.length > 0 && <td className="p-1 is-vcentered" colSpan={6}>
                    <div className="buttons has-addons">
                      <a
                        href={url$`${metadata.HOST}/documents/manifests/manifest.pdf?manifests=${selection.join(',')}`}
                        className={`button is-small is-default px-3`} target="_blank" rel="noreferrer">
                        <span className="has-text-weight-semibold">Print Manifests</span>
                      </a>
                    </div>
                  </td>}

                  {selection.length === 0 && <>
                    <td className="carrier is-size-7 is-vcentered">CARRIER</td>
                    <td className="address is-size-7 is-vcentered">ADDRESS</td>
                    <td className="reference is-size-7 is-vcentered">REFERENCE</td>
                    <td className="date is-size-7 is-vcentered">DATE</td>
                    <td className="action"></td>
                  </>}
                </tr>

                {(manifests?.edges || []).map(({ node: manifest }) => (
                  <tr key={manifest.id} className="items">
                    <td className="selector is-clickable has-text-centered is-vcentered p-0">
                      <label className="checkbox py-3 px-2">
                        <input
                          type="checkbox"
                          name={manifest.id}
                          onChange={handleSelection}
                          checked={selection.includes(manifest.id)}
                        />
                      </label>
                    </td>
                    <td className="carrier is-vcentered py-1 px-0 is-size-7 has-text-weight-bold has-text-grey" title={manifest.carrier_name}>
                      <div className="icon-text">
                        <CarrierImage
                          carrier_name={manifest.meta?.carrier || manifest.carrier_name || formatCarrierSlug(metadata.APP_NAME)}
                          containerClassName="mt-1 ml-1 mr-2" height={28} width={28}
                          text_color={getCarrier(manifest)?.config?.text_color}
                          background={getCarrier(manifest)?.config?.brand_color}
                        />
                        <div className="text-ellipsis" style={{ maxWidth: '250px', lineHeight: '16px' }}>
                          <span className="has-text-weight-bold">{manifest.id}</span>
                          <br />
                          <span className="text-ellipsis has-text-info">
                            {manifest.shipment_identifiers[0] || ' - '}
                          </span>
                        </div>
                      </div>
                    </td>
                    <td className="address is-vcentered is-size-7 has-text-weight-bold has-text-grey is-relative" >
                      <div className="p-2" style={{ position: 'absolute', maxWidth: '100%', top: 0, left: 0 }}>
                        <p className="text-ellipsis" title={formatAddressShort(manifest.address as AddressType)}>
                          {formatAddressShort(manifest.address as AddressType)}
                        </p>
                        <p className="has-text-weight-medium">{formatAddressLocationShort(manifest.address as AddressType)}</p>
                      </div>
                    </td>
                    <td className="reference is-vcentered is-size-7 has-text-weight-bold has-text-grey text-ellipsis" >
                      <span>{manifest.reference || ''}</span>
                    </td>
                    <td className="date is-vcentered px-1" >
                      <p className="is-size-7 has-text-weight-semibold has-text-grey">
                        {formatDateTime(manifest.created_at)}
                      </p>
                    </td>
                    <td className="action is-vcentered px-0">
                      <div className="buttons has-addons is-centered">
                        <MenuComponent.Menu
                          trigger={
                            <button className="button is-white">
                              <span className="icon is-small">
                                <i className="fas fa-ellipsis-h"></i>
                              </span>
                            </button>
                          }
                        >
                          <a className={`dropdown-item ${isNone(manifest.manifest_url) ? 'is-static' : ''}`}
                            href={url$`${metadata.HOST}/${manifest.manifest_url}`}
                            target="_blank"
                            rel="noreferrer"
                          >
                            <span>Print Manifest</span>
                          </a>
                        </MenuComponent.Menu>
                      </div>
                    </td>
                  </tr>
                ))}

              </tbody>

            </table>
          </div>

          <div className="px-2 py-2 is-vcentered">
            <span className="is-size-7 has-text-weight-semibold">
              {(manifests?.edges || []).length} results
            </span>

            <div className="buttons has-addons is-centered is-pulled-right">
              <button className="button is-small"
                onClick={() => updateFilter({ offset: (filter.offset as number - 20) })}
                disabled={filter.offset == 0}>
                Previous
              </button>
              <button className="button is-small"
                onClick={() => updateFilter({ offset: (filter.offset as number + 20) })}
                disabled={!manifests?.page_info.has_next_page}>
                Next
              </button>
            </div>
          </div>
        </>}

        {(query.isLoading === false && (manifests?.edges || []).length == 0) && <>
          <div className="card my-6">

            <div className="card-content has-text-centered">
              <p>No manifest found.</p>
            </div>

          </div>
        </>}

      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout showModeIndicator={true}>
      <Head><title>{`Manifests - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>

      <ContextProviders>
        <Component />
      </ContextProviders>

    </DashboardLayout>
  ), pageProps)
}
