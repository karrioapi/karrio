import React from 'react';
import { FetchResult, useMutation } from '@apollo/client';
import { GetToken, MUTATE_TOKEN, mutate_tokenVariables, TokenMutationInput } from '@/graphql';

type TemplateMutator<T> = T & {
  updateToken: (data: TokenMutationInput) => Promise<FetchResult<GetToken, Record<string, any>, Record<string, any>>>;
}

export type TokenUpdateType = (data: TokenMutationInput) => Promise<FetchResult<GetToken, Record<string, any>, Record<string, any>>>;

const TokenMutation = <T extends {}>(Component: React.FC<TemplateMutator<T>>) => (
  ({ children, ...props }: any) => {
    const [mutateToken] = useMutation<GetToken, mutate_tokenVariables>(MUTATE_TOKEN);

    const updateToken = (data: TokenMutationInput) => mutateToken({ variables: { data } });

    return (
      <Component {...props} updateToken={updateToken}>
        {children}
      </Component>
    );
  }
);

export default TokenMutation;
