import { GenerateAPIModal } from "@karrio/ui/modals/generate-api-dialog";
import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { useContext, useEffect, useRef, useState } from "react";
import { DashboardLayout } from "@/layouts/dashboard-layout";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { AppLink } from "@karrio/ui/components/app-link";
import { Loading } from "@karrio/ui/components/loader";
import { useAPIToken } from "@karrio/hooks/api-token";
import Head from "next/head";

export { getServerSideProps } from "@/context/main";


export default function ApiPage(pageProps: any) {
  const { references } = useAPIMetadata();

  const Component: React.FC = () => {
    const { setLoading } = useContext(Loading);
    const tokenInput = useRef<HTMLInputElement>(null);
    const [isRevealed, setIsRevealed] = useState<boolean>(false);
    const { query: { data: { token } = {}, ...query } } = useAPIToken();

    const copy = (_: React.MouseEvent) => {
      tokenInput.current?.select();
      document.execCommand("copy");
    };

    useEffect(() => { setLoading(query.isRefetching); }, [query.isRefetching]);

    return (
      <>

        <header className="px-0 pb-0 pt-4 is-flex is-justify-content-space-between">
          <span className="title is-4">Developers</span>
          <div></div>
        </header>

        <div className="tabs">
          <ul>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/developers" shallow={false} prefetch={false}>
                <span>Overview</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold is-active`}>
              <AppLink href="/developers/apikeys" shallow={false} prefetch={false}>
                <span>API Keys</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/developers/webhooks" shallow={false} prefetch={false}>
                <span>Webhooks</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/developers/events" shallow={false} prefetch={false}>
                <span>Events</span>
              </AppLink>
            </li>
            <li className={`is-capitalized has-text-weight-semibold`}>
              <AppLink href="/developers/logs" shallow={false} prefetch={false}>
                <span>Logs</span>
              </AppLink>
            </li>
          </ul>
        </div>

        {/* API Keys */}
        <div className="card p-3 mt-6">

          <div className="columns">
            <div className="column is-5 pr-2">
              <p className="subtitle is-6 py-1">Private Key</p>
              <p className="is-size-7 has-text-weight-semibold pr-6">
                <span>Use this key to authenticate your API calls. </span>
                <a
                  className="has-text-link"
                  href={`${references?.OPENAPI}/#section/Authentication`}
                  target="_blank"
                  rel="noreferrer">
                  Learn more
                </a>
              </p>
              <p className="is-size-7 pr-6"><strong>Warning:</strong> must be kept securely and never exposed to a client application.</p>
            </div>

            <div className="column is-5">
              <div className="field has-addons">
                <p className="control is-expanded">
                  <input className="input is-small"
                    type="text"
                    title={isRevealed ? "Click to Copy" : ""}
                    value={isRevealed ? token?.key : "key_......................."}
                    ref={tokenInput}
                    readOnly
                  />
                </p>
                <p className="control">
                  <button className="button is-small is-light px-4" title="Click to copy the token" onClick={copy} disabled={!isRevealed}>
                    <span className="icon is-small"><i className="fas fa-copy"></i></span>
                  </button>
                </p>
                <p className="control">
                  <button className="button is-small is-light px-4" title="Click to show or hide the token" onClick={() => setIsRevealed(!isRevealed)}>
                    {isRevealed ?
                      <span className="icon is-small"><i className="fas fa-eye-slash"></i></span> :
                      <span className="icon is-small"><i className="fas fa-eye"></i></span>}
                  </button>
                </p>
                <div className="control">
                  <GenerateAPIModal>
                    <button className="button is-primary is-light is-small px-4" title="Generate a new token">
                      <span className="icon is-small"><i className="fas fa-redo"></i></span>
                    </button>
                  </GenerateAPIModal>
                </div>
              </div>

              <p className="is-size-7 has-text-weight-bold pr-6">
                <span>Click </span>
                <span className="icon is-small has-text-link"><i className="fas fa-redo"></i></span>
                <span> to revoke old keys and generate a new one.</span>
              </p>
            </div>

            <div className="column is-2"></div>
          </div>
        </div>

      </>
    );
  };

  return AuthenticatedPage((
    <DashboardLayout showModeIndicator={true}>
      <Head><title>{`API Keys - ${references?.APP_NAME}`}</title></Head>
      <Component />
    </DashboardLayout>
  ), pageProps);
}
