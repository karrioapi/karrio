import {
  AutomationAuthType,
  PartialWorkflowConnectionMutationInput,
} from "@karrio/types/graphql/ee";
import {
  MetadataEditor,
  MetadataEditorContext,
} from "../forms/metadata-editor";
import { SelectField, TextAreaField } from "../components";
import { InputField } from "../components/input-field";
import { useNotifier } from "../components/notifier";
import { htmlLanguage } from "@codemirror/lang-html";
import { ModalFormProps, useModal } from "./modal";
import { isEqual, formatRef } from "@karrio/lib";
import { NotificationType } from "@karrio/types";
import { useLoader } from "../components/loader";
import CodeMirror from "@uiw/react-codemirror";
import React from "react";

type ConnectionModalEditorProps = {
  header?: string;
  connection: PartialWorkflowConnectionMutationInput & {
    // Add validation fields to the connection type
    credentials_from_metafields?: any;
    required_credentials?: string[];
    is_credentials_complete?: boolean;
    credential_validation?: any;
  };
  onSubmit: (
    connection: PartialWorkflowConnectionMutationInput,
  ) => Promise<any>;
};

function reducer(
  state: Partial<PartialWorkflowConnectionMutationInput>,
  {
    name,
    value,
  }: {
    name: string;
    value:
    | string
    | boolean
    | Partial<PartialWorkflowConnectionMutationInput>
    | string[];
  },
): PartialWorkflowConnectionMutationInput {
  switch (name) {
    case "full":
      return { ...(value as object) };
    case "partial":
      return { ...state, ...(value as object) };
    default:
      return { ...state, [name]: value };
  }
}

export const ConnectionModalEditor = ({
  trigger,
  ...args
}: ModalFormProps<ConnectionModalEditorProps>): JSX.Element => {
  const modal = useModal();

  const Component = ({
    connection: defaultValue = {},
    header,
    onSubmit,
  }: ConnectionModalEditorProps): JSX.Element => {
    const loader = useLoader();
    const { close } = useModal();
    const notifier = useNotifier();
    const [key, setKey] = React.useState<string>(`connection-${Date.now()}`);
    const [connection, dispatch] = React.useReducer(
      reducer,
      defaultValue,
      () => defaultValue,
    );

    const handleChange = (event: React.ChangeEvent<any>) => {
      const target = event.target;
      const name: string = target.name;
      let value = target.type === "checkbox" ? target.checked : target.value;

      if (target.multiple === true) {
        value = Array.from(target.selectedOptions).map((o: any) => o.value);
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

    // Helper function to get credential validation errors
    const getCredentialErrors = (): string[] => {
      if (!defaultValue.credential_validation) return [];

      const validation = defaultValue.credential_validation;
      const errors: string[] = [];

      if (validation.missing_credentials && validation.missing_credentials.length > 0) {
        errors.push(...validation.missing_credentials.map((cred: string) => `Missing: ${cred}`));
      }

      if (validation.invalid_credentials && validation.invalid_credentials.length > 0) {
        errors.push(...validation.invalid_credentials.map((cred: string) => `Invalid: ${cred}`));
      }

      return errors;
    };

    // Helper function to check if credentials are incomplete
    const isCredentialsIncomplete = () => {
      return defaultValue.is_credentials_complete === false || getCredentialErrors().length > 0;
    };

    console.log(connection);
    return (
      <form
        className="modal-card-body modal-form"
        onSubmit={handleSubmit}
        key={key}
      >
        <div className="form-floating-header p-4">
          <span className="has-text-weight-bold is-size-6">
            {header || `Edit connection`}
          </span>

          {/* Connection Status Indicator */}
          {defaultValue.id && (
            <div className="mt-2">
              {defaultValue.is_credentials_complete ? (
                <span className="tag is-success is-small">
                  <i className="fas fa-check mr-1"></i>
                  Credentials Complete
                </span>
              ) : (
                <span className="tag is-danger is-small">
                  <i className="fas fa-exclamation-triangle mr-1"></i>
                  Credentials Incomplete
                </span>
              )}
            </div>
          )}
        </div>
        <div className="py-2"></div>

        {connection !== undefined && (
          <>
            {/* connection type */}
            <SelectField
              name="auth_type"
              label="Auth type"
              className="is-small is-fullwidth"
              fieldClass="column is-3 mb-0 px-1 py-2"
              value={connection?.auth_type || ""}
              required={true}
              onChange={handleChange}
            >
              {Array.from(new Set(Object.values(AutomationAuthType))).map(
                (unit) => (
                  <option
                    key={unit}
                    value={unit}
                    disabled={
                      unit == AutomationAuthType.oauth2 ||
                      unit == AutomationAuthType.jwt
                    }
                  >
                    {formatRef(unit)}
                  </option>
                ),
              )}
            </SelectField>

            {/* name */}
            <InputField
              name="name"
              label="Name"
              wrapperClass="px-1 py-2"
              fieldClass="column mb-0 p-0"
              defaultValue={connection.name || ""}
              required={true}
              onChange={handleChange}
              className="is-small"
            />

            {/* description */}
            <div className="column mb-0 px-1 py-2">
              {/* @ts-ignore */}
              <TextAreaField
                label="description"
                rows={2}
                name="description"
                value={connection.description || ""}
                onChange={handleChange}
                placeholder="Connection description"
                className="is-small"
              />
            </div>

            {/* http request options */}
            {[AutomationAuthType.jwt, AutomationAuthType.oauth2].includes(
              connection.auth_type as any,
            ) && (
                <div className="column mb-0 p-0">
                  <InputField
                    name="host"
                    label="Host"
                    className="is-fullwidth is-small"
                    wrapperClass="px-1 py-2"
                    fieldClass="column mb-0 p-0"
                    defaultValue={connection.host || ""}
                    required={[
                      AutomationAuthType.jwt,
                      AutomationAuthType.oauth2,
                    ].includes(connection.auth_type as any)}
                    onChange={handleChange}
                  />

                  <InputField
                    name="endpoint"
                    label="Endpoint"
                    className="is-fullwidth is-small"
                    wrapperClass="px-1 py-2"
                    fieldClass="column mb-0 p-0"
                    defaultValue={connection.endpoint || ""}
                    onChange={handleChange}
                  />

                  <InputField
                    name="port"
                    label="Port"
                    type="number"
                    className="is-fullwidth is-small"
                    wrapperClass="px-1 py-2"
                    fieldClass="column mb-0 p-0"
                    defaultValue={connection.port || ""}
                    onChange={handleChange}
                  />
                </div>
              )}

            {/* credentials with validation feedback */}
            <div className="column mb-0 px-0 py-2 control">
              <div
                className="card p-2"
                style={{
                  borderColor: isCredentialsIncomplete() ? '#ff3860' : undefined,
                  borderWidth: isCredentialsIncomplete() ? '2px' : undefined,
                }}
              >

                {/* Credentials validation warning */}
                {isCredentialsIncomplete() && (
                  <div className="notification is-danger is-light p-3 mb-3">
                    <div className="is-flex is-align-items-center mb-2">
                      <i className="fas fa-exclamation-triangle mr-2"></i>
                      <strong>Credentials Required</strong>
                    </div>

                    {defaultValue.required_credentials && defaultValue.required_credentials.length > 0 && (
                      <div className="mb-2">
                        <p className="is-size-7 mb-1">Required credentials:</p>
                        <div className="tags">
                          {defaultValue.required_credentials.map((cred) => (
                            <span key={cred} className="tag is-danger is-light is-small">
                              {cred}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {getCredentialErrors().length > 0 && (
                      <div>
                        <p className="is-size-7 mb-1">Issues:</p>
                        <ul className="is-size-7">
                          {getCredentialErrors().map((error, index) => (
                            <li key={index} className="has-text-danger">• {error}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}

                <MetadataEditor
                  metadata={connection.credentials}
                  onChange={(value) => dispatch({ name: "credentials", value })}
                >
                  {/* @ts-ignore */}
                  <MetadataEditorContext.Consumer>
                    {({ isEditing, editMetadata }) => (
                      <>
                        <header className="is-flex is-justify-content-space-between py-1">
                          <div className="is-flex is-align-items-center">
                            <span className="is-title is-size-7 has-text-weight-bold is-vcentered">
                              Credentials
                            </span>
                            {isCredentialsIncomplete() && (
                              <span className="icon has-text-danger ml-2" title="Credentials incomplete">
                                <i className="fas fa-exclamation-circle"></i>
                              </span>
                            )}
                          </div>
                          <div className="is-vcentered">
                            <button
                              type="button"
                              className={`button is-small ${isCredentialsIncomplete() ? 'is-danger' : 'is-info'} is-text is-inverted px-2 py-1`}
                              disabled={isEditing}
                              onClick={() => editMetadata()}
                            >
                              <span className="is-size-7">
                                {isCredentialsIncomplete() ? 'Fix Credentials' : 'Edit'}
                              </span>
                            </button>
                          </div>
                        </header>
                      </>
                    )}
                  </MetadataEditorContext.Consumer>
                </MetadataEditor>

                {/* Show current credentials from metafields for reference */}
                {defaultValue.credentials_from_metafields && Object.keys(defaultValue.credentials_from_metafields).length > 0 && (
                  <div className="mt-3">
                    <p className="is-size-7 has-text-grey mb-1">Current credentials from metafields:</p>
                    <div className="tags">
                      {Object.keys(defaultValue.credentials_from_metafields).map((key) => (
                        <span key={key} className="tag is-light is-small">
                          {key}: {defaultValue.credentials_from_metafields[key] ? '✓' : '✗'}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* auth_template */}
            <div className="column mb-0 p-0 control">
              <label className="label is-size-7">Auth template</label>
              <div className="card is-radiusless">
                {/* @ts-ignore */}
                <CodeMirror
                  height="15vh"
                  extensions={[htmlLanguage]}
                  value={connection.auth_template || ("" as string)}
                  onChange={(value) =>
                    dispatch({ name: "auth_template", value })
                  }
                />
              </div>
            </div>

            {[AutomationAuthType.jwt, AutomationAuthType.oauth2].includes(
              connection.auth_type as any,
            ) && (
                <div className="column mb-0 p-0">
                  {/* parameters_template */}
                  <div className="column mb-0 p-0 control">
                    <label className="label is-size-7">Parameters template</label>
                    <div className="card is-radiusless">
                      {/* @ts-ignore */}
                      <CodeMirror
                        height="15vh"
                        extensions={[htmlLanguage]}
                        value={connection.parameters_template || ("" as string)}
                        onChange={(value) =>
                          dispatch({ name: "parameters_template", value })
                        }
                      />
                    </div>
                  </div>
                </div>
              )}

            <div className="py-3"></div>

            <div className="form-floating-footer has-text-centered p-1">
              <button
                className="button is-default m-1 is-small"
                type="button"
                onClick={close}
              >
                <span>Cancel</span>
              </button>
              <button
                className="button is-primary m-1 is-small"
                disabled={isEqual(connection, defaultValue)}
                type="submit"
              >
                <span>Save</span>
              </button>
            </div>
          </>
        )}
      </form>
    );
  };

  return React.cloneElement(trigger, {
    onClick: (e: React.MouseEvent) => {
      e.stopPropagation();
      modal.open(<Component {...args} />);
    },
  });
};
