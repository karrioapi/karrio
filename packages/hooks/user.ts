import {
  UPDATE_USER,
  GET_USER,
  UpdateUserInput,
  RegisterUserMutationInput,
  RequestEmailChangeMutationInput,
  REGISTER_USER,
  CONFIRM_EMAIL_CHANGE,
  ConfirmEmailChangeMutationInput,
  CONFIRM_PASSWORD_RESET,
  ConfirmPasswordResetMutationInput,
  ChangePasswordMutationInput,
  GetUser,
  confirm_email_change,
  request_email_change,
  confirm_password_reset,
  register_user,
  change_password,
  update_user,
  REQUEST_EMAIL_CHANGE,
  ConfirmEmailMutationInput,
  confirm_email,
  CONFIRM_EMAIL,
  CHANGE_PASSWORD,
  RequestPasswordResetMutationInput,
  request_password_reset,
  REQUEST_PASSWORD_RESET,
} from "@karrio/types";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuthenticatedQuery } from "./karrio";
import { gqlstr, onError, url$ } from "@karrio/lib";
import { useKarrio } from "./karrio";
import { useAPIMetadata } from "@karrio/hooks/api-metadata";
import axios from "axios";
import { getSession } from "next-auth/react";

export function useUser() {
  const karrio = useKarrio();
  const user = karrio.pageData?.user;

  // Queries
  const query = useAuthenticatedQuery({
    queryKey: ["user"],
    queryFn: () => karrio.graphql.request<GetUser>(gqlstr(GET_USER)),
    initialData: !!user ? { user } : undefined,
    refetchOnWindowFocus: false,
    staleTime: 300000,
    enabled: !!user,
    onError,
  });

  return {
    query,
  };
}

export function useUserMutation() {
  const karrio = useKarrio();
  const { getHost, metadata } = useAPIMetadata();
  const queryClient = useQueryClient();
  const invalidateCache = () => {
    // Invalidate all related queries to ensure data refresh
    queryClient.invalidateQueries({ queryKey: ["user"] });
    queryClient.invalidateQueries({ queryKey: ["organizations"] });
    // Force refetch to ensure UI updates immediately
    queryClient.refetchQueries({ queryKey: ["user"] });
  };

  // Mutations
  const updateUser = useMutation(
    (data: UpdateUserInput) =>
      karrio.graphql.request<update_user>(gqlstr(UPDATE_USER), { data }),
    { onSuccess: invalidateCache, onError },
  );
  const closeAccount = useMutation(
    async () => {
      // Bypass org header by using a direct axios POST (Authorization only)
      const host = getHost?.();
      const graphqlUrl = (metadata as any)?.GRAPHQL || url$`${host}/graphql`;
      const session: any = await getSession();
      const headers: Record<string, string> = { "content-type": "application/json" };
      if (session?.accessToken) headers["authorization"] = `Bearer ${session.accessToken}`;
      if (session?.testMode) headers["x-test-mode"] = "true";

      const body = {
        query: `mutation update_user($data: UpdateUserInput!) { update_user(input: $data) { user { email } errors { field messages } } }`,
        variables: { data: { is_active: false } },
      };

      const resp = await axios.post(graphqlUrl, body, { headers });
      const result = resp.data?.data?.update_user;
      if (!result || (result?.errors && result.errors.length)) {
        throw resp.data?.errors || result?.errors || [{ message: "Unknown error" }];
      }
      return { update_user: result } as any;
    },
    { onError },
  );
  const registerUser = useMutation(
    (data: RegisterUserMutationInput) =>
      karrio.graphql.request<register_user>(gqlstr(REGISTER_USER), { data }),
    { onSuccess: invalidateCache, onError },
  );
  const requestEmailChange = useMutation(
    (data: RequestEmailChangeMutationInput) =>
      karrio.graphql.request<request_email_change>(
        gqlstr(REQUEST_EMAIL_CHANGE),
        { data },
      ),
    { onSuccess: invalidateCache, onError },
  );
  const confirmEmailChange = useMutation(
    async (data: ConfirmEmailChangeMutationInput) => {
      // Prefer direct authenticated POST so it also works on public routes without providers
      const host = getHost?.();
      const graphqlUrl = (metadata as any)?.GRAPHQL || url$`${host}/graphql`;
      const session: any = await getSession();
      const headers: Record<string, string> = {
        "content-type": "application/json",
      };
      if (session?.accessToken) headers["authorization"] = `Bearer ${session.accessToken}`;
      if (session?.orgId) headers["x-org-id"] = String(session.orgId);
      if (session?.testMode) headers["x-test-mode"] = "true";

      const body = {
        query: `mutation confirm_email_change($data: ConfirmEmailChangeMutationInput!) { confirm_email_change(input: $data) { user { email } errors { field messages } } }`,
        variables: { data },
      };

      const resp = await axios.post(graphqlUrl, body, { headers });
      // Normalize return to the original gql.request shape
      const result = resp.data?.data?.confirm_email_change;
      if (!result) {
        // Bubble up top-level GraphQL errors in a consistent shape
        throw resp.data?.errors || [{ message: "Unknown error" }];
      }
      return { confirm_email_change: result } as any;
    },
    { onSuccess: invalidateCache, onError },
  );
  const changePassword = useMutation(
    (data: ChangePasswordMutationInput) =>
      karrio.graphql.request<change_password>(gqlstr(CHANGE_PASSWORD), {
        data,
      }),
    { onSuccess: invalidateCache, onError },
  );
  const confirmPasswordReset = useMutation(
    (data: ConfirmPasswordResetMutationInput) =>
      karrio.graphql.request<confirm_password_reset>(
        gqlstr(CONFIRM_PASSWORD_RESET),
        { data },
      ),
    { onSuccess: invalidateCache },
  );
  const confirmEmail = useMutation(
    (data: ConfirmEmailMutationInput) =>
      karrio.graphql.request<confirm_email>(gqlstr(CONFIRM_EMAIL), { data }),
    { onSuccess: invalidateCache },
  );
  const requestPasswordReset = useMutation(
    (data: RequestPasswordResetMutationInput) =>
      karrio.graphql.request<request_password_reset>(
        gqlstr(REQUEST_PASSWORD_RESET),
        { data },
      ),
    { onSuccess: invalidateCache },
  );

  return {
    closeAccount,
    confirmEmail,
    changePassword,
    confirmEmailChange,
    confirmPasswordReset,
    requestPasswordReset,
    requestEmailChange,
    registerUser,
    updateUser,
  };
}
