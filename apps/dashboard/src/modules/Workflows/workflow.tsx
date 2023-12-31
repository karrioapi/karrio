import { ActionNodeInput, AutomationActionType, AutomationAuthType, AutomationTriggerType } from '@karrio/types/graphql/ee';
import { ConnectionModalEditor } from '@karrio/ui/modals/workflow-connection-edit-modal';
import { ActionModalEditor } from '@karrio/ui/modals/workflow-action-edit-modal';
import { isEqual, isNone, isNoneOrEmpty, useLocation } from '@karrio/lib';
import { TextAreaField } from '@karrio/ui/components/textarea-field';
import { WorkflowActionType } from '@karrio/hooks/workflow-actions';
import { ConfirmModalWrapper } from '@karrio/ui/modals/form-modals';
import { AuthenticatedPage } from '@/layouts/authenticated-page';
import { InputField } from '@karrio/ui/components/input-field';
import { useWorkflowForm } from '@karrio/hooks/workflows';
import { useLoader } from '@karrio/ui/components/loader';
import { AppLink } from '@karrio/ui/components/app-link';
import { ModalProvider } from '@karrio/ui/modals/modal';
import django from 'highlight.js/lib/languages/django';
import { bundleContexts } from '@karrio/hooks/utils';
import { SelectField } from '@karrio/ui/components';
import { Disclosure } from '@headlessui/react';
import React, { useState } from 'react';
import hljs from "highlight.js";
import Head from 'next/head';

export { getServerSideProps } from "@/context/main";
const ContextProviders = bundleContexts([ModalProvider]);
hljs.registerLanguage('django', django);

export default function Page(pageProps: any) {
  const Component: React.FC = () => {
    const loader = useLoader();
    const router = useLocation();
    const { id } = router.query;
    const [key, setKey] = useState<string>(`workflow-${Date.now()}`);
    const { workflow, current, isNew, DEFAULT_STATE, query, zipActionWithNode, ...mutation } = useWorkflowForm({ id: id as string });

    const handleChange = async (changes?: Partial<typeof workflow>) => {
      if (changes === undefined) { return; }
      await mutation.updateWorkflow({ id, ...changes });
      setKey(`${id}-${Date.now()}`);
    };

    const NextIndicator = () => (
      <div className="is-flex is-justify-content-space-around p-2 my-3">
        <span className="icon is-size-6">
          <i className="fas fa-lg fa-arrow-down"></i>
        </span>
      </div>
    );

    return (
      <div className="p-4">

        <header className="columns has-background-white"
          style={{ position: 'sticky', zIndex: 1, top: 0, left: 0, right: 0, borderBottom: '1px solid #ddd' }}
        >
          <div className="column is-vcentered">
            <AppLink className="button is-small is-white" href="/workflows" style={{ borderRadius: '50%' }}>
              <span className="icon is-size-6">
                <i className="fas fa-lg fa-times"></i>
              </span>
            </AppLink>
            <span className="title is-4 has-text-weight-semibold px-3">Edit workflow</span>
          </div>
          <div className="column is-flex is-justify-content-end">
            <button
              type="button"
              onClick={() => mutation.save()}
              className="button is-small is-success"
              disabled={loader.loading || isEqual(workflow, current || DEFAULT_STATE)}
            >
              Save
            </button>
          </div>
        </header>

        {(query.isFetched && !!workflow.actions) && <div className="columns m-0">

          {/* Workflow fields section */}
          <div className="column px-0 pb-4 is-relative">

            <InputField label="name"
              name="name"
              value={workflow.name as string}
              onChange={e => handleChange({ name: e.target.value })}
              placeholder="ERP orders sync"
              className="is-small"
              required
            />

            <TextAreaField label="description"
              name="description"
              value={workflow.description as string}
              onChange={e => handleChange({ description: e.target.value })}
              placeholder="Automate ERP orders syncing for fulfillment"
              className="is-small"
            />

          </div>

          <div className="p-3"></div>

          {/* Workflow related objects section */}
          <div className="column card is-9 px-3 py-4 has-background-light is-radiusless" style={{ height: '92vh', maxHeight: '92vh', overflowY: 'auto' }}>

            {/* Trigger section */}
            <Disclosure as='div' className="card px-0" defaultOpen={true} style={{ maxWidth: '500px', margin: 'auto' }}>
              <Disclosure.Button as='header' className="p-3 is-flex is-justify-content-space-between is-clickable">
                <div className="is-title is-size-6 is-vcentered my-2">
                  <span className="has-text-weight-bold">Trigger</span>
                  <p className="is-size-7 has-text-weight-semibold has-text-grey my-1">How the workflow is tiggered</p>
                </div>
              </Disclosure.Button>
              <Disclosure.Panel>
                <hr className='my-1' style={{ height: '1px' }} />

                <div className="p-3">

                  {/* trigger type */}
                  <SelectField name="trigger_type"
                    required={true}
                    label="Trigger type"
                    className="is-fullwidth"
                    fieldClass="column mb-0 px-0 py-2"
                    value={workflow.trigger?.trigger_type || ''}
                    onChange={e => handleChange({ trigger: { ...workflow.trigger, trigger_type: e.target.value } })}
                  >
                    {Array.from(new Set(Object.values(AutomationTriggerType))).map(
                      unit => <option key={unit} value={unit} disabled={unit != AutomationTriggerType.manual}>{unit}</option>
                    )}
                  </SelectField>

                  {/* trigger schedule */}
                  <div className="column mb-0 p-0" style={{
                    display: `${workflow.trigger?.trigger_type == AutomationTriggerType.scheduled ? 'block' : 'none'}`
                  }}>

                    <InputField name="schedule"
                      label="Schedule (cron)"
                      fieldClass="column mb-0 px-1 py-2"
                      defaultValue={workflow.trigger?.schedule || ''}
                      required={workflow.trigger?.trigger_type == AutomationTriggerType.scheduled}
                      onChange={e => handleChange({ trigger: { ...workflow.trigger, schedule: e.target.value } })}
                    />

                  </div>

                  {/* webhook options */}
                  <div className="column mb-0 p-0" style={{
                    display: `${workflow.trigger?.trigger_type == AutomationTriggerType.webhook ? 'block' : 'none'}`
                  }}>

                    <InputField name="secret"
                      label="Webhook secret"
                      fieldClass="column mb-0 px-1 py-2"
                      defaultValue={workflow.trigger?.secret || ''}
                      onChange={e => handleChange({ trigger: { ...workflow.trigger, secret: e.target.value } })}
                    />

                    <InputField name="secret_key"
                      label="Webhook secret key"
                      fieldClass="column mb-0 px-1 py-0"
                      defaultValue={workflow.trigger?.secret_key || ''}
                      required={!isNoneOrEmpty(workflow.trigger?.secret_key)}
                      onChange={e => handleChange({ trigger: { ...workflow.trigger, secret_key: e.target.value } })}
                    />

                  </div>

                </div>
              </Disclosure.Panel>
            </Disclosure>

            <NextIndicator />

            {/* Actions section */}
            {zipActionWithNode(workflow.actions as WorkflowActionType[], workflow.action_nodes as ActionNodeInput[]).map(([action, node], index) => (
              <React.Fragment key={index}>
                <Disclosure as='div' className="card px-0" style={{ maxWidth: '500px', margin: 'auto' }}>
                  <Disclosure.Button as='header' className="p-3 is-flex is-justify-content-space-between is-clickable">
                    <div className="is-title is-size-6 is-vcentered my-2">
                      <span className="has-text-weight-bold">Action</span>
                      <p className="is-size-7 has-text-weight-semibold has-text-grey my-1">
                        {action.name || 'An action to perform'}
                      </p>
                    </div>
                    <div>
                      <ActionModalEditor
                        action={action}
                        onSubmit={mutation.updateAction(index, action?.id)}
                        trigger={
                          <button type="button" className="button is-white">
                            <span className="icon"><i className="fas fa-pen"></i></span>
                          </button>
                        }
                      />
                      <ConfirmModalWrapper
                        onSubmit={mutation.deleteAction(index, action?.id)}
                        trigger={
                          <button type="button" className="button is-white" disabled={index == 0}>
                            <span className="icon"><i className="fas fa-trash"></i></span>
                          </button>
                        }
                      />
                    </div>
                  </Disclosure.Button>
                  <Disclosure.Panel>
                    <hr className='my-1' style={{ height: '1px' }} />

                    <div className="p-2 is-size-7">

                      {/* action type */}
                      <div className="columns my-0 px-3">
                        <div className="column is-4 py-1">
                          <span className="has-text-weight-bold has-text-grey">Action type</span>
                        </div>
                        <div className="column is-8 py-1"><code>{action.action_type}</code></div>
                      </div>

                      {/* action description */}
                      {!!action.description && <div className="columns my-0 px-3">
                        <div className="column is-4 py-1">
                          <span className="has-text-weight-bold has-text-grey">description</span>
                        </div>
                        <div className="column is-8 py-1"><code>{action.description}</code></div>
                      </div>}

                      {/* data mapping options */}
                      {action.action_type == AutomationActionType.data_mapping && <>

                        {/* action parameters type */}
                        <div className="columns my-0 px-3">
                          <div className="column is-4 py-1">
                            <span className="has-text-weight-bold has-text-grey">format</span>
                          </div>
                          <div className="column is-8 py-1"><code>{action.content_type}</code></div>
                        </div>

                        {/* action parameters template */}
                        <div className="columns is-multiline my-0 px-3">
                          <div className="column py-1">
                            <span className="has-text-weight-bold has-text-grey">Template</span>
                          </div>
                          <div className="column is-12 py-1">
                            <pre className="code p-1" style={{ maxHeight: '15vh', overflowY: 'auto' }}>
                              <code
                                dangerouslySetInnerHTML={{
                                  __html: hljs.highlight((action.parameters_template || '') as string, { language: 'django' }).value,
                                }}
                              />
                            </pre>
                          </div>
                        </div>

                      </>}

                      {/* http request options */}
                      {action.action_type == AutomationActionType.http_request && <>

                        {/* action method */}
                        <div className="columns my-0 px-3">
                          <div className="column is-4 py-1">
                            <span className="has-text-weight-bold has-text-grey">Method</span>
                          </div>
                          <div className="column is-8 py-1"><code>{action.method?.toLocaleUpperCase()}</code></div>
                        </div>

                        {/* action host */}
                        <div className="columns my-0 px-3">
                          <div className="column is-4 py-1">
                            <span className="has-text-weight-bold has-text-grey">Host</span>
                          </div>
                          <div className="column is-8 py-1"><code>{action.host}</code></div>
                        </div>

                        {/* host port */}
                        {!isNone(action.port) && <div className="columns my-0 px-3">
                          <div className="column is-4 py-1">
                            <span className="has-text-weight-bold has-text-grey">Port</span>
                          </div>
                          <div className="column is-8 py-1"><code>{action.port}</code></div>
                        </div>}

                        {/* action endpoint */}
                        {!isNoneOrEmpty(action.endpoint) && <div className="columns my-0 px-3">
                          <div className="column is-4 py-1">
                            <span className="has-text-weight-bold has-text-grey">Endpoint</span>
                          </div>
                          <div className="column is-8 py-1"><code>{action.endpoint}</code></div>
                        </div>}

                        {/* action content type */}
                        <div className="columns my-0 px-3">
                          <div className="column is-4 py-1">
                            <span className="has-text-weight-bold has-text-grey">Content Type</span>
                          </div>
                          <div className="column is-8 py-1"><code>{action.content_type}</code></div>
                        </div>

                        {/* action header template */}
                        <div className="columns is-multiline my-0 px-3">
                          <div className="column py-1">
                            <span className="has-text-weight-bold has-text-grey">Header Template</span>
                          </div>
                          <div className="column is-12 py-1">
                            <pre className="code p-1" style={{ maxHeight: '5vh', overflowY: 'auto' }}>
                              <code
                                dangerouslySetInnerHTML={{
                                  __html: hljs.highlight((action.header_template || '') as string, { language: 'django' }).value,
                                }}
                              />
                            </pre>
                          </div>
                        </div>

                        {/* action parameters type */}
                        <div className="columns my-0 px-3">
                          <div className="column is-4 py-1">
                            <span className="has-text-weight-bold has-text-grey">Parameters Type</span>
                          </div>
                          <div className="column is-8 py-1"><code>{action.parameters_type}</code></div>
                        </div>

                        {/* action parameters template */}
                        <div className="columns is-multiline my-0 px-3">
                          <div className="column py-1">
                            <span className="has-text-weight-bold has-text-grey">Parameters Template</span>
                          </div>
                          <div className="column is-12 py-1">
                            <pre className="code p-1" style={{ maxHeight: '15vh', overflowY: 'auto' }}>
                              <code
                                dangerouslySetInnerHTML={{
                                  __html: hljs.highlight((action.parameters_template || "") as string, { language: 'django' }).value,
                                }}
                              />
                            </pre>
                          </div>
                        </div>

                      </>}

                    </div>


                    <Disclosure as='div' className="card px-0 m-2" style={{ maxWidth: '500px', margin: 'auto' }}>
                      <Disclosure.Button as='header' className="p-3 is-flex is-justify-content-space-between is-clickable">
                        <div className="is-title is-size-6 is-vcentered my-2">
                          <span className="has-text-weight-bold">Connection</span>
                          <p className="is-size-7 has-text-weight-semibold has-text-grey my-1">
                            {action.connection?.name || 'A connection for the action'}
                          </p>
                        </div>
                        <div>
                          <ConnectionModalEditor
                            connection={action.connection || { auth_type: 'basic' } as any}
                            onSubmit={mutation.updateActionConnection(index, action?.id)}
                            trigger={
                              <button type="button" className="button is-white">
                                <span className="icon">
                                  <i className={`fas fa-${!!action.connection ? 'pen' : 'plus'}`}></i>
                                </span>
                              </button>
                            }
                          />
                          <ConfirmModalWrapper
                            onSubmit={mutation.deleteActionConnection(index, action?.id, action.connection?.id)}
                            trigger={
                              <button type="button" className="button is-white" disabled={!action.connection}>
                                <span className="icon"><i className="fas fa-trash"></i></span>
                              </button>
                            }
                          />
                        </div>
                      </Disclosure.Button>
                      <Disclosure.Panel>
                        <hr className='my-1' style={{ height: '1px' }} />

                        {!action.connection && <div className="p-3 is-size-7">
                          <div className="message p-2 is-size-7 has-text-weight-bold">
                            <span>No connection defined!</span>
                          </div>
                        </div>}

                        {!!action.connection && <div className="p-3 is-size-7">

                          {/* auth type */}
                          <div className="columns my-0 px-3">
                            <div className="column is-4 py-1">
                              <span className="has-text-weight-bold has-text-grey">Auth type</span>
                            </div>
                            <div className="column is-8 py-1"><code>{action.connection.auth_type}</code></div>
                          </div>

                          {/* connection description */}
                          {!!action.connection.description && <div className="columns my-0 px-3">
                            <div className="column is-4 py-1">
                              <span className="has-text-weight-bold has-text-grey">description</span>
                            </div>
                            <div className="column is-8 py-1"><code>{action.connection.description}</code></div>
                          </div>}

                          {/* http request options */}
                          {[AutomationAuthType.oauth2, AutomationAuthType.jwt].includes(action.connection.auth_type as any) && <>

                            {/* connection host */}
                            <div className="columns my-0 px-3">
                              <div className="column is-4 py-1">
                                <span className="has-text-weight-bold has-text-grey">Host</span>
                              </div>
                              <div className="column is-8 py-1"><code>{action.connection.host}</code></div>
                            </div>

                            {/* host port */}
                            {!isNone(action.connection.port) && <div className="columns my-0 px-3">
                              <div className="column is-4 py-1">
                                <span className="has-text-weight-bold has-text-grey">Port</span>
                              </div>
                              <div className="column is-8 py-1"><code>{action.connection.port}</code></div>
                            </div>}

                            {/* endpoint */}
                            {!isNoneOrEmpty(action.connection.endpoint) && <div className="columns my-0 px-3">
                              <div className="column is-4 py-1">
                                <span className="has-text-weight-bold has-text-grey">Endpoint</span>
                              </div>
                              <div className="column is-8 py-1"><code>{action.connection.endpoint}</code></div>
                            </div>}

                          </>}

                          {/* connection auth template */}
                          <div className="columns is-multiline my-0 px-3">
                            <div className="column py-1">
                              <span className="has-text-weight-bold has-text-grey">Auth template</span>
                            </div>
                            <div className="column is-12 py-1">
                              <pre className="code p-1" style={{ maxHeight: '15vh', overflowY: 'auto' }}>
                                <code
                                  dangerouslySetInnerHTML={{
                                    __html: hljs.highlight((action.connection.auth_template || '') as string, { language: 'django' }).value,
                                  }}
                                />
                              </pre>
                            </div>
                          </div>

                          {[AutomationAuthType.oauth2, AutomationAuthType.jwt].includes(action.connection.auth_type as any) && <>

                            {/* parameters template */}
                            <div className="columns is-multiline my-0 px-3">
                              <div className="column py-1">
                                <span className="has-text-weight-bold has-text-grey">Template</span>
                              </div>
                              <div className="column is-12 py-1">
                                <pre className="code p-1" style={{ maxHeight: '15vh', overflowY: 'auto' }}>
                                  <code
                                    dangerouslySetInnerHTML={{
                                      __html: hljs.highlight((action.connection.parameters_template || '{}') as string, { language: 'django' }).value,
                                    }}
                                  />
                                </pre>
                              </div>
                            </div>

                          </>}

                        </div>}
                      </Disclosure.Panel>
                    </Disclosure>

                  </Disclosure.Panel>
                </Disclosure>

                <NextIndicator />
              </React.Fragment>
            ))}


            <ActionModalEditor
              action={(DEFAULT_STATE.actions || [])[0] as any}
              onSubmit={mutation.addAction}
              trigger={
                <div className="is-flex is-justify-content-space-around p-2">
                  <button type="button" className="button is-small is-default">Add action</button>
                </div>
              }
            />

          </div>

        </div>}

      </div>
    )
  };

  return AuthenticatedPage((
    <>
      <Head><title>{`Workflow - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>

      <ContextProviders>
        <Component />
      </ContextProviders>

    </>
  ), pageProps);
}
