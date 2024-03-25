import { AutomationActionType, AutomationHTTPContentType, AutomationHTTPMethod, AutomationParametersType, PartialWorkflowActionMutationInput } from '@karrio/types/graphql/ee';
import { SelectField, TextAreaField } from '../components';
import { InputField } from '../components/input-field';
import { useNotifier } from '../components/notifier';
import { htmlLanguage } from '@codemirror/lang-html';
import { isEqual, formatRef } from '@karrio/lib';
import { ModalFormProps, useModal } from './modal';
import { NotificationType } from '@karrio/types';
import { useLoader } from '../components/loader';
import CodeMirror from '@uiw/react-codemirror';
import React from 'react';

type ActionModalEditorProps = {
  header?: string;
  action: PartialWorkflowActionMutationInput;
  onSubmit: (action: PartialWorkflowActionMutationInput) => Promise<any>;
};

function reducer(state: Partial<PartialWorkflowActionMutationInput>, { name, value }: { name: string, value: string | boolean | Partial<PartialWorkflowActionMutationInput> | string[] }): PartialWorkflowActionMutationInput {
  switch (name) {
    case "full":
      return { ...(value as object) };
    case "partial":
      return { ...state, ...(value as object) };
    default:
      return { ...state, [name]: value };
  }
}

export const ActionModalEditor: React.FC<ModalFormProps<ActionModalEditorProps>> = ({ trigger, ...args }) => {
  const modal = useModal();

  const Component: React.FC<ActionModalEditorProps> = props => {
    const { action: defaultValue = {}, header, onSubmit } = props;
    const loader = useLoader();
    const { close } = useModal();
    const notifier = useNotifier();
    const [action, dispatch] = React.useReducer(reducer, defaultValue, () => defaultValue);
    const [key, setKey] = React.useState<string>(`action-${Date.now()}`);

    const handleChange = (event: React.ChangeEvent<any>) => {
      const target = event.target;
      const name: string = target.name;
      let value = target.type === 'checkbox' ? target.checked : target.value;

      if (target.multiple === true) {
        value = Array.from(target.selectedOptions).map((o: any) => o.value)
      }

      dispatch({ name, value });
    };
    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      const { ...payload } = action;
      try {
        loader.setLoading(!!payload.id);
        onSubmit && onSubmit(payload);
        setTimeout(() => close(), 1000);
      } catch (message: any) {
        notifier.notify({ type: NotificationType.error, message });
      }
      loader.setLoading(false);
    };

    return (
      <form className="modal-card-body modal-form" onSubmit={handleSubmit} key={key}>
        <div className="form-floating-header p-4">
          <span className="has-text-weight-bold is-size-6">{header || `Edit action`}</span>
        </div>
        <div className="p-3 my-4"></div>

        {(action !== undefined) && <>

          {/* action type */}
          <SelectField name="action_type"
            label="Trigger type"
            className="is-small is-fullwidth"
            fieldClass="column is-3 mb-0 px-1 py-2"
            value={action?.action_type || ''}
            required={true}
            onChange={handleChange}
          >
            {Array.from(new Set(Object.values(AutomationActionType))).map(
              unit => <option key={unit} value={unit} disabled={unit == AutomationActionType.function_call}>{formatRef(unit)}</option>
            )}
          </SelectField>

          {/* name */}
          <InputField name="name"
            label="Name"
            wrapperClass="px-1 py-2"
            fieldClass="column mb-0 p-0"
            defaultValue={action.name || ''}
            required={true}
            onChange={handleChange}
            className="is-small"
          />

          {/* description */}
          <TextAreaField label="description"
            rows={2}
            name="description"
            value={action.description || ''}
            onChange={handleChange}
            placeholder="Action description"
            className="is-small"
          />

          {/* http request options */}
          {(action.action_type == AutomationActionType.http_request) && <div className="column mb-0 p-0">

            <InputField name="host"
              label="Host"
              className="is-fullwidth is-small"
              wrapperClass="px-1 py-2"
              fieldClass="column mb-0 p-0"
              defaultValue={action.host || ''}
              required={action.action_type == AutomationActionType.http_request}
              onChange={handleChange}
            />

            <InputField name="endpoint"
              label="Endpoint"
              className="is-fullwidth is-small"
              wrapperClass="px-1 py-2"
              fieldClass="column mb-0 p-0"
              defaultValue={action.endpoint || ''}
              onChange={handleChange}
            />

            <InputField name="port"
              label="Port"
              type='number'
              className="is-fullwidth is-small"
              wrapperClass="px-1 py-2"
              fieldClass="column mb-0 p-0"
              defaultValue={action.port || ''}
              onChange={handleChange}
            />

            {/* method */}
            <SelectField name="method"
              label="HTTP method"
              className="is-small is-fullwidth"
              wrapperClass="px-0 py-2"
              fieldClass="column is-3 mb-0 p-0"
              value={action?.method || ''}
              required={true}
              onChange={handleChange}
            >
              {Array.from(new Set(Object.values(AutomationHTTPMethod))).map(
                unit => <option key={unit} value={unit}>{formatRef(unit)}</option>
              )}
            </SelectField>

            {/* content_type */}
            <SelectField name="content_type"
              label="Content type"
              className="is-small is-fullwidth"
              fieldClass="column is-3 mb-0 px-0 py-2"
              value={action?.content_type || ''}
              required={true}
              onChange={handleChange}
            >
              {Array.from(new Set(Object.values(AutomationHTTPContentType))).map(
                unit => <option key={unit} value={unit}>{formatRef(unit)}</option>
              )}
            </SelectField>

            {/* header_template */}
            <div className="column mb-0 p-0 control">
              <label className="label is-size-7">Header template</label>
              <div className="card is-radiusless">
                <CodeMirror
                  height="20vh"
                  extensions={[htmlLanguage]}
                  value={action.header_template || "" as string}
                  onChange={value => dispatch({ name: 'header_template', value })}
                />
              </div>
            </div>

            {/* parameters_type */}
            <SelectField name="parameters_type"
              label="Parameters type"
              className="is-small is-fullwidth"
              fieldClass="column is-3 mb-0 px-0 py-2"
              value={action?.parameters_type || ''}
              required={true}
              onChange={handleChange}
            >
              {Array.from(new Set(Object.values(AutomationParametersType))).map(
                unit => <option key={unit} value={unit}>{formatRef(unit)}</option>
              )}
            </SelectField>

            {/* parameters_template */}
            <div className="column mb-0 p-0 control">
              <label className="label is-size-7">Parameters template</label>
              <div className="card is-radiusless">
                <CodeMirror
                  height="40vh"
                  extensions={[htmlLanguage]}
                  value={action.parameters_template || "" as string}
                  onChange={value => dispatch({ name: 'parameters_template', value })}
                />
              </div>
            </div>

          </div>}

          {/* function call options */}
          {(action.action_type == AutomationActionType.data_mapping) && <div className="column mb-0 p-0">

            {/* content_type */}
            <SelectField name="content_type"
              label="Content type"
              className="is-small is-fullwidth"
              fieldClass="column is-3 mb-0 px-0 py-2"
              value={action?.content_type || ''}
              required={true}
              onChange={handleChange}
            >
              {Array.from(new Set(Object.values(AutomationHTTPContentType))).map(
                unit => <option key={unit} value={unit}>{formatRef(unit)}</option>
              )}
            </SelectField>

            {/* parameters_template */}
            <div className="column mb-0 p-0 control">
              <label className="label is-size-7">Parameters template</label>
              <div className="card is-radiusless">
                <CodeMirror
                  height="40vh"
                  extensions={[htmlLanguage]}
                  value={action.parameters_template || "" as string}
                  onChange={value => dispatch({ name: 'parameters_template', value })}
                />
              </div>
            </div>

          </div>}

          {/* conditional options */}
          {(action.action_type == AutomationActionType.conditional) && <div className="column mb-0 p-0">

            {/* parameters_template */}
            <div className="column mb-0 p-0 control">
              <label className="label is-size-7">Data template</label>
              <div className="card is-radiusless">
                <CodeMirror
                  height="40vh"
                  extensions={[htmlLanguage]}
                  value={action.parameters_template || "" as string}
                  onChange={value => dispatch({ name: 'parameters_template', value })}
                />
              </div>
            </div>

          </div>}

          <div className="p-3 my-5"></div>

          <div className="form-floating-footer has-text-centered p-1">
            <button className="button is-default m-1 is-small" type="button" onClick={close}>
              <span>Cancel</span>
            </button>
            <button className="button is-primary m-1 is-small"
              disabled={isEqual(defaultValue, action)}
              type="submit">
              <span>Save</span>
            </button>
          </div>

        </>}

      </form>
    )
  };

  return React.cloneElement(trigger, {
    onClick: (e: React.MouseEvent) => {
      e.stopPropagation();
      modal.open(<Component {...args} />)
    }
  });
};
