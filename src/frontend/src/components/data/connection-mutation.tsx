import React from 'react';
import { FetchResult, MutationFunctionOptions, MutationResult, useMutation } from '@apollo/client';
import { CreateConnectionInput, CREATE_CONNECTION, create_connectionVariables, DELETE_CONNECTION, delete_connectionVariables, UpdateConnectionInput, UPDATED_CONNECTION, update_connectionVariables } from '@/graphql';

export type ConnectionMutator<T> = T & {
  createConnection: (data: CreateConnectionInput) => Promise<FetchResult<CreateConnectionInput, Record<string, any>, Record<string, any>>>;
  updateConnection: (data: UpdateConnectionInput) => Promise<FetchResult<UpdateConnectionInput, Record<string, any>, Record<string, any>>>;
  deleteConnection: (id: string) => Promise<FetchResult<{ id: string; }, Record<string, any>, Record<string, any>>>;
}

export type ConnectionMutationType = (options?: MutationFunctionOptions<create_connectionVariables, {
  data: Partial<CreateConnectionInput>;
}> | undefined) => Promise<FetchResult<CreateConnectionInput, Record<string, any>, Record<string, any>>>;
export type ConnectionMutationResultType = MutationResult<CreateConnectionInput>;

const ConnectionMutation = <T extends {}>(Component: React.FC<ConnectionMutator<T>>) => {
  return ({ children, ...props }: any) => {
    const [createMutation] = useMutation<CreateConnectionInput, create_connectionVariables>(CREATE_CONNECTION);
    const [updateMutation] = useMutation<UpdateConnectionInput, update_connectionVariables>(UPDATED_CONNECTION);
    const [deleteMutation] = useMutation<{ id: string }, delete_connectionVariables>(DELETE_CONNECTION);

    const createConnection = (data: CreateConnectionInput) => createMutation({ variables: { data } });
    const updateConnection = (data: UpdateConnectionInput) => updateMutation({ variables: { data } });
    const deleteConnection = (id: string) => deleteMutation({ variables: { data: { id } } });

    return (
      <Component {...props}
        createConnection={createConnection}
        updateConnection={updateConnection}
        deleteConnection={deleteConnection}
      >
        {children}
      </Component>
    );
  };
}

export default ConnectionMutation;
