import React from 'react';
import { FetchResult, useMutation } from '@apollo/client';
import { GetUser_user, MUTATE_USER, mutate_userVariables, UserMutationInput } from '@/graphql';


export type UserMutator<T> = T & {
  updateUser: (data: UserMutationInput) => Promise<FetchResult<GetUser_user, Record<string, any>, Record<string, any>>>;
  closeAccount: () => Promise<FetchResult<GetUser_user, Record<string, any>, Record<string, any>>>;
}

export type UserUpdateType = (data: UserMutationInput) => Promise<FetchResult<GetUser_user, Record<string, any>, Record<string, any>>>;

const UserMutation = <T extends {}>(Component: React.FC<UserMutator<T>>) => (
  ({ children, ...props }: any) => {
    const [updateMutation, update] = useMutation<GetUser_user, mutate_userVariables>(MUTATE_USER);

    const updateUser = (data: UserMutationInput) => updateMutation({ variables: { data } });
    const closeAccount = () => updateMutation({ variables: { data: { is_active: false } } });

    return (
      <Component {...props} updateUser={updateUser} closeAccount={closeAccount}>
        {children}
      </Component>
    );
  }
);

export default UserMutation;
