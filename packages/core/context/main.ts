import { AccountContextDataType, Metadata } from "@karrio/types";
import { ServerErrorCode, url$ } from "@karrio/lib";
import { KARRIO_PUBLIC_URL } from "@karrio/lib";
import axios from "axios";

const AUTH_HTTP_CODES = [401, 403, 407];

export async function loadMetadata() {
  const { data: metadata, error } = await axios
    .get<Metadata>(KARRIO_PUBLIC_URL as string)
    .then((res) => ({ data: res.data, error: null }))
    .catch((e) => {
      const code = AUTH_HTTP_CODES.includes(e.response?.status)
        ? ServerErrorCode.API_AUTH_ERROR
        : ServerErrorCode.API_CONNECTION_ERROR;
      return {
        data: null,
        error: {
          code,
          message: `
          Server (${KARRIO_PUBLIC_URL}) unreachable.
          Please make sure that the API is running and reachable.
        `,
        },
      };
    });

  return { metadata, error };
}

export async function loadUserData(session: any, metadata?: Metadata) {
  if (!session || !metadata) return { user: null };

  const { accessToken, orgId, testMode } = session;
  const { data, error } = await axios
    .post<AccountContextDataType>(
      url$`${metadata.HOST || ""}/graphql`,
      { query: ACCOUNT_DATA_QUERY },
      {
        headers: {
          ...(orgId ? { "x-org-id": orgId } : {}),
          ...(testMode ? { "x-test-mode": testMode } : {}),
          authorization: `Bearer ${accessToken}`,
        } as any,
      },
    )
    .then((res) => ({ data: res.data?.data, error: null }))
    .catch((e) => {
      const code = AUTH_HTTP_CODES.includes(e.response?.status)
        ? ServerErrorCode.API_AUTH_ERROR
        : ServerErrorCode.API_CONNECTION_ERROR;
      return {
        data: {},
        error: {
          code,
          message: `
          Server (${metadata.HOST}) unreachable.
          Please make sure that the API is running and reachable.
        `,
        },
      };
    });

  return { ...data, error };
}

export async function loadOrgData(session: any, metadata?: Metadata) {
  if (!session || !metadata) return { organization: null };

  const { accessToken, orgId, testMode } = session;
  const { data, error } = await axios
    .post<AccountContextDataType>(
      url$`${metadata.HOST || ""}/graphql`,
      { query: ORG_DATA_QUERY },
      {
        headers: {
          ...(orgId ? { "x-org-id": orgId } : {}),
          ...(testMode ? { "x-test-mode": testMode } : {}),
          authorization: `Bearer ${accessToken}`,
        } as any,
      },
    )
    .then((res) => ({ data: res.data?.data, error: null }))
    .catch((e) => {
      const code = AUTH_HTTP_CODES.includes(e.response?.status)
        ? ServerErrorCode.API_AUTH_ERROR
        : ServerErrorCode.API_CONNECTION_ERROR;
      return {
        data: {},
        error: {
          code,
          message: `
          Server (${metadata.HOST}) unreachable.
          Please make sure that the API is running and reachable.
        `,
        },
      };
    });

  return { ...data, error };
}

const ACCOUNT_DATA_QUERY = `{
  user {
    email
    full_name
    is_staff
    is_superuser
    last_login
    date_joined
    permissions
  }
  workspace_config {
    object_type
    default_currency
    default_country_code
    default_weight_unit
    default_dimension_unit
    state_tax_id
    federal_tax_id
    default_label_type
    customs_aes
    customs_eel_pfc
    customs_license_number
    customs_certificate_number
    customs_nip_number
    customs_eori_number
    customs_vat_registration_number
    insured_by_default
  }
}`;
const ORG_DATA_QUERY = `{
  organization {
    id
  }
  organizations {
    id
    name
    slug
    token
    current_user {
      email
      full_name
      is_admin
      is_owner
      last_login
    }
    members {
      email
      full_name
      is_admin
      is_owner
      invitation {
        id
        guid
        invitee_identifier
        created
        modified
      }
      last_login
    }
  }
}`;
