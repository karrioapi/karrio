import { AuthenticatedPage } from "@/layouts/authenticated-page";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { Switch } from "@karrio/ui/components/switch";
import { AdminLayout } from "@/layouts/admin-layout";
import getConfig from 'next/config';
import { url$ } from "@karrio/lib";
import Head from "next/head";

export { getServerSideProps } from "@/context/main";

const { publicRuntimeConfig } = getConfig();


export default function Page(pageProps: any) {
    const { APP_NAME } = (pageProps as any).metadata || {};

    const Component: React.FC = () => {
        const { metadata } = useAPIMetadata();

        return (
            <>
                <header className="px-0 pb-5 pt-1 mb-1">
                    <span className="title is-4 has-text-weight-bold">Platform details</span>
                </header>

                {/* Platfrom config */}
                <div className="card px-0">

                    <header className="px-3 mt-3 is-flex is-justify-content-space-between">
                        <span className="is-title is-size-6 has-text-weight-bold is-vcentered my-2">Platform</span>
                        <div className="is-vcentered">
                            <button type="button" className="button is-small is-white" disabled>
                                <span className="icon is-small"><i className="fas fa-pen"></i></span>
                            </button>
                        </div>
                    </header>

                    <hr className='my-1' style={{ height: '1px' }} />

                    <div className="p-3">

                        <p className="is-size-7 my-1 has-text-weight-bold">Platform name</p>
                        <p className="is-size-7 my-1 has-text-weight-semibold has-text-grey">{metadata?.APP_NAME}</p>

                    </div>

                    <hr className='my-1 mx-3' style={{ height: '1px' }} />

                    <div className="p-3">

                        <p className="is-size-7 my-1 has-text-weight-bold">API hostname</p>
                        <p className="is-size-7 my-1 has-text-weight-semibold has-text-grey">
                            {url$`${metadata?.HOST}`.replace('http://', '').replace('https://', '')}
                        </p>

                    </div>

                    <hr className='my-1 mx-3' style={{ height: '1px' }} />

                    <div className="p-3">

                        <p className="is-size-7 my-1 has-text-weight-bold">Dashboard hostname</p>
                        <p className="is-size-7 my-1 has-text-weight-semibold has-text-grey">{location.host}</p>

                    </div>

                </div>

                <div className="p-4"></div>

                {/* Feature flags */}
                <div className="card px-0 py-3">

                    <header className="px-3 is-flex is-justify-content-space-between">
                        <span className="is-title is-size-6 has-text-weight-bold is-vcentered my-2">Feature flags</span>
                        <div className="is-vcentered"></div>
                    </header>

                    <hr className='my-1' style={{ height: '1px' }} />

                    <div className="p-3">

                        <div className="is-flex is-justify-content-space-between">
                            <div>
                                <label className="label">ALLOW_SIGNUP</label>
                                <p className="help">Allow user signup</p>
                            </div>
                            <div>
                                <Switch checked={true} />
                            </div>
                        </div>

                        <hr className='my-1' style={{ height: '1px' }} />

                        <div className="is-flex is-justify-content-space-between">
                            <div>
                                <label className="label">ALLOW_ADMIN_APPROVED_SIGNUP</label>
                                <p className="help">user signup will require admin approval</p>
                            </div>
                            <div>
                                <Switch checked={true} />
                            </div>
                        </div>

                        <hr className='my-1' style={{ height: '1px' }} />

                        <div className="is-flex is-justify-content-space-between">
                            <div>
                                <label className="label">AUDIT_LOGGING</label>
                                <p className="help">Toggle audit logging functionality</p>
                            </div>
                            <div>
                                <Switch checked={false} disabled />
                            </div>
                        </div>

                        <hr className='my-1' style={{ height: '1px' }} />

                        <div className="is-flex is-justify-content-space-between">
                            <div>
                                <label className="label">APPS_MANAGEMENT</label>
                                <p className="help">Enable apps</p>
                            </div>
                            <div>
                                <Switch checked={false} disabled />
                            </div>
                        </div>

                        <hr className='my-1' style={{ height: '1px' }} />

                        <div className="is-flex is-justify-content-space-between">
                            <div>
                                <label className="label">ORDERS_MANAGEMENT</label>
                                <p className="help">Enable order management panel</p>
                            </div>
                            <div>
                                <Switch checked={false} />
                            </div>
                        </div>

                    </div>

                </div>

                <div className="p-4"></div>

                {/* Email config */}
                <div className="card px-0 py-3">

                    <header className="px-3 is-flex is-justify-content-space-between">
                        <span className="is-title is-size-6 has-text-weight-bold is-vcentered my-2">Email config</span>
                        <div className="is-vcentered"></div>
                    </header>

                    <hr className='my-1' style={{ height: '1px' }} />

                    <div className="p-3">

                        <div className="field">
                            <label className="label">EMAIL_USE_TLS</label>
                            <div className="control">
                                <input className="input" type="text" />
                            </div>
                            <p className="help">Determine whether the configuration support TLS</p>
                        </div>

                        <div className="field">
                            <label className="label">EMAIL_HOST_USER</label>
                            <div className="control">
                                <input className="input" type="text" />
                            </div>
                            <p className="help">The authentication user (email). e.g: admin@karrio.io</p>
                        </div>

                        <div className="field">
                            <label className="label">EMAIL_HOST_PASSWORD</label>
                            <div className="control">
                                <input className="input" type="text" />
                            </div>
                            <p className="help">The authentication password</p>
                        </div>

                        <div className="field">
                            <label className="label">EMAIL_HOST</label>
                            <div className="control">
                                <input className="input" type="text" />
                            </div>
                            <p className="help">The mail server host. e.g: smtp.gmail.com</p>
                        </div>

                        <div className="field">
                            <label className="label">EMAIL_PORT</label>
                            <div className="control">
                                <input className="input" type="text" />
                            </div>
                            <p className="help">The mail server port. e.g: 465 (SSL required) or 587 (TLS required)</p>
                        </div>

                        <div className="field">
                            <label className="label">EMAIL_FROM_ADDRESS</label>
                            <div className="control">
                                <input className="input" type="text" />
                            </div>
                            <p className="help">Email sent from. e.g: noreply@karrio.io</p>
                        </div>

                    </div>

                </div>

                <div className="p-4"></div>

                {/* Address validation */}
                <div className="card px-0 py-3">

                    <header className="px-3 is-flex is-justify-content-space-between">
                        <span className="is-title is-size-6 has-text-weight-bold is-vcentered my-2">Address Validation Service</span>
                        <div className="is-vcentered"></div>
                    </header>

                    <hr className='my-1' style={{ height: '1px' }} />

                    <div className="p-3">

                        <div className="field">
                            <label className="label">GOOGLE_CLOUD_API_KEY</label>
                            <div className="control">
                                <input className="input" type="text" />
                            </div>
                            <p className="help">A Google GeoCoding API key</p>
                        </div>

                        <div className="field">
                            <label className="label">CANADAPOST_ADDRESS_COMPLETE_API_KEY</label>
                            <div className="control">
                                <input className="input" type="text" />
                            </div>
                            <p className="help">The Canada Post AddressComplete service API Key</p>
                        </div>

                    </div>

                </div>

                <div className="p-4"></div>

                {/* Data Retention */}
                <div className="card px-0 py-3">

                    <header className="px-3 is-flex is-justify-content-space-between">
                        <span className="is-title is-size-6 has-text-weight-bold is-vcentered my-2">Data retention</span>
                        <div className="is-vcentered"></div>
                    </header>

                    <hr className='my-1' style={{ height: '1px' }} />

                    <div className="p-3">

                        <div className="field">
                            <label className="label">ORDER_DATA_RETENTION</label>
                            <div className="control">
                                <input className="input" type="text" />
                            </div>
                            <p className="help">Order data retention period (in days)</p>
                        </div>

                        <div className="field">
                            <label className="label">TRACKER_DATA_RETENTION</label>
                            <div className="control">
                                <input className="input" type="text" />
                            </div>
                            <p className="help">Tracker data retention period (in days)</p>
                        </div>

                        <div className="field">
                            <label className="label">SHIPMENT_DATA_RETENTION</label>
                            <div className="control">
                                <input className="input" type="text" />
                            </div>
                            <p className="help">Shipment data retention period (in days)</p>
                        </div>

                        <div className="field">
                            <label className="label">API_LOGS_DATA_RETENTION</label>
                            <div className="control">
                                <input className="input" type="text" />
                            </div>
                            <p className="help">API request and SDK tracing logs retention period (in days)</p>
                        </div>

                    </div>

                </div>

                <div className="p-4"></div>

                <div className="p-2 mb-6 has-text-centered">
                    <button className="button is-primary">Save</button>
                </div>
            </>
        );
    };

    return AuthenticatedPage((
        <AdminLayout showModeIndicator={true}>
            <Head><title>{`Platform - ${APP_NAME}`}</title></Head>

            <Component />

        </AdminLayout>
    ), pageProps)
}
