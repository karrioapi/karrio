import { AutomationAuthType, PartialWorkflowConnectionMutationInput } from '@karrio/types/graphql/ee';
import { MetadataEditor, MetadataEditorContext } from '../forms/metadata-editor';
import { SelectField, TextAreaField } from '../components';
import { InputField } from '../components/input-field';
import { useNotifier } from '../components/notifier';
import { htmlLanguage } from '@codemirror/lang-html';
import { ModalFormProps, useModal } from './modal';
import { isEqual, formatRef } from '@karrio/lib';
import { NotificationType } from '@karrio/types';
import { useLoader } from '../components/loader';
import CodeMirror from '@uiw/react-codemirror';
import React from 'react';

type ConnectionModalEditorProps = {
  header?: string;
  connection: PartialWorkflowConnectionMutationInput;
  onSubmit: (connection: PartialWorkflowConnectionMutationInput) => Promise<any>;
};

function reducer(state: Partial<PartialWorkflowConnectionMutationInput>, { name, value }: { name: string, value: string | boolean | Partial<PartialWorkflowConnectionMutationInput> | string[] }): PartialWorkflowConnectionMutationInput {
  console.log("touch reducer", name, value)
  switch (name) {
    case "full":
      return { ...(value as object) };
    case "partial":
      return { ...state, ...(value as object) };
    default:
      return { ...state, [name]: value };
  }
}

export const ConnectionModalEditor: React.FC<ModalFormProps<ConnectionModalEditorProps>> = ({ trigger, ...args }) => {
  const modal = useModal();

  const Component: React.FC<ConnectionModalEditorProps> = props => {
    const { connection: defaultValue = {}, header, onSubmit } = props;
    const loader = useLoader();
    const { close } = useModal();
    const notifier = useNotifier();
    const [key, setKey] = React.useState<string>(`connection-${Date.now()}`);
    const [connection, dispatch] = React.useReducer(reducer, defaultValue, () => defaultValue);

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
      const { ...payload } = connection;
      try {
        loader.setLoading(!!payload.id);
        onSubmit && onSubmit(payload);
        setTimeout(() => close(), 1000);
      } catch (message: any) {
        notifier.notify({ type: NotificationType.error, message });
      }
      loader.setLoading(false);
    };
    console.log(connection)
    return (
      <form className="modal-card-body modal-form" onSubmit={handleSubmit} key={key}>
        <div className="form-floating-header p-4">
          <span className="has-text-weight-bold is-size-6">{header || `Edit connection`}</span>
        </div>
        <div className="p-3 my-4"></div>

        {(connection !== undefined) && <>

          {/* connection type */}
          <SelectField name="auth_type"
            label="Auth type"
            className="is-small is-fullwidth"
            fieldClass="column is-3 mb-0 px-1 py-2"
            value={connection?.auth_type || ''}
            required={true}
            onChange={handleChange}
          >
            {Array.from(new Set(Object.values(AutomationAuthType))).map(
              unit => <option key={unit} value={unit} disabled={unit == AutomationAuthType.oauth2 || unit == AutomationAuthType.jwt}>{formatRef(unit)}</option>
            )}
          </SelectField>

          {/* name */}
          <InputField name="name"
            label="Name"
            wrapperClass="px-1 py-2"
            fieldClass="column mb-0 p-0"
            defaultValue={connection.name || ''}
            required={true}
            onChange={handleChange}
            className="is-small"
          />

          {/* description */}
          <TextAreaField label="description"
            rows={2}
            name="description"
            value={connection.description || ''}
            onChange={handleChange}
            placeholder="Connection description"
            className="is-small"
          />

          {/* http request options */}
          {([AutomationAuthType.jwt, AutomationAuthType.oauth2].includes(connection.auth_type as any)) && <div className="column mb-0 p-0">

            <InputField name="host"
              label="Host"
              className="is-fullwidth is-small"
              wrapperClass="px-1 py-2"
              fieldClass="column mb-0 p-0"
              defaultValue={connection.host || ''}
              required={[AutomationAuthType.jwt, AutomationAuthType.oauth2].includes(connection.auth_type as any)}
              onChange={handleChange}
            />

            <InputField name="endpoint"
              label="Endpoint"
              className="is-fullwidth is-small"
              wrapperClass="px-1 py-2"
              fieldClass="column mb-0 p-0"
              defaultValue={connection.endpoint || ''}
              onChange={handleChange}
            />

            <InputField name="port"
              label="Port"
              type='number'
              className="is-fullwidth is-small"
              wrapperClass="px-1 py-2"
              fieldClass="column mb-0 p-0"
              defaultValue={connection.port || ''}
              onChange={handleChange}
            />

          </div>}

          {/* credentials */}
          <div className="column mb-0 px-0 control">
            <div className="card p-2">
              <MetadataEditor
                metadata={connection.credentials}
                onChange={value => dispatch({ name: 'credentials', value })}
              >
                <MetadataEditorContext.Consumer>{({ isEditing, editMetadata }) => (<>

                  <header className="is-flex is-justify-content-space-between px-2">
                    <span className="is-title is-size-7 has-text-weight-bold is-vcentered my-2">Credentials</span>
                    <div className="is-vcentered">
                      <button
                        type="button"
                        className="button is-small is-info is-text is-inverted p-1"
                        disabled={isEditing}
                        onClick={() => editMetadata()}>
                        <span>Edit credentials</span>
                      </button>
                    </div>
                  </header>

                </>)}</MetadataEditorContext.Consumer>
              </MetadataEditor>
            </div>
          </div>

          {/* auth_template */}
          <div className="column mb-0 p-0 control">
            <label className="label is-size-7">Auth template</label>
            <div className="card is-radiusless">
              <CodeMirror
                height="15vh"
                extensions={[htmlLanguage]}
                value={connection.auth_template || "" as string}
                onChange={value => dispatch({ name: 'auth_template', value })}
              />
            </div>
          </div>

          {([AutomationAuthType.jwt, AutomationAuthType.oauth2].includes(connection.auth_type as any)) && <div className="column mb-0 p-0">

            {/* parameters_template */}
            <div className="column mb-0 p-0 control">
              <label className="label is-size-7">Parameters template</label>
              <div className="card is-radiusless">
                <CodeMirror
                  height="15vh"
                  extensions={[htmlLanguage]}
                  value={connection.parameters_template || "" as string}
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
              disabled={isEqual(connection, defaultValue)}
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
