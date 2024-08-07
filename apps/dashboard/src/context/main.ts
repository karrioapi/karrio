import {
  AccountContextDataType,
  Metadata,
  PortalSessionType,
  SessionType,
  SubscriptionType,
  OrgContextDataType,
  TenantType,
} from "@karrio/types";
import {
  GetServerSideProps,
  GetServerSidePropsContext,
  NextApiRequest,
  NextApiResponse,
} from "next";
import { createServerError, isNone, ServerErrorCode, url$ } from "@karrio/lib";
import { getSession } from "next-auth/react";
import {
  KARRIO_ADMIN_API_KEY,
  KARRIO_PUBLIC_URL,
  KARRIO_ADMIN_URL,
  KARRIO_URL,
  MULTI_TENANT,
  TENANT_ENV_KEY,
  logger,
} from "@karrio/lib";
import { Session } from "next-auth";
import axios from "axios";

type RequestContext =
  | GetServerSidePropsContext
  | { req: NextApiRequest; res: NextApiResponse };
const AUTH_HTTP_CODES = [401, 403, 407];

export const getServerSideProps: GetServerSideProps = async (ctx) => {
  const session = ((await getSession(ctx)) as SessionType<Session>) || null;
  const pathname = ctx.resolvedUrl;

  const orgId = ((session as any)?.orgId as string) || null;

  const metadata = await loadAPIMetadata(ctx).catch((_) => _);
  const data = await loadContextData(session, metadata.metadata);
  const subscription = await checkSubscription(session, metadata.metadata);

  await setSessionCookies(ctx, orgId);

  if (needStaffAccess(pathname, data)) {
    return {
      redirect: {
        permanent: false,
        destination: "/",
      },
    };
  }

  return {
    props: {
      pathname,
      orgId,
      ...metadata,
      ...subscription,
      ...data,
    },
  };
};

export async function loadAPIMetadata(ctx: RequestContext): Promise<{
  metadata?: Metadata;
  KARRIO_PUBLIC_URL?: string;
  MULTI_TENANT?: boolean;
}> {
  // Attempt connection to the karrio API to retrieve the API metadata
  const API_URL = await getAPIURL(ctx);

  return new Promise(async (resolve, reject) => {
    try {
      const { data: metadata } = await axios.get<Metadata>(API_URL);

      // TODO:: implement version compatibility check here.
      await setSessionCookies(ctx as any);
      resolve({ metadata, KARRIO_PUBLIC_URL, MULTI_TENANT });
    } catch (e: any | Response) {
      logger.error(`Failed to fetch API metadata from (${API_URL})`);
      logger.error(e.response?.data || e.response);
      const code = AUTH_HTTP_CODES.includes(e.response?.status)
        ? ServerErrorCode.API_AUTH_ERROR
        : ServerErrorCode.API_CONNECTION_ERROR;

      const error = createServerError({
        code,
        message: `
          Server (${API_URL}) unreachable.
          Please make sure that the API is running and reachable.
        `,
      });
      reject({ error });
    }
  });
}

export async function loadContextData(
  session: SessionType,
  metadata: Metadata,
): Promise<any> {
  if (isNone(session)) return {};

  const { accessToken, orgId, testMode } = session;
  const headers = {
    ...(orgId ? { "x-org-id": orgId } : {}),
    ...(testMode ? { "x-test-mode": testMode } : {}),
    authorization: `Bearer ${accessToken}`,
  } as any;

  const getAccountData = () =>
    axios
      .post<AccountContextDataType>(
        url$`${metadata.HOST || ""}/graphql`,
        { query: ACCOUNT_DATA_QUERY },
        { headers },
      )
      .then(({ data }) => data);
  const getOrgData = () =>
    !!metadata?.MULTI_ORGANIZATIONS
      ? axios
          .post<OrgContextDataType>(
            url$`${metadata.HOST || ""}/graphql`,
            { query: ORG_DATA_QUERY },
            { headers },
          )
          .then(({ data }) => data)
      : Promise.resolve({ data: {} });

  try {
    const [{ data: user }, { data: org }] = await Promise.all([
      getAccountData(),
      getOrgData(),
    ]);
    return { metadata, ...user, ...org };
  } catch (e: any | Response) {
    logger.error(`Failed to fetch API data from (${KARRIO_URL})`);
    logger.error(e.response?.data || e.response);
    const code = AUTH_HTTP_CODES.includes(e.response?.status)
      ? ServerErrorCode.API_AUTH_ERROR
      : ServerErrorCode.API_CONNECTION_ERROR;

    const error = createServerError({
      code,
      message: "Failed to load intial data...",
    });
    return { metadata, error };
  }
}

export async function setSessionCookies(
  ctx: GetServerSidePropsContext,
  orgId?: string | null,
) {
  // Sets the authentication orgId cookie if the session has one
  if (ctx.res && !!orgId) {
    ctx.res.setHeader(
      "Set-Cookie",
      `orgId=${orgId}; path=${ctx.resolvedUrl || "/"}`,
    );
  }
}

export async function checkSubscription(
  session: SessionType | any,
  metadata?: Metadata,
) {
  if (isNone(session)) return {};
  const { accessToken, orgId } = session;

  if (
    orgId &&
    (metadata?.ORG_LEVEL_BILLING || metadata?.TENANT_LEVEL_BILLING)
  ) {
    const headers = {
      ...(orgId ? { "x-org-id": orgId } : {}),
      authorization: `Bearer ${accessToken}`,
    } as any;
    const getOrgSubscription = () =>
      axios
        .get<SubscriptionType>(
          url$`${metadata?.HOST}/v1/billing/subscription`,
          { headers },
        )
        .then(({ data }) => data)
        .catch(() => {
          return null;
        });

    try {
      const subscription = await getOrgSubscription();

      return { subscription };
    } catch (e: any | Response) {
      logger.error(
        `Failed to fetch API subscription details from (${KARRIO_URL})`,
      );
      logger.error(e.response?.data || e.response);
    }
  }

  return { subscription: null };
}

export async function createPortalSession(
  session: SessionType | any,
  host: string,
  subscription?: SubscriptionType,
  metadata?: Metadata,
) {
  if (subscription?.is_owner) {
    const return_url = "http://" + host;
    const headers = {
      ...(session.orgId ? { "x-org-id": session.orgId } : {}),
      authorization: `Bearer ${session.accessToken}`,
    } as any;

    const getCustomerPortalSession = () =>
      axios
        .post<PortalSessionType>(
          url$`${metadata?.HOST}/v1/billing/portal`,
          { return_url },
          { headers },
        )
        .then(({ data }) => data);

    try {
      const portal_session = await getCustomerPortalSession();

      return { session_url: portal_session.url };
    } catch (e: any | Response) {
      logger.error(
        `Failed to create customer portal session from (${KARRIO_URL})`,
      );
      logger.error(e.response?.data || e.response);
    }
  }

  return {};
}

export async function loadTenantInfo(filter: {
  app_domain?: string;
  schema_name?: string;
}): Promise<TenantType | null> {
  try {
    const { data } = await axios({
      url: url$`${KARRIO_ADMIN_URL}/admin/graphql/`,
      method: "POST",
      headers: {
        authorization: `Token ${KARRIO_ADMIN_API_KEY}`,
      },
      data: { variables: { filter }, query: TENANT_QUERY },
    });
    console.log(JSON.stringify(data, null, 2));
    return data.data?.tenants?.edges[0].node;
  } catch (e: any) {
    console.log(e);
    console.log(e.response?.data, url$`${KARRIO_ADMIN_URL}/admin/graphql/`);

    return null;
  }
}

function needStaffAccess(
  pathname,
  { user, metadata }: { user?: any | null; metadata?: Metadata },
) {
  return (
    pathname.includes("/admin") &&
    !!user &&
    user?.is_staff === false &&
    metadata?.ADMIN_DASHBOARD == false
  );
}

async function getAPIURL(ctx: RequestContext) {
  if (!MULTI_TENANT) {
    return KARRIO_URL as string;
  }

  const params = (ctx as GetServerSidePropsContext).params;
  const headers = (ctx.req as NextApiRequest).headers;
  const host = headers ? headers.host : null;
  const site = params ? params.site : null;

  const app_domain = (site || host) as string;
  const tenant =
    MULTI_TENANT && !!app_domain ? await loadTenantInfo({ app_domain }) : null;
  const APIURL = !!TENANT_ENV_KEY
    ? (tenant?.api_domains || []).find((d) =>
        d.includes(TENANT_ENV_KEY as string),
      )
    : (tenant?.api_domains || [])[0];

  return (!!APIURL ? APIURL : KARRIO_URL) as string;
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
const TENANT_QUERY = `query getTenant($filter: TenantFilter!) {
  tenants(filter: $filter) {
    edges { node { schema_name api_domains } }
  }
}`;
