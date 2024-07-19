import {
  Collection,
  LABEL_TYPES,
  NoneEnum,
  NotificationType,
  CarrierSettingsCarrierNameEnum,
} from "@karrio/types";
import {
  isEqual,
  isNone,
  isNoneOrEmpty,
  useLocation,
  validationMessage,
  validityCheck,
} from "@karrio/lib";
import {
  MetadataEditor,
  MetadataEditorContext,
} from "../forms/metadata-editor";
import { CarrierConnectionType } from "@karrio/hooks/user-connection";
import React, { useContext, useReducer, useState } from "react";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import { Notifier, Notify } from "../components/notifier";
import { SelectField } from "../components/select-field";
import { MetadataObjectTypeEnum } from "@karrio/types";
import { InputField } from "../components/input-field";
import { CountryInput } from "../forms/country-input";
import { useAppMode } from "@karrio/hooks/app-mode";
import { Disclosure } from "@headlessui/react";
import { Loading } from "../components/loader";
import { TextAreaField } from "../components";

type CarrierNameType = CarrierSettingsCarrierNameEnum | NoneEnum;
type OperationType = {
  connection?: CarrierConnectionType;
  create?: (data: any) => Promise<any>;
  update?: (data: any) => Promise<any>;
  onConfirm?: () => Promise<any>;
};
type ConnectProviderModalContextType = {
  editConnection: (operation?: OperationType) => void;
};

export const ConnectProviderModalContext =
  React.createContext<ConnectProviderModalContextType>(
    {} as ConnectProviderModalContextType,
  );

interface ConnectProviderModalComponent {
  connection?: CarrierConnectionType;
  children?: React.ReactNode;
}

function reducer(
  state: any,
  { name, value }: { name: string; value: string | boolean | object | null },
) {
  switch (name) {
    case "full":
      return { ...(value as object) };
    case "partial":
      return { ...state, ...(value as object) };
    case "carrier_name":
      return { [name]: value };
    default:
      return { ...state, [name]: value };
  }
}

export const ConnectProviderModal: React.FC<ConnectProviderModalComponent> = ({
  children,
}) => {
  const {
    references: { carriers, connection_configs, service_names, option_names },
  } = useAPIMetadata();
  const { testMode } = useAppMode();
  const { notify } = useContext(Notify);
  const { loading, setLoading } = useContext(Loading);
  const { addUrlParam, removeUrlParam } = useLocation();
  const DEFAULT_STATE = (): Partial<CarrierConnectionType> => ({
    carrier_name: NoneEnum.none,
  });
  const [key, setKey] = useState<string>(`connection-${Date.now()}`);
  const [isNew, setIsNew] = useState<boolean>(true);
  const [payload, dispatch] = useReducer(reducer, DEFAULT_STATE());
  const [carrier_name, setCarrierName] = useState<CarrierNameType>(
    NoneEnum.none,
  );
  const [isActive, setIsActive] = useState<boolean>(false);
  const [isInvalid, setIsInvalid] = useState<boolean>(false);
  const [operation, setOperation] = useState<OperationType>(
    {} as OperationType,
  );

  const editConnection = (operation: OperationType = {}): void => {
    const connection = operation.connection || DEFAULT_STATE();
    const connection_carrier: CarrierNameType =
      connection.carrier_name === NoneEnum.none ||
      Object.values(CarrierSettingsCarrierNameEnum).includes(
        connection.carrier_name as any,
      )
        ? (connection.carrier_name as CarrierSettingsCarrierNameEnum)
        : NoneEnum.none;
    setCarrierName(connection_carrier);
    setIsNew(isNone(operation.connection));
    setOperation(operation);
    dispatch({ name: "full", value: connection });
    setKey(`connection-${Date.now()}`);
    setIsActive(true);
    addUrlParam("modal", connection.id || "new");
  };
  const close = (e?: React.MouseEvent) => {
    e?.preventDefault();
    if (isNew) {
      dispatch({ name: "full", value: DEFAULT_STATE() });
      setCarrierName(NoneEnum.none);
    }
    setKey(`connection-${Date.now()}`);
    setIsActive(false);
    removeUrlParam("modal");
  };
  const field = (property: string) => {
    return fieldState(carrier_name as CarrierNameType, property);
  };
  const directChange = (property: string) => (value: any) => {
    dispatch({
      name: property,
      value: value === "none" || isNoneOrEmpty(value) ? null : value,
    });
  };

  const handleChange = (event: React.ChangeEvent<any>) => {
    const target = event.target;
    const value = target.type === "checkbox" ? target.checked : target.value;
    const name: string = target.name;

    dispatch({
      name,
      value: value === "none" || isNoneOrEmpty(value) ? null : value,
    });
  };
  const handleCarrierChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const target = event.target;
    const value = target.value as CarrierNameType;
    let state = ["lang", "language"].reduce(
      (acc, cur) => {
        if (fieldState(value, cur).default) {
          return { ...acc, [cur]: fieldState(value, cur).default };
        }
        return acc;
      },
      {
        carrier_id: `${value.toLocaleLowerCase()}${testMode ? "-test" : ""}`,
      },
    );

    setCarrierName(value);
    dispatch({ name: "full", value: state });
  };
  const handleConfigChange = (
    event: React.ChangeEvent<HTMLInputElement & HTMLSelectElement>,
  ) => {
    const target = event.target;
    const name: string = target.name;
    let value =
      (target as any).type === "checkbox" ? target.checked : target.value;

    if (target.multiple === true) {
      value = Array.from(target.selectedOptions).map(
        (o: any) => o.value,
      ) as any;
    }

    const config = {
      ...payload.config,
      [name]: value === "none" || isNoneOrEmpty(value) ? null : value,
    };
    dispatch({ name: "config", value: config });
  };
  const handleSubmit = async (evt: React.FormEvent<HTMLFormElement>) => {
    evt.preventDefault();
    setLoading(true);
    try {
      const {
        carrier_name: _,
        __typename,
        capabilities,
        display_name,
        rate_sheet,
        services,
        test_mode,
        ...content
      } = payload;
      const data = {
        [carrier_name]: carrier_name.includes("generic")
          ? { ...content, display_name }
          : content,
      };
      if (isNew) {
        operation.create && (await operation.create(data));
      } else {
        operation.update && (await operation.update(data));
        dispatch({ name: "partial", value: payload });
      }
      notify({
        type: NotificationType.success,
        message: `carrier connection ${isNew ? "registered" : "updated"} successfully`,
      });
      setTimeout(() => close(), 500);
      operation.onConfirm && operation.onConfirm();
    } catch (err: any) {
      notify({ type: NotificationType.error, message: err });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Notifier>
      <ConnectProviderModalContext.Provider value={{ editConnection }}>
        {children}
      </ConnectProviderModalContext.Provider>

      <div className={`modal ${isActive ? "is-active" : ""}`} key={key}>
        <div className="modal-background"></div>
        <form className="modal-card" onSubmit={handleSubmit}>
          <section
            className="modal-card-body modal-form"
            onChange={(e: any) => {
              setIsInvalid(
                e.currentTarget.querySelectorAll(".is-danger").length > 0,
              );
            }}
          >
            <div className="form-floating-header p-4">
              <span className="has-text-weight-bold is-size-6">
                Edit carrier account
              </span>
            </div>
            <div className="p-3 my-4"></div>

            <SelectField
              value={carrier_name}
              onChange={handleCarrierChange}
              disabled={!isNew}
              key={`select-${key}`}
              className="is-fullwidth"
              required
            >
              <option value="none">Select Carrier</option>

              {carriers &&
                Object.keys(carriers)
                  .sort()
                  .map((carrier) => (
                    <option key={carrier} value={carrier}>
                      {(carriers as Collection)[carrier]}
                    </option>
                  ))}
            </SelectField>

            {carrier_name !== NoneEnum.none && field("carrier_id").exists && (
              <>
                <hr />

                {field("display_name").exists && (
                  <InputField
                    label="Display Name"
                    value={payload.display_name}
                    name="display_name"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("display_name").required}
                  />
                )}

                {field("custom_carrier_name").exists && (
                  <InputField
                    label="Slug"
                    value={payload.custom_carrier_name}
                    onInvalid={validityCheck(
                      validationMessage("Please enter a valid slug"),
                    )}
                    name="custom_carrier_name"
                    onChange={handleChange}
                    className="is-small"
                    pattern="^[a-z0-9_]+$"
                    required={field("custom_carrier_name").required}
                  />
                )}

                <InputField
                  label="Carrier Id"
                  value={payload.carrier_id}
                  name="carrier_id"
                  wrapperClass="pt-2"
                  onChange={handleChange}
                  className="is-small"
                  required={field("carrier_id").required}
                >
                  <p className="help">
                    friendly-tag. e.g:{" "}
                    <strong>dhl-express-us, ups-ca-test...</strong>
                  </p>
                </InputField>

                {/* Carrier specific fields BEGING */}

                {field("site_id").exists && (
                  <InputField
                    label="Site Id"
                    value={payload.site_id}
                    name="site_id"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("site_id").required}
                  />
                )}

                {field("sendle_id").exists && (
                  <InputField
                    label="Sendle ID"
                    value={payload.sendle_id}
                    name="sendle_id"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("sendle_id").required}
                  />
                )}

                {field("seller_id").exists && (
                  <InputField
                    label="Seller ID"
                    value={payload.seller_id}
                    name="seller_id"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("seller_id").required}
                  />
                )}

                {field("customer_id").exists && (
                  <InputField
                    label="Customer ID"
                    value={payload.customer_id}
                    name="customer_id"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("customer_id").required}
                  />
                )}

                {field("identifier").exists && (
                  <InputField
                    label="Identifier"
                    value={payload.identifier}
                    name="identifier"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("identifier").required}
                  />
                )}

                {field("api_key").exists && (
                  <InputField
                    label="API Key"
                    value={payload.api_key}
                    name="api_key"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("api_key").required}
                  />
                )}

                {field("dhl_api_key").exists && (
                  <InputField
                    label="DHL API Key (Consumer Key)"
                    value={payload.dhl_api_key}
                    name="dhl_api_key"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("dhl_api_key").required}
                  />
                )}

                {field("laposte_api_key").exists && (
                  <InputField
                    label="La Poste API Key"
                    value={payload.laposte_api_key}
                    name="laposte_api_key"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("laposte_api_key").required}
                  />
                )}

                {field("client_id").exists && (
                  <InputField
                    label="Client ID"
                    value={payload.client_id}
                    name="client_id"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("client_id").required}
                  />
                )}

                {field("partner_id").exists && (
                  <InputField
                    label="Partner ID"
                    value={payload.partner_id}
                    name="partner_id"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("partner_id").required}
                  />
                )}

                {field("developer_id").exists && (
                  <InputField
                    label="Developer ID"
                    value={payload.developer_id}
                    name="developer_id"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("developer_id").required}
                  />
                )}

                {field("check_word").exists && (
                  <InputField
                    label="Check Word"
                    value={payload.check_word}
                    type="text"
                    name="check_word"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("check_word").required}
                  />
                )}

                {field("delis_id").exists && (
                  <InputField
                    label="Delis ID"
                    value={payload.delis_id}
                    name="delis_id"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("delis_id").required}
                  />
                )}

                {field("username").exists && (
                  <InputField
                    label="Username"
                    value={payload.username}
                    name="username"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("username").required}
                  />
                )}

                {field("password").exists && (
                  <InputField
                    label="Password"
                    value={payload.password}
                    type="text"
                    name="password"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("password").required}
                  />
                )}

                {field("principal").exists && (
                  <InputField
                    label="Principal"
                    value={payload.principal}
                    name="principal"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("principal").required}
                  />
                )}

                {field("credential").exists && (
                  <InputField
                    label="Credential"
                    value={payload.credential}
                    type="text"
                    name="credential"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("credential").required}
                  />
                )}

                {field("zt_id").exists && (
                  <InputField
                    label="ZT ID"
                    value={payload.zt_id}
                    name="zt_id"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={!testMode}
                  />
                )}

                {field("zt_password").exists && (
                  <InputField
                    label="ZT Password"
                    value={payload.zt_password}
                    name="zt_password"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={!testMode}
                  />
                )}

                {field("app_id").exists && (
                  <InputField
                    label="App Id"
                    value={payload.app_id}
                    name="app_id"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={!testMode}
                  />
                )}

                {field("app_token").exists && (
                  <InputField
                    label="App Token"
                    value={payload.app_token}
                    name="app_token"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={!testMode}
                  />
                )}

                {field("client_secret").exists && (
                  <InputField
                    label="Client Secret"
                    value={payload.client_secret}
                    type="text"
                    name="client_secret"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("client_secret").required}
                  />
                )}

                {field("secret_key").exists && (
                  <InputField
                    label="Secret Key"
                    value={payload.secret_key}
                    type="text"
                    name="secret_key"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("secret_key").required}
                  />
                )}

                {field("track_api_key").exists && (
                  <InputField
                    label="Track API Key"
                    value={payload.track_api_key}
                    name="track_api_key"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("track_api_key").required}
                  />
                )}

                {field("track_secret_key").exists && (
                  <InputField
                    label="Track API secret Key"
                    value={payload.track_secret_key}
                    type="text"
                    name="track_secret_key"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("track_secret_key").required}
                  />
                )}

                {field("customer_number").exists && (
                  <InputField
                    label="Customer Number"
                    value={payload.customer_number}
                    name="customer_number"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("customer_number").required}
                  />
                )}

                {field("license_key").exists && (
                  <InputField
                    label="License Key"
                    value={payload.license_key}
                    name="license_key"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("license_key").required}
                  />
                )}

                {field("consumer_key").exists && (
                  <InputField
                    label="Consumer Key"
                    value={payload.consumer_key}
                    name="consumer_key"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("consumer_key").required}
                  />
                )}

                {field("tracking_consumer_key").exists && (
                  <InputField
                    label="Tracking API consumer key"
                    value={payload.tracking_consumer_key}
                    name="tracking_consumer_key"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("tracking_consumer_key").required}
                  />
                )}

                {field("consumer_secret").exists && (
                  <InputField
                    label="Consumer Secret"
                    value={payload.consumer_secret}
                    type="text"
                    name="consumer_secret"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("consumer_secret").required}
                  />
                )}

                {field("tracking_consumer_secret").exists && (
                  <InputField
                    label="Tracking API consumer secret"
                    value={payload.tracking_consumer_secret}
                    type="text"
                    name="tracking_consumer_secret"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("tracking_consumer_secret").required}
                  />
                )}

                {field("contract_id").exists && (
                  <InputField
                    label="Contract Id"
                    value={payload.contract_id}
                    name="contract_id"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("contract_id").required}
                  />
                )}

                {field("api_secret").exists && (
                  <InputField
                    label="API Secret"
                    value={payload.api_secret}
                    type="text"
                    name="api_secret"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("api_secret").required}
                  />
                )}

                {field("account_number").exists && (
                  <InputField
                    label="Account Number"
                    value={payload.account_number}
                    name="account_number"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("account_number").required}
                  />
                )}

                {field("account").exists && (
                  <InputField
                    label="Account"
                    value={payload.account}
                    name="account"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("account").required}
                  />
                )}

                {field("service_type").exists && (
                  <InputField
                    label="Service type"
                    value={payload.service_type}
                    name="service_type"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("service_type").required}
                  />
                )}

                {field("billing_account").exists && (
                  <InputField
                    label="Billing Account"
                    value={payload.billing_account}
                    name="billing_account"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("billing_account").required}
                  />
                )}

                {field("meter_number").exists && (
                  <InputField
                    label="Meter Number"
                    value={payload.meter_number}
                    name="meter_number"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("meter_number").required}
                  />
                )}

                {field("user_key").exists && (
                  <InputField
                    label="User Key"
                    value={payload.user_key}
                    name="user_key"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("user_key").required}
                  />
                )}

                {field("user_token").exists && (
                  <InputField
                    label="User Token"
                    value={payload.user_token}
                    name="user_token"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("user_token").required}
                  />
                )}

                {field("account_pin").exists && (
                  <InputField
                    label="Account Pin"
                    value={payload.account_pin}
                    name="account_pin"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("account_pin").required}
                  />
                )}

                {field("account_entity").exists && (
                  <InputField
                    label="Account Entity"
                    value={payload.account_entity}
                    name="account_entity"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("account_entity").required}
                  />
                )}

                {field("depot").exists && (
                  <InputField
                    label="Depot"
                    value={payload.depot}
                    name="depot"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("depot").required}
                  />
                )}

                {field("mailer_id").exists && (
                  <InputField
                    label="Mailer ID"
                    value={payload.mailer_id}
                    name="mailer_id"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("mailer_id").required}
                  />
                )}

                {field("customer_registration_id").exists && (
                  <InputField
                    label="Customer Registration ID"
                    value={payload.customer_registration_id}
                    name="customer_registration_id"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("customer_registration_id").required}
                  />
                )}

                {field("logistics_manager_mailer_id").exists && (
                  <InputField
                    label="Logistics Manager Mailer ID"
                    value={payload.logistics_manager_mailer_id}
                    name="logistics_manager_mailer_id"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("logistics_manager_mailer_id").required}
                  />
                )}

                {field("access_key").exists && (
                  <InputField
                    label="Access Key"
                    value={payload.access_key}
                    name="access_key"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("access_key").required}
                  />
                )}

                {field("aws_region").exists && (
                  <InputField
                    label="AWS Region"
                    value={payload.aws_region}
                    name="aws_region"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("aws_region").required}
                  />
                )}

                {field("mws_auth_token").exists && (
                  <InputField
                    label="MWS Auth Token"
                    value={payload.mws_auth_token}
                    name="mws_auth_token"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("mws_auth_token").required}
                  />
                )}

                {field("account_code").exists && (
                  <InputField
                    label="Account code"
                    value={payload.account_code}
                    name="account_code"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("account_code").required}
                  />
                )}

                {field("toll_username").exists && (
                  <InputField
                    label="TOLL username"
                    value={payload.toll_username}
                    name="toll_username"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("toll_username").required}
                  />
                )}

                {field("toll_password").exists && (
                  <InputField
                    label="TOLL password"
                    value={payload.toll_password}
                    name="toll_password"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("toll_password").required}
                  />
                )}

                {field("my_toll_identity").exists && (
                  <InputField
                    label="My TOLL identity"
                    value={payload.my_toll_identity}
                    name="my_toll_identity"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small"
                    required={field("my_toll_identity").required}
                  />
                )}

                {field("my_toll_token").exists && (
                  <TextAreaField
                    label="My TOLL token"
                    value={payload.my_toll_token}
                    rows={2}
                    name="my_toll_token"
                    onChange={handleChange}
                    className="is-small"
                    fieldClass="pt-2"
                    required={field("my_toll_token").required}
                  />
                )}

                {field("lang").exists && (
                  <SelectField
                    value={payload.lang}
                    label="Lang"
                    name="lang"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small is-fullwidth"
                    required={field("lang").required}
                  >
                    {!field("lang").required && <option value="none"></option>}
                    <option value="en_EN">en_EN</option>
                    <option value="fr_FR">fr_FR</option>
                  </SelectField>
                )}

                {field("language").exists && (
                  <SelectField
                    value={payload.language}
                    label="Language"
                    name="language"
                    wrapperClass="pt-2"
                    onChange={handleChange}
                    className="is-small is-fullwidth"
                    required={field("language").required}
                  >
                    {!field("language").required && (
                      <option value="none"></option>
                    )}
                    <option value="en">en</option>
                    <option value="fr">fr</option>
                  </SelectField>
                )}

                {field("account_country_code").exists && (
                  <CountryInput
                    label="Account Country Code"
                    onValueChange={directChange("account_country_code")}
                    value={payload.account_country_code}
                    className="is-small"
                    dropdownClass="is-small"
                    wrapperClass="pt-2"
                    required={field("account_country_code").required}
                  />
                )}

                {/* Carrier config section */}

                {carrier_name.toString() in (connection_configs || {}) && (
                  <div className="mt-4">
                    <Disclosure>
                      {({ open }) => (
                        <div className="block">
                          <Disclosure.Button
                            as="div"
                            style={{ boxShadow: "none" }}
                            className="is-flex is-justify-content-space-between is-clickable px-0 mb-2"
                          >
                            <h2 className="title is-6 my-3">
                              Connection Config
                            </h2>
                            <span className="icon is-small m-2 mt-3">
                              {open ? (
                                <i className="fas fa-chevron-up"></i>
                              ) : (
                                <i className="fas fa-chevron-down"></i>
                              )}
                            </span>
                          </Disclosure.Button>
                          <Disclosure.Panel className="card is-flat columns is-multiline m-0">
                            {"cost_center" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.config?.cost_center || ""}
                                name="cost_center"
                                label="Cost center"
                                onChange={handleConfigChange}
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                              />
                            )}

                            {"sub_account" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.config?.sub_account || ""}
                                name="sub_account"
                                label="Sub account"
                                onChange={handleConfigChange}
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                              />
                            )}

                            {"processing_location" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.config?.cost_center || ""}
                                name="processing_location"
                                label="Processing location"
                                onChange={handleConfigChange}
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                              />
                            )}

                            {"language_code" in
                              connection_configs[carrier_name.toString()] && (
                              <SelectField
                                value={payload.config?.language_code}
                                name="language_code"
                                label="language code"
                                onChange={handleConfigChange}
                                className="is-small is-fullwidth"
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                              >
                                <option value="none"></option>
                                <option value="en">en</option>
                                <option value="fr">fr</option>
                              </SelectField>
                            )}

                            {"label_type" in
                              connection_configs[carrier_name.toString()] && (
                              <SelectField
                                value={payload.config?.label_type}
                                name="label_type"
                                label="Default label type"
                                onChange={handleConfigChange}
                                className="is-small is-fullwidth"
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                              >
                                <option value="none"></option>
                                {LABEL_TYPES.map((_) => (
                                  <option key={_} value={_}>
                                    {_}
                                  </option>
                                ))}
                              </SelectField>
                            )}

                            {"smart_post_hub_id" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.config?.smart_post_hub_id || ""}
                                name="smart_post_hub_id"
                                label="Smart Post Hub ID"
                                onChange={handleConfigChange}
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                              />
                            )}

                            {"enforce_zpl" in
                              connection_configs[carrier_name.toString()] && (
                              <div className="field column is-6 mb-0">
                                <div className="control">
                                  <label className="checkbox has-text-weight-bold mt-5 pt-1">
                                    <input
                                      type="checkbox"
                                      checked={payload.config?.enforce_zpl}
                                      name="enforce_zpl"
                                      onChange={handleConfigChange}
                                    />{" "}
                                    <span style={{ fontSize: "0.8em" }}>
                                      Always use ZPL
                                    </span>
                                  </label>
                                </div>
                              </div>
                            )}

                            {"transmit_shipment_by_default" in
                              connection_configs[carrier_name.toString()] && (
                              <div className="field column is-6 mb-0">
                                <div className="control">
                                  <label className="checkbox has-text-weight-bold mt-3 pt-1">
                                    <input
                                      type="checkbox"
                                      checked={
                                        payload.config
                                          ?.transmit_shipment_by_default
                                      }
                                      name="transmit_shipment_by_default"
                                      onChange={handleConfigChange}
                                    />{" "}
                                    <span style={{ fontSize: "0.8em" }}>
                                      Submit shipment by default
                                    </span>
                                  </label>
                                </div>
                              </div>
                            )}

                            {"skip_service_filter" in
                              connection_configs[carrier_name.toString()] && (
                              <div className="field column is-6 mb-0">
                                <div className="control">
                                  <label className="checkbox has-text-weight-bold mt-5 pt-1">
                                    <input
                                      type="checkbox"
                                      checked={
                                        payload.config?.skip_service_filter
                                      }
                                      name="skip_service_filter"
                                      onChange={handleConfigChange}
                                    />{" "}
                                    <span style={{ fontSize: "0.8em" }}>
                                      Disable service filter
                                    </span>
                                  </label>
                                </div>
                              </div>
                            )}

                            {"service_suffix" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.config?.service_suffix || ""}
                                name="service_suffix"
                                label="Fixed service suffix"
                                onChange={handleConfigChange}
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                              />
                            )}

                            {"business_id" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.config?.business_id || ""}
                                name="business_id"
                                label="Business ID"
                                onChange={handleConfigChange}
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                              />
                            )}

                            {"SYSID" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.config?.SYSID || ""}
                                name="SYSID"
                                label="TOLL SYSID"
                                onChange={handleConfigChange}
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                              />
                            )}

                            {"SHIP_GS1" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.config?.SHIP_GS1 || ""}
                                name="SHIP_GS1"
                                label="TOLL SHIP_GS1"
                                onChange={handleConfigChange}
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                              />
                            )}

                            {"SHIP_range_start" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.config?.SHIP_range_start || ""}
                                type="number"
                                step={1}
                                name="SHIP_range_start"
                                label="TOLL SHIP range start"
                                onChange={handleConfigChange}
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                              />
                            )}

                            {"SHIP_range_end" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.config?.SHIP_range_end || ""}
                                type="number"
                                step={1}
                                name="SHIP_range_end"
                                label="TOLL SHIP range end"
                                onChange={handleConfigChange}
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                              />
                            )}

                            {"SSCC_GS1" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.config?.SSCC_GS1 || ""}
                                name="SSCC_GS1"
                                label="TOLL SSCC_GS1"
                                onChange={handleConfigChange}
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                              />
                            )}

                            {"SSCC_range_start" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.config?.SSCC_range_start || ""}
                                type="number"
                                step={1}
                                name="SSCC_range_start"
                                label="TOLL SSCC range start"
                                onChange={handleConfigChange}
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                              />
                            )}

                            {"SSCC_range_end" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.config?.SSCC_range_end || ""}
                                type="number"
                                step={1}
                                name="SSCC_range_end"
                                label="TOLL SSCC range end"
                                onChange={handleConfigChange}
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                              />
                            )}

                            {"channel" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.config?.channel || ""}
                                name="channel"
                                label="Channel"
                                onChange={handleConfigChange}
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                              />
                            )}

                            {"freight_mode" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.config?.freight_mode || ""}
                                name="freight_mode"
                                label="Freight mode"
                                onChange={handleConfigChange}
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                              />
                            )}

                            {"message_sender" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.config?.message_sender || ""}
                                name="message_sender"
                                label="Message sender"
                                onChange={handleConfigChange}
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                              />
                            )}

                            {"brand_color" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.config?.brand_color || ""}
                                type="color"
                                name="brand_color"
                                label="Brand color"
                                onChange={handleConfigChange}
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                              />
                            )}

                            {"text_color" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.config?.text_color || ""}
                                type="color"
                                name="text_color"
                                label="Text color"
                                onChange={handleConfigChange}
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                              />
                            )}

                            {"account_service_type" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.account_service_type}
                                name="account_service_type"
                                label="Account service type"
                                onChange={handleConfigChange}
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                              />
                            )}

                            {"server_url" in
                              connection_configs[carrier_name.toString()] && (
                              <InputField
                                value={payload.config?.server_url || ""}
                                name="server_url"
                                label="Custom server URL"
                                onChange={handleConfigChange}
                                wrapperClass="column is-12 pt-1"
                                fieldClass="mb-0"
                                className="is-small is-fullwidth"
                                placeholder="https://your-instance.api.com.au"
                              />
                            )}

                            {"rate_request_types" in
                              connection_configs[carrier_name.toString()] && (
                              <SelectField
                                value={payload.config?.rate_request_types}
                                name="rate_request_types"
                                label="Rate request types"
                                onChange={handleConfigChange}
                                className="is-small is-fullwidth"
                                wrapperClass="column is-6 pt-1"
                                fieldClass="mb-0"
                                size={3}
                                multiple
                              >
                                <option value="none"></option>
                                <option value="LIST">LIST</option>
                                <option value="PREFERRED">PREFERRED</option>
                                <option value="INCENTIVE">INCENTIVE</option>
                                <option value="ACCOUNT">ACCOUNT</option>
                              </SelectField>
                            )}

                            {"shipping_services" in
                              connection_configs[carrier_name.toString()] && (
                              <SelectField
                                defaultValue={payload.config?.shipping_services}
                                name="shipping_services"
                                label="Preferred shipping services"
                                className="is-small is-multiple is-fullwidth"
                                wrapperClass="column is-12 pt-1"
                                fieldClass="mb-0"
                                onChange={handleConfigChange}
                                size={6}
                                multiple
                              >
                                {Object.entries(
                                  service_names[carrier_name.toString()] || {},
                                ).map(([_, __]) => (
                                  <option key={_} value={_}>
                                    {__}
                                  </option>
                                ))}
                              </SelectField>
                            )}

                            {"shipping_options" in
                              connection_configs[carrier_name.toString()] && (
                              <SelectField
                                defaultValue={payload.config?.shipping_options}
                                name="shipping_options"
                                label={`Enable carrier specific shipping options`}
                                className="is-small is-multiple is-fullwidth"
                                wrapperClass="column is-12 pt-1"
                                fieldClass="mb-0"
                                onChange={handleConfigChange}
                                size={6}
                                multiple
                              >
                                {Object.entries(
                                  option_names[carrier_name.toString()] || {},
                                ).map(([_, __]) => (
                                  <option key={_} value={_}>
                                    {__}
                                  </option>
                                ))}
                              </SelectField>
                            )}
                          </Disclosure.Panel>
                        </div>
                      )}
                    </Disclosure>
                  </div>
                )}

                {/* Carrier specific fields END */}

                <hr className="mt-5 mb-3" style={{ height: "1px" }} />

                <MetadataEditor
                  object_type={MetadataObjectTypeEnum.carrier}
                  metadata={payload.metadata}
                  onChange={directChange("metadata")}
                >
                  <MetadataEditorContext.Consumer>
                    {({ isEditing, editMetadata }) => (
                      <>
                        <div className="is-flex is-justify-content-space-between">
                          <h2 className="title is-6 my-3">Metadata</h2>

                          <button
                            type="button"
                            className="button is-default is-small is-align-self-center"
                            disabled={isEditing}
                            onClick={() => editMetadata()}
                          >
                            <span className="icon is-small">
                              <i className="fas fa-pen"></i>
                            </span>
                            <span>Edit metadata</span>
                          </button>
                        </div>

                        <hr className="mt-1 my-1" style={{ height: "1px" }} />
                      </>
                    )}
                  </MetadataEditorContext.Consumer>
                </MetadataEditor>

                <div className="p-3 my-5"></div>
                <div className="form-floating-footer has-text-centered p-1">
                  <button
                    className="button is-default m-1 is-small"
                    onClick={close}
                    disabled={loading}
                  >
                    <span>Cancel</span>
                  </button>
                  <button
                    className={`button is-primary ${loading ? "is-loading" : ""} m-1 is-small`}
                    disabled={
                      isInvalid ||
                      isEqual(operation.connection || DEFAULT_STATE, payload)
                    }
                    type="submit"
                  >
                    <span>Submit</span>
                  </button>
                </div>
              </>
            )}
          </section>
        </form>
        <button
          className="modal-close is-large has-background-dark"
          aria-label=""
          onClick={close}
        ></button>
      </div>
    </Notifier>
  );
};

function fieldState(carrier_name: CarrierNameType, property: string) {
  const field =
    (
      {
        [CarrierSettingsCarrierNameEnum.AlliedExpress]: [
          ["carrier_id", true],
          ["username", true],
          ["password", true],
          ["account", false],
          ["service_type", false],
        ],
        [CarrierSettingsCarrierNameEnum.AlliedExpressLocal]: [
          ["carrier_id", true],
          ["username", true],
          ["password", true],
          ["account", false],
          ["service_type", false],
        ],
        [CarrierSettingsCarrierNameEnum.AmazonShipping]: [
          ["carrier_id", true],
          ["seller_id", true],
          ["developer_id", true],
          ["mws_auth_token", true],
          ["aws_region"],
        ],
        [CarrierSettingsCarrierNameEnum.Aramex]: [
          ["carrier_id", true],
          ["username", true],
          ["password", true],
          ["account_pin", true],
          ["account_entity", true],
          ["account_number", true],
          ["account_country_code"],
        ],
        [CarrierSettingsCarrierNameEnum.Australiapost]: [
          ["carrier_id", true],
          ["api_key", true],
          ["password", true],
          ["account_number", true],
        ],
        [CarrierSettingsCarrierNameEnum.AsendiaUs]: [
          ["carrier_id", true],
          ["username", true],
          ["password", true],
          ["api_key", true],
          ["account_number", true],
        ],
        [CarrierSettingsCarrierNameEnum.Boxknight]: [
          ["carrier_id", true],
          ["username", true],
          ["password", true],
        ],
        [CarrierSettingsCarrierNameEnum.Bpost]: [
          ["carrier_id", true],
          ["account_id", true],
          ["passphrase", true],
        ],
        [CarrierSettingsCarrierNameEnum.Canadapost]: [
          ["carrier_id", true],
          ["username", true],
          ["password", true],
          ["customer_number"],
          ["contract_id"],
        ],
        [CarrierSettingsCarrierNameEnum.Canpar]: [
          ["carrier_id", true],
          ["username", true],
          ["password", true],
        ],
        [CarrierSettingsCarrierNameEnum.Chronopost]: [
          ["carrier_id", true],
          ["account_number", true],
          ["password", true],
          ["account_country_code"],
        ],
        [CarrierSettingsCarrierNameEnum.Colissimo]: [
          ["carrier_id", true],
          ["contract_number", true],
          ["password", true],
          ["laposte_api_key"],
        ],
        [CarrierSettingsCarrierNameEnum.Dicom]: [
          ["carrier_id", true],
          ["username", true],
          ["password", true],
          ["billing_account"],
        ],
        [CarrierSettingsCarrierNameEnum.Dpd]: [
          ["carrier_id", true],
          ["delis_id", true],
          ["password", true],
          ["depot"],
          ["account_country_code"],
        ],
        [CarrierSettingsCarrierNameEnum.DhlParcelDe]: [
          ["carrier_id", true],
          ["username", true],
          ["password", true],
          ["dhl_api_key", true],
          ["customer_number"],
          ["tracking_consumer_key"],
          ["tracking_consumer_secret"],
        ],
        [CarrierSettingsCarrierNameEnum.Dpdhl]: [
          ["carrier_id", true],
          ["username", true],
          ["password", true],
          ["app_id"],
          ["app_token"],
          ["zt_id"],
          ["zt_password"],
          ["account_number"],
        ],
        [CarrierSettingsCarrierNameEnum.DhlExpress]: [
          ["carrier_id", true],
          ["site_id", true],
          ["password", true],
          ["account_number", true],
          ["account_country_code"],
        ],
        [CarrierSettingsCarrierNameEnum.DhlPoland]: [
          ["carrier_id", true],
          ["username", true],
          ["password", true],
          ["account_number", true],
        ],
        [CarrierSettingsCarrierNameEnum.DhlUniversal]: [
          ["carrier_id", true],
          ["consumer_key", true],
          ["consumer_secret", true],
        ],
        [CarrierSettingsCarrierNameEnum.Eshipper]: [
          ["carrier_id", true],
          ["principal", true],
          ["credential", true],
        ],
        [CarrierSettingsCarrierNameEnum.Easypost]: [
          ["carrier_id", true],
          ["api_key", true],
        ],
        [CarrierSettingsCarrierNameEnum.Freightcom]: [
          ["carrier_id", true],
          ["username", true],
          ["password", true],
        ],
        [CarrierSettingsCarrierNameEnum.Generic]: [
          ["display_name", true],
          ["custom_carrier_name", true],
          ["carrier_id", true],
          ["account_number"],
          ["account_country_code"],
        ],
        [CarrierSettingsCarrierNameEnum.Geodis]: [
          ["carrier_id", true],
          ["identifier", true],
          ["api_key", true],
          ["language", false, "fr"],
        ],
        [CarrierSettingsCarrierNameEnum.Laposte]: [
          ["carrier_id", true],
          ["api_key", true],
          ["lang", false, "fr_FR"],
        ],
        [CarrierSettingsCarrierNameEnum.Locate2u]: [
          ["carrier_id", true],
          ["client_id", true],
          ["client_secret", true],
          ["account_country_code"],
        ],
        [CarrierSettingsCarrierNameEnum.Nationex]: [
          ["carrier_id", true],
          ["api_key", true],
          ["customer_id", true],
          ["billing_account"],
          ["language", false, "en"],
        ],
        [CarrierSettingsCarrierNameEnum.Roadie]: [
          ["carrier_id", true],
          ["api_key", true],
        ],
        [CarrierSettingsCarrierNameEnum.Fedex]: [
          ["carrier_id", true],
          ["api_key"],
          ["secret_key"],
          ["track_api_key"],
          ["track_secret_key"],
          ["account_number"],
          ["account_country_code"],
        ],
        [CarrierSettingsCarrierNameEnum.FedexWs]: [
          ["carrier_id", true],
          ["user_key"],
          ["password", true],
          ["meter_number", true],
          ["account_number", true],
          ["account_country_code"],
        ],
        [CarrierSettingsCarrierNameEnum.Purolator]: [
          ["carrier_id", true],
          ["username", true],
          ["password", true],
          ["account_number", true],
          ["user_token"],
        ],
        [CarrierSettingsCarrierNameEnum.Royalmail]: [
          ["carrier_id", true],
          ["client_id", true],
          ["client_secret", true],
        ],
        [CarrierSettingsCarrierNameEnum.Sendle]: [
          ["carrier_id", true],
          ["sendle_id", true],
          ["api_key", true],
          ["account_country_code"],
        ],
        [CarrierSettingsCarrierNameEnum.Tge]: [
          ["carrier_id", true],
          ["username", true],
          ["password", true],
          ["api_key", true],
          ["toll_username", true],
          ["toll_password", true],
          ["account_code", true],
          ["my_toll_token", true],
          ["my_toll_identity", true],
        ],
        [CarrierSettingsCarrierNameEnum.Tnt]: [
          ["carrier_id", true],
          ["username", true],
          ["password", true],
          ["account_number"],
          ["account_country_code"],
        ],
        [CarrierSettingsCarrierNameEnum.Ups]: [
          ["carrier_id", true],
          ["client_id", true],
          ["client_secret", true],
          ["account_number", true],
          ["account_country_code"],
        ],
        [CarrierSettingsCarrierNameEnum.Usps]: [
          ["carrier_id", true],
          ["username", true],
          ["password", true],
          ["mailer_id"],
          ["customer_registration_id"],
          ["logistics_manager_mailer_id"],
        ],
        [CarrierSettingsCarrierNameEnum.UspsInternational]: [
          ["carrier_id", true],
          ["username", true],
          ["password", true],
          ["mailer_id"],
          ["customer_registration_id"],
          ["logistics_manager_mailer_id"],
        ],
        [CarrierSettingsCarrierNameEnum.Zoom2u]: [
          ["carrier_id", true],
          ["api_key", true],
          ["account_country_code"],
        ],
        [NoneEnum.none]: [],
      }[carrier_name] || []
    ).find(([_, ...__]) => _ === property) || [];

  return {
    get exists() {
      return field[0] !== undefined;
    },
    get required() {
      return field[1] === true;
    },
    get default() {
      return field[2];
    },
  };
}

export function useConnectCarrierModal() {
  return useContext(ConnectProviderModalContext);
}
