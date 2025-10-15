import {
  accept_organization_invitation,
  ACCEPT_ORGANIZATION_INVITATION,
  ChangeOrganizationOwnerMutationInput,
  change_organization_owner,
  CHANGE_ORGANIZATION_OWNER,
  CreateOrganizationMutationInput,
  create_organization,
  CREATE_ORGANIZATION,
  delete_organization,
  DELETE_ORGANIZATION,
  delete_organization_invitation,
  DELETE_ORGANIZATION_INVITES,
  get_organizations,
  GET_ORGANIZATIONS,
  get_organization_invitation,
  GET_ORGANIZATION_INVITATION,
  SendOrganizationInvitesMutationInput,
  send_organization_invites,
  SEND_ORGANIZATION_INVITES,
  SetOrganizationUserRolesMutationInput,
  set_organization_user_roles,
  SET_ORGANIZATION_USER_ROLES,
  UpdateOrganizationMutationInput,
  update_organization,
  UPDATE_ORGANIZATION,
  get_organizations_organizations_edges_node,
} from "@karrio/types/graphql/ee";
import {
  UseQueryResult,
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import { gqlstr, insertUrlParam, setCookie } from "@karrio/lib";
import { useSession } from "next-auth/react";
import { useKarrio, useAuthenticatedQuery, useAuthenticatedMutation } from "./karrio";
import React from "react";

export type OrganizationType = get_organizations_organizations_edges_node;
type OrganizationContextType = {
  query?: UseQueryResult<get_organizations, any>;
  organization?: OrganizationType;
  organizations?: OrganizationType[];
};
export const OrganizationContext = React.createContext<OrganizationContextType>(
  {} as any,
);

const extractCurrent = (
  orgs?: OrganizationType[],
  orgId?: string,
): OrganizationType | undefined => {
  const current = (orgs || []).find((org) => org?.id === orgId);
  return current;
};

type OrganizationProviderProps = {
  children?: React.ReactNode;
  organizations: any;
  orgId?: string;
  metadata?: any;
};

export const OrganizationProvider = ({
  children,
  ...props
}: OrganizationProviderProps): JSX.Element => {
  const karrio = useKarrio();
  const initialOrganizations = React.useMemo<OrganizationType[] | undefined>(() => {
    // Accept either array or connection payload; normalize to array of nodes
    if (Array.isArray((props as any).organizations)) return (props as any).organizations as any;
    const edges = (props as any).organizations?.edges;
    if (Array.isArray(edges)) return edges.map((e: any) => e.node);
    // Some logs showed props being coerced to an object with numeric keys; recover array
    const numericKeys = Object.keys((props as any).organizations || {}).filter(k => /^\d+$/.test(k));
    if (numericKeys.length > 0) {
      return numericKeys
        .sort((a, b) => Number(a) - Number(b))
        .map((k) => (props as any).organizations[k]);
    }
    return undefined;
  }, [props.organizations]);

  const [organizations, setOrganizations] = React.useState<OrganizationType[] | undefined>(initialOrganizations);
  const [organization, setOrganization] = React.useState<OrganizationType | undefined>(extractCurrent(initialOrganizations, props.orgId));

  const query = useAuthenticatedQuery({
    queryKey: ["organizations"],
    queryFn: () =>
      karrio.graphql
        .request<get_organizations>(gqlstr(GET_ORGANIZATIONS), { filter: { is_active: true } })
        .then((data) => {
          const nodes = data?.organizations?.edges?.map((e: any) => e.node) || [];
          setOrganizations(nodes);
          const current = extractCurrent(nodes, props.orgId);
          setOrganization(current);
          setCookie("orgId", current?.id);
          return data;
        }),
    // Hydrate with normalized list when available
    initialData: initialOrganizations ? { organizations: { edges: initialOrganizations.map((n: any) => ({ node: n })) } as any } : undefined,
    enabled: props.metadata?.MULTI_ORGANIZATIONS === true,
    refetchOnWindowFocus: false,
    staleTime: 1500000,
  });

  if (!props.metadata?.MULTI_ORGANIZATIONS) return <>{children}</>;

  React.useEffect(() => {
    if (!query.data || !query.isFetched) return;
    const nodes = query.data?.organizations?.edges?.map((e: any) => e.node) || [];
    setOrganizations(nodes);
    const current = extractCurrent(nodes, props.orgId);
    setOrganization(current);
  }, [props.orgId, query.data]);

  return (
    <OrganizationContext.Provider
      value={{ organization, organizations, query }}
    >
      {children}
    </OrganizationContext.Provider>
  );
};

export function useOrganizations() {
  return React.useContext(OrganizationContext);
}

export function useOrganizationMutation() {
  const { update } = useSession();
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    queryClient.invalidateQueries({ queryKey: ["organizations"] });
    // Invalidate common org-scoped caches
    queryClient.invalidateQueries({
      predicate: (q) => {
        const key = q.queryKey as any[];
        // If key has the session scope object with orgId, let it refetch after session.update
        return Array.isArray(key) && key.length > 1 && typeof key[1] === 'object' && key[1] !== null && 'orgId' in key[1];
      }
    });
  };

  const createOrganization = useAuthenticatedMutation({
    mutationFn: (data: CreateOrganizationMutationInput) =>
      karrio.graphql.request<create_organization>(gqlstr(CREATE_ORGANIZATION), {
        data,
      }),
    onSuccess: invalidateCache,
  });

  const updateOrganization = useAuthenticatedMutation({
    mutationFn: (data: UpdateOrganizationMutationInput) =>
      karrio.graphql.request<update_organization>(gqlstr(UPDATE_ORGANIZATION), {
        data,
      }),
    onSuccess: invalidateCache,
  });

  const deleteOrganization = useAuthenticatedMutation({
    mutationFn: (data: { id: string }) =>
      karrio.graphql.request<delete_organization>(gqlstr(DELETE_ORGANIZATION), {
        data,
      }),
    onSuccess: invalidateCache,
  });

  const changeOrganizationOwner = useAuthenticatedMutation({
    mutationFn: (data: ChangeOrganizationOwnerMutationInput) =>
      karrio.graphql.request<change_organization_owner>(
        gqlstr(CHANGE_ORGANIZATION_OWNER),
        { data },
      ),
    onSuccess: invalidateCache,
  });

  const setOrganizationUserRoles = useAuthenticatedMutation({
    mutationFn: (data: SetOrganizationUserRolesMutationInput) =>
      karrio.graphql.request<set_organization_user_roles>(
        gqlstr(SET_ORGANIZATION_USER_ROLES),
        { data },
      ),
    onSuccess: invalidateCache,
  });

  const sendOrganizationInvites = useAuthenticatedMutation({
    mutationFn: (data: SendOrganizationInvitesMutationInput) =>
      karrio.graphql.request<send_organization_invites>(
        gqlstr(SEND_ORGANIZATION_INVITES),
        { data },
      ),
    onSuccess: invalidateCache,
  });

  const deleteOrganizationInvitation = useAuthenticatedMutation({
    mutationFn: (data: { id: string }) =>
      karrio.graphql.request<delete_organization_invitation>(
        gqlstr(DELETE_ORGANIZATION_INVITES),
        { data },
      ),
    onSuccess: invalidateCache,
  });

  // Helpers
  const changeActiveOrganization = async (orgId: string) => {
    // Optimistically set cookie; session.update is the source of truth
    setCookie("orgId", orgId);
    try {
      await update({ orgId });
      invalidateCache();
      // Use soft refresh for App Router to re-render server comps
      if (typeof window !== 'undefined' && 'navigation' in window) {
        // next/navigation router.refresh isn't accessible here; fallback to hard refresh
        // Consumer UIs can call router.refresh after awaiting this promise
      }
    } catch (e) {
      // Best-effort: revert cookie on failure
      setCookie("orgId", (karrio.pageData as any)?.orgId || "");
      throw e;
    }
  };

  const removeOrganizationMember = useAuthenticatedMutation({
    mutationFn: (data: { org_id: string; user_id: string }) =>
      karrio.graphql.request(
        `
          mutation RemoveOrganizationMember($data: RemoveOrganizationMemberMutationInput!) {
            remove_organization_member(input: $data) {
              organization {
                id
                name
                members {
                  email
                  full_name
                  is_admin
                  is_owner
                  last_login
                  invitation {
                    id
                    invitee_identifier
                  }
                }
              }
              errors { field messages }
            }
          }
        `,
        { data }
      ),
    onSuccess: invalidateCache,
  });

  const updateMemberStatus = useAuthenticatedMutation({
    mutationFn: (data: { org_id: string; user_id: string; is_active: boolean }) =>
      karrio.graphql.request(
        `
          mutation UpdateMemberStatus($data: UpdateMemberStatusMutationInput!) {
            update_member_status(input: $data) {
              organization {
                id
                name
                members {
                  email
                  full_name
                  is_admin
                  is_owner
                  last_login
                  invitation {
                    id
                    invitee_identifier
                  }
                }
              }
              errors { field messages }
            }
          }
        `,
        { data }
      ),
    onSuccess: invalidateCache,
  });

  const resendOrganizationInvite = useAuthenticatedMutation({
    mutationFn: (data: { invitation_id: string; redirect_url: string }) =>
      karrio.graphql.request(
        `
          mutation ResendOrganizationInvite($data: ResendOrganizationInviteMutationInput!) {
            resend_organization_invite(input: $data) {
              invitation {
                id
                invitee_identifier
              }
              errors { field messages }
            }
          }
        `,
        { data }
      ),
    onSuccess: invalidateCache,
  });

  return {
    createOrganization,
    updateOrganization,
    deleteOrganization,
    changeOrganizationOwner,
    setOrganizationUserRoles,
    sendOrganizationInvites,
    deleteOrganizationInvitation,
    removeOrganizationMember,
    updateMemberStatus,
    resendOrganizationInvite,
    changeActiveOrganization,
  };
}

export function useOrganizationInvitation(guid?: string) {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    // Invalidate all related queries to ensure data refresh
    queryClient.invalidateQueries({ queryKey: ["organizations"] });
    // Force refetch to ensure UI updates immediately
    queryClient.refetchQueries({ queryKey: ["organizations"] });
  };

  // Queries
  const query = useQuery({
    queryKey: ["invitation", guid],
    queryFn: () =>
      karrio.graphql.request<get_organization_invitation>(
        gqlstr(GET_ORGANIZATION_INVITATION),
        { variables: { guid } },
      ),
    enabled: !!guid,
  });

  // Mutations
  const acceptInvitation = useMutation(
    (data: { guid: string; full_name?: string; password?: string }) =>
      karrio.graphql.request<accept_organization_invitation>(
        gqlstr(ACCEPT_ORGANIZATION_INVITATION),
        { data },
      ),
    { onSuccess: invalidateCache },
  );

  return {
    query,
    acceptInvitation,
  };
}
