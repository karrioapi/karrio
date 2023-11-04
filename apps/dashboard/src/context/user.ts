import { UPDATE_USER, GET_USER, UpdateUserInput, RegisterUserMutationInput, RequestEmailChangeMutationInput, REGISTER_USER, CONFIRM_EMAIL_CHANGE, ConfirmEmailChangeMutationInput, CONFIRM_PASSWORD_RESET, ConfirmPasswordResetMutationInput, ChangePasswordMutationInput, GetUser, confirm_email_change, request_email_change, confirm_password_reset, register_user, change_password, update_user, GetUser_user, REQUEST_EMAIL_CHANGE, ConfirmEmailMutationInput, confirm_email, CONFIRM_EMAIL, CHANGE_PASSWORD, RequestPasswordResetMutationInput, request_password_reset, REQUEST_PASSWORD_RESET } from "@karrio/graphql";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { gqlstr, onError } from "@/lib/helper";
import { useKarrio } from "@/lib/client";

export type UserType = GetUser_user;


export function useUser() {
  const karrio = useKarrio();

  // Queries
  const query = useQuery(
    ['user'],
    () => karrio.graphql$.request<GetUser>(gqlstr(GET_USER)),
    { onError }
  );

  return {
    query,
  };
}

export function useUserMutation() {
  const karrio = useKarrio();
  const queryClient = useQueryClient();
  const invalidateCache = () => { queryClient.invalidateQueries(['user']) };

  // Mutations
  const updateUser = useMutation(
    (data: UpdateUserInput) => karrio.graphql$.request<update_user>(gqlstr(UPDATE_USER), { data }),
    { onSuccess: invalidateCache, onError }
  );
  const closeAccount = useMutation(
    () => karrio.graphql$.request<update_user>(gqlstr(UPDATE_USER), { data: { is_active: false } }),
    { onSuccess: invalidateCache, onError }
  );
  const registerUser = useMutation(
    (data: RegisterUserMutationInput) => karrio.graphql$.request<register_user>(
      gqlstr(REGISTER_USER), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const requestEmailChange = useMutation(
    (data: RequestEmailChangeMutationInput) => karrio.graphql$.request<request_email_change>(
      gqlstr(REQUEST_EMAIL_CHANGE), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const confirmEmailChange = useMutation(
    (data: ConfirmEmailChangeMutationInput) => karrio.graphql$.request<confirm_email_change>(
      gqlstr(CONFIRM_EMAIL_CHANGE), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const changePassword = useMutation(
    (data: ChangePasswordMutationInput) => karrio.graphql$.request<change_password>(
      gqlstr(CHANGE_PASSWORD), { data }
    ),
    { onSuccess: invalidateCache, onError }
  );
  const confirmPasswordReset = useMutation(
    (data: ConfirmPasswordResetMutationInput) => karrio.graphql$.request<confirm_password_reset>(
      gqlstr(CONFIRM_PASSWORD_RESET), { data }
    ),
    { onSuccess: invalidateCache }
  );
  const confirmEmail = useMutation(
    (data: ConfirmEmailMutationInput) => karrio.graphql$.request<confirm_email>(
      gqlstr(CONFIRM_EMAIL), { data }
    ),
    { onSuccess: invalidateCache }
  );
  const requestPasswordReset = useMutation(
    (data: RequestPasswordResetMutationInput) => karrio.graphql$.request<request_password_reset>(
      gqlstr(REQUEST_PASSWORD_RESET), { data }
    ),
    { onSuccess: invalidateCache }
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
