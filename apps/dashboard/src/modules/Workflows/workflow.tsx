import { WorkflowTriggerType, WorkflowType, useWorkflow, useWorkflowMutation } from '@karrio/hooks/workflows';
import { TextAreaField } from '@karrio/ui/components/textarea-field';
import { WorkflowActionType } from '@karrio/hooks/workflow-actions';
import { isEqual, isNoneOrEmpty, useLocation } from '@karrio/lib';
import { AutomationActionType, AutomationHTTPContentType, AutomationHTTPMethod, AutomationParametersType, AutomationTriggerType } from '@karrio/types/graphql/ee';
import { AuthenticatedPage } from '@/layouts/authenticated-page';
import React, { useEffect, useReducer, useState } from 'react';
import { InputField } from '@karrio/ui/components/input-field';
import { useNotifier } from '@karrio/ui/components/notifier';
import { useLoader } from '@karrio/ui/components/loader';
import { AppLink } from '@karrio/ui/components/app-link';
import { SelectField } from '@karrio/ui/components';
import { NotificationType } from '@karrio/types';
import { Disclosure } from '@headlessui/react';
import CodeMirror from '@uiw/react-codemirror';
import { jsonLanguage } from '@codemirror/lang-json';
import Head from 'next/head';

export { getServerSideProps } from "@/context/main";

type stateValue = string | boolean | string[] | Partial<WorkflowType> | Partial<WorkflowActionType> | Partial<WorkflowTriggerType>;
const DEFAULT_STATE = {
  actions: [{
    name: '',
    desciption: '',
  }],
  trigger: {
    trigger_type: "manual",
  },
  workflow: {
    name: '',
    description: '',
    action_nodes: [
      { order: 1, slug: "" }
    ],
  },
};

function reducer(state: any, { name, value }: { name: string, value: stateValue }) {
  switch (name) {
    case 'partial':
      return { ...(value as object) };
    default:
      return { ...state, [name]: value }
  }
}

function listReducer(states: any, { index = -1, name, value }: { index?: number, name: string, value: stateValue }) {
  switch (name) {
    case 'add':
      return [...states, { ...(value as any) }];
    case 'remove':
      return [...states.filter((_: any, i: number) => i !== index)];
    case 'partial':
      if (index == -1) return [...(value as any)];
      return [...states.map((s: any) => s.id == (value as any).id ? ({ ...(value as object) }) : s)];
    default:
      states[index] = { ...states[index], [name]: value };
      return [...states];
  }
}

export default function Page(pageProps: any) {
  const Component: React.FC = () => {
    const loader = useLoader();
    const router = useLocation();
    const { id } = router.query;
    const notifier = useNotifier();
    const mutation = useWorkflowMutation();
    const [isNew, setIsNew] = useState<boolean>();
    const [workflow, dispatch] = useReducer(reducer, DEFAULT_STATE.workflow, () => DEFAULT_STATE.workflow);
    const [trigger, dispatchTrigger] = useReducer(reducer, DEFAULT_STATE.trigger, () => DEFAULT_STATE.trigger);
    const [actions, dispatchActions] = useReducer(listReducer, DEFAULT_STATE.actions, () => DEFAULT_STATE.actions);
    const action = {} as any

    const { query: { data: { workflow: current } = {}, ...query }, workflowId, setWorkflowId } = useWorkflow({
      setVariablesToURL: true,
      id: id as string,
    });

    const handleChange = (dispatcher: React.Dispatch<any>, index?: number) => (event: React.ChangeEvent<any>) => {
      const target = event.target;
      let value = target.type === 'checkbox' ? target.checked : target.value;
      let name: string = target.name;

      if (target.multiple === true) {
        value = Array.from(target.selectedOptions).map((o: any) => o.value)
      }

      dispatcher({ name, value, index });
    };
    const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
      evt.preventDefault();
      loader.setLoading(true);
      const { updated_at, ...data } = workflow;

      try {
        if (isNew) {
          const { create_workflow } = await mutation.createWorkflow.mutateAsync(data);
          notifier.notify({ type: NotificationType.success, message: `Document workflow created successfully` });
          loader.setLoading(false);

          setWorkflowId(create_workflow.workflow?.id as string);
        } else {
          await mutation.updateWorkflow.mutateAsync(data);
          query.refetch();
          notifier.notify({ type: NotificationType.success, message: `Document workflow updated successfully` });
          loader.setLoading(false);
        }
      } catch (message: any) {
        notifier.notify({ type: NotificationType.error, message });
        loader.setLoading(false);
      }
    };
    const NextIndicator = () => (
      <div className="is-flex is-justify-content-space-around p-2 my-3">
        <span className="icon is-size-6">
          <i className="fas fa-lg fa-arrow-down"></i>
        </span>
      </div>
    );

    useEffect(() => { setIsNew(workflowId === 'new'); }, [workflowId]);
    useEffect(() => {
      if (workflowId !== 'new') {
        dispatch({ name: 'partial', value: current as any });
        // dispatchActions({ name: 'partial', value: (current?.actions || DEFAULT_STATE.actions) as any });
        dispatchTrigger({ name: 'partial', value: (current?.trigger || DEFAULT_STATE.trigger) as any });
      }
    }, [current]);

    return (
      <form onSubmit={handleSubmit} className="p-4">

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
              type="submit"
              className="button is-small is-success"
              disabled={loader.loading || isEqual(workflow, workflow || DEFAULT_STATE)}
            >
              Save
            </button>
          </div>
        </header>

        <div className="columns m-0">

          <div className="column px-0 pb-4 is-relative">

            <InputField label="name"
              name="name"
              value={workflow.name as string}
              onChange={handleChange(dispatch)}
              placeholder="ERP orders sync"
              className="is-small"
              required
            />

            <TextAreaField label="description"
              name="description"
              value={workflow.description as string}
              onChange={handleChange(dispatch)}
              placeholder="Automate ERP orders syncing for fulfillment"
              className="is-small"
            />

          </div>

          <div className="p-3"></div>

          <div className="column card is-9 px-3 py-4 has-background-light is-radiusless" style={{ maxHeight: '92vh', overflowY: 'auto' }}>

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
                    label="Trigger type"
                    className="is-fullwidth"
                    fieldClass="column mb-0 px-0 py-2"
                    value={trigger?.trigger_type}
                    required={true}
                    onChange={handleChange(dispatchTrigger)}
                  >
                    {Array.from(new Set(Object.values(AutomationTriggerType))).map(
                      unit => <option key={unit} value={unit}>{unit}</option>
                    )}
                  </SelectField>

                  {/* trigger schedule */}
                  <div className="column mb-0 p-0" style={{
                    display: `${trigger.trigger_type == AutomationTriggerType.scheduled ? 'block' : 'none'}`
                  }}>

                    <InputField name="schedule"
                      label="Schedule (cron)"
                      fieldClass="column mb-0 px-1 py-2"
                      defaultValue={trigger.schedule}
                      required={trigger.trigger_type == AutomationTriggerType.scheduled}
                      onChange={handleChange(dispatchTrigger)}
                    />

                  </div>

                  {/* webhook options */}
                  <div className="column mb-0 p-0" style={{
                    display: `${trigger.trigger_type == AutomationTriggerType.webhook ? 'block' : 'none'}`
                  }}>

                    <InputField name="secret"
                      label="Webhook secret"
                      fieldClass="column mb-0 px-1 py-2"
                      defaultValue={trigger.secret}
                      onChange={handleChange(dispatchTrigger)}
                    />

                    <InputField name="secret_key"
                      label="Webhook secret key"
                      fieldClass="column mb-0 px-1 py-0"
                      defaultValue={trigger.secret_key}
                      required={!isNoneOrEmpty(trigger.secret_key)}
                      onChange={handleChange(dispatchTrigger)}
                    />

                  </div>

                </div>
              </Disclosure.Panel>
            </Disclosure>

            <NextIndicator />

            <Disclosure as='div' className="card px-0" style={{ maxWidth: '500px', margin: 'auto' }}>
              {({ open }) => <>

                <Disclosure.Button as='header' className="p-3 is-flex is-justify-content-space-between is-clickable">
                  <div className="is-title is-size-6 is-vcentered my-2">
                    <span className="has-text-weight-bold">Action</span>
                    <p className="is-size-7 has-text-weight-semibold has-text-grey my-1">
                      {action.name || 'An action to perform'}
                    </p>
                  </div>
                  <div style={{ marginTop: 'auto', marginBottom: 'auto' }}>
                    <button type="button" className="button is-white" onClick={e => { e.stopPropagation(); }}>
                      <span className="icon"><i className="fas fa-trash"></i></span>
                    </button>
                  </div>
                </Disclosure.Button>

                <Disclosure.Panel>
                  <hr className='my-1' style={{ height: '1px' }} />

                  <div className="p-3">

                    {/* action type */}
                    <SelectField name="action_type"
                      label="Trigger type"
                      className="is-fullwidth is-small"
                      fieldClass="column mb-0 px-0 py-2"
                      value={action?.action_type}
                      required={true}
                      onChange={handleChange(dispatchActions, 0)}
                    >
                      {Array.from(new Set(Object.values(AutomationActionType))).map(
                        unit => <option key={unit} value={unit}>{unit}</option>
                      )}
                    </SelectField>

                    {/* name */}
                    <InputField name="name"
                      label="Name"
                      fieldClass="column mb-0 px-1 py-2"
                      defaultValue={action.name}
                      required={true}
                      onChange={handleChange(dispatchActions, 0)}
                      className="is-small"
                    />

                    {/* description */}
                    <TextAreaField label="description"
                      rows={2}
                      name="description"
                      value={action.description || ''}
                      onChange={handleChange(dispatchActions, 0)}
                      placeholder="Action description"
                      className="is-small"
                    />

                    {/* http request options */}
                    <div className="column mb-0 p-0" style={{ display: `${action.trigger_type == AutomationActionType.http_request ? 'block' : 'none'}` }}>

                      <InputField name="host"
                        label="Host"
                        className="is-fullwidth is-small"
                        fieldClass="column mb-0 px-1 py-2"
                        defaultValue={action.host}
                        required={action.trigger_type == AutomationActionType.http_request}
                        onChange={handleChange(dispatchActions, 0)}
                      />

                      <InputField name="endpoint"
                        label="Endpoint"
                        className="is-fullwidth is-small"
                        fieldClass="column mb-0 px-1 py-2"
                        defaultValue={action.host}
                        onChange={handleChange(dispatchActions, 0)}
                      />

                      <InputField name="port"
                        label="Port"
                        type='number'
                        className="is-fullwidth is-small"
                        fieldClass="column mb-0 px-1 py-2"
                        defaultValue={action.port}
                        onChange={handleChange(dispatchActions, 0)}
                      />

                      {/* method */}
                      <SelectField name="method"
                        label="HTTP method"
                        className="is-fullwidth is-small"
                        fieldClass="column mb-0 px-0 py-2"
                        value={action?.method}
                        required={true}
                        onChange={handleChange(dispatchActions, 0)}
                      >
                        {Array.from(new Set(Object.values(AutomationHTTPMethod))).map(
                          unit => <option key={unit} value={unit}>{unit}</option>
                        )}
                      </SelectField>

                    </div>

                    {/* content_type */}
                    <SelectField name="content_type"
                      label="Content type"
                      className="is-fullwidth is-small"
                      fieldClass="column mb-0 px-0 py-2"
                      value={action?.content_type}
                      required={true}
                      onChange={handleChange(dispatchActions, 0)}
                    >
                      {Array.from(new Set(Object.values(AutomationHTTPContentType))).map(
                        unit => <option key={unit} value={unit}>{unit}</option>
                      )}
                    </SelectField>

                    {/* header_template */}
                    <div className="column mb-0 p-0 control">
                      <label className="label is-size-7">Header template</label>
                      <div className="card is-radiusless">
                        <CodeMirror
                          height="15vh"
                          extensions={[jsonLanguage]}
                          value={action.header_template as string}
                          onChange={value => dispatchActions({ name: 'header_template', value, index: 0 })}
                        />
                      </div>
                    </div>

                    {/* parameters_type */}
                    <SelectField name="parameters_type"
                      label="Parameters type"
                      className="is-fullwidth is-small"
                      fieldClass="column mb-0 px-0 py-2"
                      value={action?.parameters_type}
                      required={true}
                      onChange={handleChange(dispatchActions, 0)}
                    >
                      {Array.from(new Set(Object.values(AutomationParametersType))).map(
                        unit => <option key={unit} value={unit}>{unit}</option>
                      )}
                    </SelectField>

                    {/* parameters_template */}
                    <div className="column mb-0 p-0 control">
                      <label className="label is-size-7">Parameters template</label>
                      <div className="card is-radiusless">
                        <CodeMirror
                          height="25vh"
                          extensions={[jsonLanguage]}
                          value={action.parameters_template as string}
                          onChange={value => dispatchActions({ name: 'parameters_template', value, index: 0 })}
                        />
                      </div>
                    </div>

                  </div>
                </Disclosure.Panel>

              </>}
            </Disclosure>

            <NextIndicator />

            <div className="is-flex is-justify-content-space-around p-2">
              <button className="button is-small is-default">Add action</button>
            </div>

          </div>

        </div>

      </form>
    )
  };

  return AuthenticatedPage((
    <>
      <Head><title>{`Workflow - ${(pageProps as any).metadata?.APP_NAME}`}</title></Head>

      <Component />
    </>
  ), pageProps);
}
