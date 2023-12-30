import { AutomationActionType, AutomationHTTPContentType, AutomationHTTPMethod, AutomationParametersType, CreateWorkflowActionMutationInput, UpdateWorkflowActionMutationInput } from '@karrio/types/graphql/ee';
import { SelectField, TextAreaField } from '../components';
import { InputField } from '../components/input-field';
import { useNotifier } from '../components/notifier';
import { htmlLanguage } from '@codemirror/lang-html';
import { ModalFormProps, useModal } from './modal';
import { NotificationType } from '@karrio/types';
import { useLoader } from '../components/loader';
import CodeMirror from '@uiw/react-codemirror';
import { deepEqual, formatRef } from '@karrio/lib';
import React from 'react';

type ActionDataType = CreateWorkflowActionMutationInput & UpdateWorkflowActionMutationInput;
type ActionModalEditorProps = {
  header?: string;
  action?: ActionDataType;
  onSubmit: (action: ActionDataType) => Promise<any>;
};

function reducer(state: any, { name, value }: { name: string, value: string | boolean | object | string[] }) {
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
    const { action: defaultValue = { is_active: true }, header, onSubmit } = props;
    const loader = useLoader();
    const { close } = useModal();
    const notifier = useNotifier();
    const [action, dispatch] = React.useReducer(reducer, defaultValue);
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
      const { created_at, updated_at, object_type, ...payload } = action;
      try {
        loader.setLoading(true);
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
            value={action?.action_type}
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
            fieldClass="column mb-0 px-1 py-2"
            defaultValue={action.name}
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
          <div className="column mb-0 p-0" style={{ display: `${action.trigger_type == AutomationActionType.http_request ? 'block' : 'none'}` }}>

            <InputField name="host"
              label="Host"
              className="is-fullwidth is-small"
              fieldClass="column mb-0 px-1 py-2"
              defaultValue={action.host}
              required={action.trigger_type == AutomationActionType.http_request}
              onChange={handleChange}
            />

            <InputField name="endpoint"
              label="Endpoint"
              className="is-fullwidth is-small"
              fieldClass="column mb-0 px-1 py-2"
              defaultValue={action.host}
              onChange={handleChange}
            />

            <InputField name="port"
              label="Port"
              type='number'
              className="is-fullwidth is-small"
              fieldClass="column mb-0 px-1 py-2"
              defaultValue={action.port}
              onChange={handleChange}
            />

            {/* method */}
            <SelectField name="method"
              label="HTTP method"
              className="is-small is-fullwidth"
              fieldClass="column is-3 mb-0 px-0 py-2"
              value={action?.method}
              required={true}
              onChange={handleChange}
            >
              {Array.from(new Set(Object.values(AutomationHTTPMethod))).map(
                unit => <option key={unit} value={unit}>{formatRef(unit)}</option>
              )}
            </SelectField>

          </div>

          {/* content_type */}
          <SelectField name="content_type"
            label="Content type"
            className="is-small is-fullwidth"
            fieldClass="column is-3 mb-0 px-0 py-2"
            value={action?.content_type}
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
                value={action.header_template as string}
                onChange={value => dispatch({ name: 'header_template', value })}
              />
            </div>
          </div>

          {/* parameters_type */}
          <SelectField name="parameters_type"
            label="Parameters type"
            className="is-small is-fullwidth"
            fieldClass="column is-3 mb-0 px-0 py-2"
            value={action?.parameters_type}
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
                value={action.parameters_template as string}
                onChange={value => dispatch({ name: 'parameters_template', value })}
              />
            </div>
          </div>

          <div className="p-3 my-5"></div>

          <div className="form-floating-footer has-text-centered p-1">
            <button className="button is-default m-1 is-small" type="button" onClick={close}>
              <span>Cancel</span>
            </button>
            <button className="button is-primary m-1 is-small"
              disabled={deepEqual(defaultValue, action)}
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
