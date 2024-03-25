import { useWorkspaceConfig, useWorkspaceConfigMutation } from "@karrio/hooks/workspace-config";
import { COUNTRY_OPTIONS, CURRENCY_OPTIONS, GetWorkspaceConfig_workspace_config } from "@karrio/types";
import { InputField, SelectField } from "../components";
import { isNoneOrEmpty } from "@karrio/lib";
import React from "react";
import { useUser } from "@karrio/hooks/user";

type WorkspaceConfigFormProps = {
  pageProps?: { workspace_config?: GetWorkspaceConfig_workspace_config } | any;
};


function reducer(state: GetWorkspaceConfig_workspace_config, { name, value }: { name: string, value: string | boolean | object | null | Partial<GetWorkspaceConfig_workspace_config> }): GetWorkspaceConfig_workspace_config {
  switch (name) {
    case "full":
      return { ...(value as GetWorkspaceConfig_workspace_config) };
    case "partial":
      return { ...state, ...(value as object) };
    default:
      return { ...state, [name]: value };
  }
}


export const WorkspaceConfigForm: React.FC<WorkspaceConfigFormProps> = ({ pageProps }) => {
  const mutation = useWorkspaceConfigMutation();
  const { query: { data: { user } = {} } } = useUser();
  const [payload, dispatch] = React.useReducer(reducer, pageProps?.workspace_config, () => pageProps?.workspace_config || {});
  const { query: { data: { workspace_config } = {}, ...query } } = useWorkspaceConfig({ defaultValue: pageProps?.workspace_config });

  const onChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name: string = target.name;

    dispatch({ name, value: value === 'none' || isNoneOrEmpty(value) ? null : value });
  };

  return (
    <>


      {/* General preferences section */}
      <div className="columns py-6 my-4">
        <div className="column is-5 pr-2">
          <p className="subtitle is-6 py-1">General defaults</p>
          <p className="is-size-7 pr-2">Set up preferences for your {pageProps?.APP_NAME || ""} account.</p>
        </div>

        <div className="column is-4">

          {/* currency */}
          <SelectField name="default_currency"
            label="Default Currency"
            wrapperClass="py-2"
            disabled={!(user?.permissions || []).includes("manage_team")}
            controlClass="is-expanded"
            className="is-small is-fullwidth"
            fieldClass={`column mb-0 p-0 ${(payload.default_currency !== workspace_config?.default_currency) ? 'is-12 is-grouped' : 'is-10'}`}
            value={payload?.default_currency || ''}
            onChange={onChange}
            addonRight={<>
              {(payload.default_currency !== workspace_config?.default_currency) &&
                <div className="buttons">
                  <button
                    onClick={() => dispatch({ name: "default_currency", value: workspace_config!.default_currency })}
                    className="button is-small is-default">
                    cancel
                  </button>
                  <button
                    onClick={() => mutation.updateWorkspaceConfig.mutateAsync({ default_currency: payload.default_currency })}
                    className={`button is-small is-success ${mutation.updateWorkspaceConfig.isLoading ? 'is-loading' : ''}`}>
                    save
                  </button>
                </div>}
            </>}
          >
            <option value="none">Select a currency</option>
            {CURRENCY_OPTIONS.map(unit => <option key={unit} value={unit}>{unit}</option>)}
          </SelectField>

          {/* country */}
          <SelectField name="default_country_code"
            label="Default Country"
            wrapperClass="py-2"
            disabled={!(user?.permissions || []).includes("manage_team")}
            controlClass="is-expanded"
            className="is-small is-fullwidth"
            fieldClass={`column mb-0 p-0 ${(payload.default_country_code !== workspace_config?.default_country_code) ? 'is-12 is-grouped' : 'is-10'}`}
            value={payload?.default_country_code || ''}
            onChange={onChange}
            addonRight={<>
              {(payload.default_country_code !== workspace_config?.default_country_code) &&
                <div className="buttons">
                  <button
                    onClick={() => dispatch({ name: "default_country", value: workspace_config!.default_country_code })}
                    className="button is-small is-default">
                    cancel
                  </button>
                  <button

                    onClick={() => mutation.updateWorkspaceConfig.mutateAsync({ default_country_code: payload.default_country_code })}
                    className={`button is-small is-success ${mutation.updateWorkspaceConfig.isLoading ? 'is-loading' : ''}`}>
                    save
                  </button>
                </div>}
            </>}
          >
            <option value="none">Select a country</option>
            {COUNTRY_OPTIONS.map(unit => <option key={unit} value={unit}>{unit}</option>)}
          </SelectField>

          {/* label type */}
          <SelectField name="default_label_type"
            label="Default Label Type"
            wrapperClass="py-2"
            disabled={!(user?.permissions || []).includes("manage_team")}
            controlClass="is-expanded"
            className="is-small is-fullwidth"
            fieldClass={`column mb-0 p-0 ${(payload.default_label_type !== workspace_config?.default_label_type) ? 'is-12 is-grouped' : 'is-10'}`}
            value={payload?.default_label_type || ''}
            onChange={onChange}
            addonRight={<>
              {(payload.default_label_type !== workspace_config?.default_label_type) &&
                <div className="buttons">
                  <button
                    onClick={() => dispatch({ name: "default_label_type", value: workspace_config!.default_label_type })}
                    className="button is-small is-default">
                    cancel
                  </button>
                  <button

                    onClick={() => mutation.updateWorkspaceConfig.mutateAsync({ default_label_type: payload.default_label_type })}
                    className={`button is-small is-success ${mutation.updateWorkspaceConfig.isLoading ? 'is-loading' : ''}`}>
                    save
                  </button>
                </div>}
            </>}
          >
            <option value="none">Select a label type</option>
            <option value="PDF">PDF</option>
            <option value="ZPL">ZPL</option>
          </SelectField>

          {/* Weight units */}
          <SelectField name="default_weight_unit"
            label="Default Size Unit"
            wrapperClass="py-2"
            disabled={!(user?.permissions || []).includes("manage_team")}
            controlClass="is-expanded"
            className="is-small is-fullwidth"
            fieldClass={`column mb-0 p-0 ${(payload.default_weight_unit !== workspace_config?.default_weight_unit) ? 'is-12 is-grouped' : 'is-10'}`}
            value={payload?.default_weight_unit || ''}
            onChange={e => {
              const value = (e.target.value === 'none' || isNoneOrEmpty(e.target.value) ? null : e.target.value);
              dispatch({
                name: "partial", value: {
                  default_weight_unit: value,
                  default_dimension_unit: !!value ? value === 'LB' ? 'IN' : 'CM' : null
                }
              });
            }}
            addonRight={<>
              {(payload.default_weight_unit !== workspace_config?.default_weight_unit) &&
                <div className="buttons">
                  <button
                    onClick={() => dispatch({
                      name: "partial", value: {
                        default_weight_unit: workspace_config!.default_weight_unit,
                        default_dimension_unit: workspace_config!.default_dimension_unit
                      }
                    })}
                    className="button is-small is-default">
                    cancel
                  </button>
                  <button
                    onClick={() => mutation.updateWorkspaceConfig.mutateAsync({
                      default_weight_unit: payload.default_weight_unit,
                      default_dimension_unit: payload.default_dimension_unit
                    })}
                    className={`button is-small is-success ${mutation.updateWorkspaceConfig.isLoading ? 'is-loading' : ''}`}>
                    save
                  </button>
                </div>}
            </>}
          >
            <option value="none">Select a weight unit</option>
            <option value="LB">LB/IN</option>
            <option value="KG">KG/CM</option>
          </SelectField>

        </div>

        <div className="column is-3"></div>
      </div>

      <hr style={{ height: '1px' }} />

      {/* Tax identifers */}
      <div className="columns py-6 my-4">
        <div className="column is-5 pr-2">
          <p className="subtitle is-6 py-1">Shipping Tax identifiers</p>
          <p className="is-size-7 pr-2">Set up tax identifiers for your account.</p>
        </div>

        <div className="column is-4">

          {/* State Tax ID */}
          <InputField name="state_tax_id"
            label="State Tax ID"
            wrapperClass="py-2"
            disabled={!(user?.permissions || []).includes("manage_team")}
            className="is-small"
            controlClass="is-expanded"
            fieldClass={`column mb-0 p-0 ${(payload.state_tax_id !== workspace_config?.state_tax_id) ? 'is-12 is-grouped' : 'is-10'}`}
            defaultValue={payload?.state_tax_id || ""}
            onChange={onChange}
            addonRight={<>
              {(payload.state_tax_id !== workspace_config?.state_tax_id) &&
                <div className="buttons">
                  <button
                    onClick={() => dispatch({ name: "tax_id", value: workspace_config!.state_tax_id })}
                    className="button is-small is-default">
                    cancel
                  </button>
                  <button

                    onClick={() => mutation.updateWorkspaceConfig.mutateAsync({ state_tax_id: payload.state_tax_id })}
                    className={`button is-small is-success ${mutation.updateWorkspaceConfig.isLoading ? 'is-loading' : ''}`}>
                    save
                  </button>
                </div>}
            </>}
          />

          {/* Federal Tax ID */}
          <InputField name="federal_tax_id"
            label="Federal Tax ID"
            wrapperClass="py-2"
            disabled={!(user?.permissions || []).includes("manage_team")}
            className="is-small"
            controlClass="is-expanded"
            fieldClass={`column mb-0 p-0 ${(payload.federal_tax_id !== workspace_config?.federal_tax_id) ? 'is-12 is-grouped' : 'is-10'}`}
            defaultValue={payload?.federal_tax_id || ""}
            onChange={onChange}
            addonRight={<>
              {(payload.federal_tax_id !== workspace_config?.federal_tax_id) &&
                <div className="buttons">
                  <button
                    onClick={() => dispatch({ name: "federal_tax_id", value: workspace_config!.federal_tax_id })}
                    className="button is-small is-default">
                    cancel
                  </button>
                  <button

                    onClick={() => mutation.updateWorkspaceConfig.mutateAsync({ federal_tax_id: payload.federal_tax_id })}
                    className={`button is-small is-success ${mutation.updateWorkspaceConfig.isLoading ? 'is-loading' : ''}`}>
                    save
                  </button>
                </div>}
            </>}
          />

        </div>

      </div>

      <hr style={{ height: '1px' }} />

      {/* Customs declaration identifier section */}
      <div className="columns py-6 my-4">
        <div className="column is-5 pr-2">
          <p className="subtitle is-6 py-1">Shipping Customs identifiers</p>
          <p className="is-size-7 pr-2">Spee up customs declaration for international shipments.</p>
        </div>

        <div className="column is-4">

          {/* AES */}
          <InputField name="customs_aes"
            label="AES"
            wrapperClass="py-2"
            disabled={!(user?.permissions || []).includes("manage_team")}
            className="is-small"
            controlClass="is-expanded"
            fieldClass={`column mb-0 p-0 ${(payload.customs_aes !== workspace_config?.customs_aes) ? 'is-12 is-grouped' : 'is-10'}`}
            defaultValue={payload?.customs_aes || ""}
            onChange={onChange}
            addonRight={<>
              {(payload.customs_aes !== workspace_config?.customs_aes) &&
                <div className="buttons">
                  <button
                    onClick={() => dispatch({ name: "customs_aes", value: workspace_config!.customs_aes })}
                    className="button is-small is-default">
                    cancel
                  </button>
                  <button

                    onClick={() => mutation.updateWorkspaceConfig.mutateAsync({ customs_aes: payload.customs_aes })}
                    className={`button is-small is-success ${mutation.updateWorkspaceConfig.isLoading ? 'is-loading' : ''}`}>
                    save
                  </button>
                </div>}
            </>}
          />

          {/* EEL/PFC */}
          <InputField name="customs_eel_pfc"
            label="EEL/PFC"
            wrapperClass="py-2"
            disabled={!(user?.permissions || []).includes("manage_team")}
            className="is-small"
            controlClass="is-expanded"
            fieldClass={`column mb-0 p-0 ${(payload.customs_eel_pfc !== workspace_config?.customs_eel_pfc) ? 'is-12 is-grouped' : 'is-10'}`}
            defaultValue={payload?.customs_eel_pfc || ""}
            onChange={onChange}
            addonRight={<>
              {(payload.customs_eel_pfc !== workspace_config?.customs_eel_pfc) &&
                <div className="buttons">
                  <button
                    onClick={() => dispatch({ name: "customs_eel_pfc", value: workspace_config!.customs_eel_pfc })}
                    className="button is-small is-default">
                    cancel
                  </button>
                  <button

                    onClick={() => mutation.updateWorkspaceConfig.mutateAsync({ customs_eel_pfc: payload.customs_eel_pfc })}
                    className={`button is-small is-success ${mutation.updateWorkspaceConfig.isLoading ? 'is-loading' : ''}`}>
                    save
                  </button>
                </div>}
            </>}
          />

          {/* License number */}
          <InputField name="customs_license_number"
            label="License number"
            wrapperClass="py-2"
            disabled={!(user?.permissions || []).includes("manage_team")}
            className="is-small"
            controlClass="is-expanded"
            fieldClass={`column mb-0 p-0 ${(payload.customs_license_number !== workspace_config?.customs_license_number) ? 'is-12 is-grouped' : 'is-10'}`}
            defaultValue={payload?.customs_license_number || ""}
            onChange={onChange}
            addonRight={<>
              {(payload.customs_license_number !== workspace_config?.customs_license_number) &&
                <div className="buttons">
                  <button
                    onClick={() => dispatch({ name: "customs_license_number", value: workspace_config!.customs_license_number })}
                    className="button is-small is-default">
                    cancel
                  </button>
                  <button

                    onClick={() => mutation.updateWorkspaceConfig.mutateAsync({ customs_license_number: payload.customs_license_number })}
                    className={`button is-small is-success ${mutation.updateWorkspaceConfig.isLoading ? 'is-loading' : ''}`}>
                    save
                  </button>
                </div>}
            </>}
          />

          {/* Certificate number */}
          <InputField name="customs_certificate_number"
            label="Certificate number"
            wrapperClass="py-2"
            disabled={!(user?.permissions || []).includes("manage_team")}
            className="is-small"
            controlClass="is-expanded"
            fieldClass={`column mb-0 p-0 ${(payload.customs_certificate_number !== workspace_config?.customs_certificate_number) ? 'is-12 is-grouped' : 'is-10'}`}
            defaultValue={payload?.customs_certificate_number || ""}
            onChange={onChange}
            addonRight={<>
              {(payload.customs_certificate_number !== workspace_config?.customs_certificate_number) &&
                <div className="buttons">
                  <button
                    onClick={() => dispatch({ name: "customs_certificate_number", value: workspace_config!.customs_certificate_number })}
                    className="button is-small is-default">
                    cancel
                  </button>
                  <button

                    onClick={() => mutation.updateWorkspaceConfig.mutateAsync({ customs_certificate_number: payload.customs_certificate_number })}
                    className={`button is-small is-success ${mutation.updateWorkspaceConfig.isLoading ? 'is-loading' : ''}`}>
                    save
                  </button>
                </div>}
            </>}
          />

          {/* NIP number */}
          <InputField name="customs_nip_number"
            label="NIP number"
            wrapperClass="py-2"
            disabled={!(user?.permissions || []).includes("manage_team")}
            className="is-small"
            controlClass="is-expanded"
            fieldClass={`column mb-0 p-0 ${(payload.customs_nip_number !== workspace_config?.customs_nip_number) ? 'is-12 is-grouped' : 'is-10'}`}
            defaultValue={payload?.customs_nip_number || ""}
            onChange={onChange}
            addonRight={<>
              {(payload.customs_nip_number !== workspace_config?.customs_nip_number) &&
                <div className="buttons">
                  <button
                    onClick={() => dispatch({ name: "customs_nip_number", value: workspace_config!.customs_nip_number })}
                    className="button is-small is-default">
                    cancel
                  </button>
                  <button

                    onClick={() => mutation.updateWorkspaceConfig.mutateAsync({ customs_nip_number: payload.customs_nip_number })}
                    className={`button is-small is-success ${mutation.updateWorkspaceConfig.isLoading ? 'is-loading' : ''}`}>
                    save
                  </button>
                </div>}
            </>}
          />

          {/* EORI number */}
          <InputField name="customs_eori_number"
            label="EORI number"
            wrapperClass="py-2"
            disabled={!(user?.permissions || []).includes("manage_team")}
            className="is-small"
            controlClass="is-expanded"
            fieldClass={`column mb-0 p-0 ${(payload.customs_eori_number !== workspace_config?.customs_eori_number) ? 'is-12 is-grouped' : 'is-10'}`}
            defaultValue={payload?.customs_eori_number || ""}
            onChange={onChange}
            addonRight={<>
              {(payload.customs_eori_number !== workspace_config?.customs_eori_number) &&
                <div className="buttons">
                  <button
                    onClick={() => dispatch({ name: "customs_eori_number", value: workspace_config!.customs_eori_number })}
                    className="button is-small is-default">
                    cancel
                  </button>
                  <button

                    onClick={() => mutation.updateWorkspaceConfig.mutateAsync({ customs_eori_number: payload.customs_eori_number })}
                    className={`button is-small is-success ${mutation.updateWorkspaceConfig.isLoading ? 'is-loading' : ''}`}>
                    save
                  </button>
                </div>}
            </>}
          />

          {/* VAT registration number */}
          <InputField name="customs_vat_registration_number"
            label="VAT registration number"
            wrapperClass="py-2"
            disabled={!(user?.permissions || []).includes("manage_team")}
            className="is-small"
            controlClass="is-expanded"
            fieldClass={`column mb-0 p-0 ${(payload.customs_vat_registration_number !== workspace_config?.customs_vat_registration_number) ? 'is-12 is-grouped' : 'is-10'}`}
            defaultValue={payload?.customs_vat_registration_number || ""}
            onChange={onChange}
            addonRight={<>
              {(payload.customs_vat_registration_number !== workspace_config?.customs_vat_registration_number) &&
                <div className="buttons">
                  <button
                    onClick={() => dispatch({ name: "customs_vat_registration_number", value: workspace_config!.customs_vat_registration_number })}
                    className="button is-small is-default">
                    cancel
                  </button>
                  <button

                    onClick={() => mutation.updateWorkspaceConfig.mutateAsync({ customs_vat_registration_number: payload.customs_vat_registration_number })}
                    className={`button is-small is-success ${mutation.updateWorkspaceConfig.isLoading ? 'is-loading' : ''}`}>
                    save
                  </button>
                </div>}
            </>}
          />

        </div>

        <div className="column is-3"></div>
      </div>

    </>
  )
};
