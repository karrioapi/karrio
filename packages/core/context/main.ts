"use server";
import {
  KARRIO_ADMIN_API_KEY,
  KARRIO_ADMIN_URL,
  KARRIO_URL,
  MULTI_TENANT,
  ServerErrorCode,
  TENANT_ENV_KEY,
  url$,
} from "@karrio/lib";
import { AccountContextDataType, Metadata, TenantType } from "@karrio/types";
import { unstable_cache } from "next/cache";
import { redirect } from "next/navigation";
import { headers } from "next/headers";
import { Session } from "next-auth";
import axios from "axios";

const AUTH_HTTP_CODES = [401, 403, 407];

export async function requireAuthentication(session: Session | null) {
  if (!session || (session as any)?.error === "RefreshAccessTokenError") {
    const [pathname, search] = [
      headers().get("x-pathname") || "",
      headers().get("x-search") || "",
    ];

    const location = search.includes("next") ? search : `${pathname}${search}`;

    redirect(`/signin?next=${location}`);
  }
}

export async function loadMetadata() {
  // Attempt connection to the karrio API to retrieve the API metadata
  const API_URL = await getAPIURL();

  const { data: metadata, error } = await axios
    .get<Metadata>(url$`${API_URL}`, {
      headers: { "Content-Type": "application/json" },
    })
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
          Server (${API_URL}) unreachable.
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

async function getAPIURL() {
  if (!MULTI_TENANT) return KARRIO_URL as string;

  const app_domain = headers().get("host") as string;
  const tenant =
    MULTI_TENANT && !!app_domain ? await loadTenantInfo({ app_domain }) : null;
  const APIURL = !!TENANT_ENV_KEY
    ? (tenant?.api_domains || []).find((d) =>
        d.includes(TENANT_ENV_KEY as string),
      )
    : (tenant?.api_domains || [])[0];

  return (!!APIURL ? APIURL : KARRIO_URL) as string;
}

export const loadTenantInfo = unstable_cache(
  async (filter: {
    app_domain?: string;
    schema_name?: string;
  }): Promise<TenantType | null> => {
    console.log("loadTenantInfo", filter);
    try {
      const { data } = await axios({
        url: url$`${KARRIO_ADMIN_URL}/admin/graphql/`,
        method: "POST",
        headers: {
          authorization: `Token ${KARRIO_ADMIN_API_KEY}`,
        },
        data: { variables: { filter }, query: TENANT_QUERY },
      });
      // console.log(JSON.stringify(data, null, 2));
      return data.data?.tenants?.edges[0]?.node;
    } catch (e: any) {
      console.log(e);
      console.log(e.response?.data, url$`${KARRIO_ADMIN_URL}/admin/graphql/`);

      return null;
    }
  },
  ["tenant"],
  { revalidate: 3600, tags: ["tenant"] },
);

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
const TENANT_QUERY = `query getTenant($filter: TenantFilter!) {
  tenants(filter: $filter) {
    edges { node { schema_name api_domains } }
  }
}`;
