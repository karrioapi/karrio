"use server";
import {
  isNone,
  KARRIO_ADMIN_API_KEY,
  KARRIO_ADMIN_URL,
  KARRIO_URL,
  logger,
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

/**
 * Helper function to extract the current domain from headers
 * Use this at the top level of your page components or API routes
 * and pass the result to other functions to avoid headers() calls inside cached functions
 */
export async function getCurrentDomain(): Promise<string | null> {
  return (await headers()).get("host");
}

export async function requireAuthentication(session: Session | null) {
  if (!session || (session as any)?.error === "RefreshAccessTokenError") {
    const [pathname, search] = [
      (await headers()).get("x-pathname") || "/",
      (await headers()).get("x-search") || "",
    ];

    if (pathname.includes("/signin")) return;

    const location = search.includes("next")
      ? `?${search}`
      : `?next=${pathname}${search}`;

    logger.debug("redirecting to signin");
    redirect(`/signin${location}`);
  }
}

// Create domain-specific cached metadata loader
function createMetadataLoader(domain?: string) {
  return unstable_cache(
    async () => {
      // Detect if we're in a build environment
      const IS_BUILD = process.env.NODE_ENV === 'production' && process.env.NEXT_PHASE === 'phase-production-build';

      // Return mock data during build to avoid actual API calls
      if (IS_BUILD) {
        logger.debug({ action: "> loadMetadata", message: "Using mock data during build" });
        return {
          metadata: {
            HOST: "http://mock-api-for-build",
            VERSION: "build-version",
            "APP_NAME": "Karrio",
            "APP_WEBSITE": "https://karrio.io",
            "ADMIN": "http://localhost:5002/admin",
            "GRAPHQL": "http://localhost:5002/graphql",
            "OPENAPI": "http://localhost:5002/openapi",
            "AUDIT_LOGGING": true,
            "ALLOW_SIGNUP": true,
            "ALLOW_ADMIN_APPROVED_SIGNUP": false,
            "ALLOW_MULTI_ACCOUNT": true,
            "ADMIN_DASHBOARD": true,
            "MULTI_ORGANIZATIONS": true,
            "ORDERS_MANAGEMENT": true,
            "APPS_MANAGEMENT": true,
            "DOCUMENTS_MANAGEMENT": true,
            "DATA_IMPORT_EXPORT": false,
            "PERSIST_SDK_TRACING": true,
            "WORKFLOW_MANAGEMENT": true
          },
          error: null
        };
      }

      // Attempt connection to the karrio API to retrieve the API metadata
      const API_URL = await getAPIURL(undefined, domain);

      logger.debug({ action: "> loadMetadata", API_URL });

      const { data: metadata, error } = await axios
        .get<Metadata>(url$`${API_URL}`, {
          headers: { "Content-Type": "application/json" },
        })
        .then((res) => ({ data: res.data, error: null }))
        .catch((e) => {
          console.log("loadMetadata", e);
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
    },
    [`metadata-${domain || 'default'}`],
    { revalidate: 5, tags: ["metadata"] } // Cache for 5 seconds to reflect admin changes quickly
  );
}

// Cached version of loadMetadata to prevent multiple requests during build
export async function loadMetadata(domain?: string) {
  const cachedLoader = createMetadataLoader(domain);
  return await cachedLoader();
}

export async function loadUserData(session: any, metadata?: Metadata, domain?: string) {
  if (!session || !metadata) return { user: null };

  const API_URL = await getAPIURL(metadata, domain);
  const { accessToken, orgId, testMode } = session;
  const { data, error } = await axios
    .post<AccountContextDataType>(
      url$`${API_URL}/graphql`,
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
          Server (${API_URL}) unreachable.
          Please make sure that the API is running and reachable.
        `,
        },
      };
    });

  return { ...data, error };
}

export async function loadOrgData(session: any, metadata?: Metadata, domain?: string) {
  if (!session || !metadata || !metadata.MULTI_ORGANIZATIONS) {
    return { organization: null };
  }

  const API_URL = await getAPIURL(metadata, domain);
  const { accessToken, orgId, testMode } = session;
  const { data, error } = await axios
    .post<AccountContextDataType>(
      url$`${API_URL}/graphql`,
      { query: ORG_DATA_QUERY },
      {
        headers: {
          ...(orgId ? { "x-org-id": orgId } : {}),
          ...(testMode ? { "x-test-mode": testMode } : {}),
          authorization: `Bearer ${accessToken}`,
        } as any,
      },
    )
    .then((res) => ({ data: (res.data?.data as any)?.organizations?.edges?.map((e: any) => e.node) || [], error: null }))
    .catch((e) => {
      const code = AUTH_HTTP_CODES.includes(e.response?.status)
        ? ServerErrorCode.API_AUTH_ERROR
        : ServerErrorCode.API_CONNECTION_ERROR;
      return {
        data: {},
        error: {
          code,
          message: `
          Server (${API_URL}) unreachable.
          Please make sure that the API is running and reachable.
        `,
        },
      };
    });

  // Return a consistent shape for client providers
  return { organizations: data, error };
}

async function getAPIURL(metadata?: Metadata, app_domain?: string) {
  if (metadata?.HOST) {
    return MULTI_TENANT ? metadata.HOST : KARRIO_URL;
  }

  if (
    MULTI_TENANT === true &&
    !isNone(KARRIO_ADMIN_URL) &&
    !isNone(KARRIO_ADMIN_API_KEY)
  ) {
    // Use provided app_domain or get it from headers
    const domain = app_domain || (await headers()).get("host") as string;
    const tenant =
      MULTI_TENANT && !!domain
        ? await loadTenantInfo({ app_domain: domain })
        : null;
    const APIURL = !!TENANT_ENV_KEY
      ? (tenant?.api_domains || []).find((d) =>
        d.includes(TENANT_ENV_KEY as string),
      )
      : (tenant?.api_domains || [])[0];

    return (!!APIURL ? APIURL : KARRIO_URL) as string;
  }

  return KARRIO_URL as string;
}

// Create domain-specific cached tenant info loader
function createTenantInfoLoader(domain: string) {
  return unstable_cache(
    async (): Promise<TenantType | null> => {
      logger.debug("loadTenantInfo", { app_domain: domain });
      try {
        const { data } = await axios({
          url: url$`${KARRIO_ADMIN_URL}/admin/graphql/`,
          method: "POST",
          headers: {
            authorization: `Token ${KARRIO_ADMIN_API_KEY}`,
          },
          data: {
            variables: { filter: { app_domain: domain } },
            query: TENANT_QUERY
          },
        });
        return data.data?.tenants?.edges[0]?.node;
      } catch (e: any) {
        console.log(e);
        console.log(e.response?.data, url$`${KARRIO_ADMIN_URL}/admin/graphql/`);
        return null;
      }
    },
    [`tenant-${domain}`],
    { revalidate: 3600, tags: ["tenant"] },
  );
}

export async function loadTenantInfo(filter: {
  app_domain?: string;
  schema_name?: string;
}): Promise<TenantType | null> {
  // For app_domain, use cached loader
  if (filter.app_domain) {
    const cachedLoader = createTenantInfoLoader(filter.app_domain);
    return await cachedLoader();
  }

  // For schema_name or other filters, make direct call (less common case)
  logger.debug("loadTenantInfo (uncached)", filter);
  try {
    const { data } = await axios({
      url: url$`${KARRIO_ADMIN_URL}/admin/graphql/`,
      method: "POST",
      headers: {
        authorization: `Token ${KARRIO_ADMIN_API_KEY}`,
      },
      data: { variables: { filter }, query: TENANT_QUERY },
    });
    return data.data?.tenants?.edges[0]?.node;
  } catch (e: any) {
    console.log(e);
    console.log(e.response?.data, url$`${KARRIO_ADMIN_URL}/admin/graphql/`);
    return null;
  }
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
  organizations(filter: {is_active: true}) {
    page_info {
      count
      has_next_page
      has_previous_page
      start_cursor
      end_cursor
    }
    edges {
      node {
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
    }
  }
}`;

const TENANT_QUERY = `query getTenant($filter: TenantFilter!) {
  tenants(filter: $filter) {
    edges { node { schema_name api_domains } }
  }
}`;
