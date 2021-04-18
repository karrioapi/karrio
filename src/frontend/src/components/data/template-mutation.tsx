import React from 'react';
import { FetchResult, useMutation } from '@apollo/client';
import { CreateTemplateInput, CREATE_TEMPLATE, create_templateVariables, DELETE_TEMPLATE, delete_templateVariables, UPDATED_TEMPLATE, UpdateTemplateInput, update_templateVariables } from '@/graphql';


export type TemplateMutator<T> = T & {
  createTemplate: (data: CreateTemplateInput) => Promise<FetchResult<CreateTemplateInput, Record<string, any>, Record<string, any>>>;
  updateTemplate: (data: UpdateTemplateInput) => Promise<FetchResult<UpdateTemplateInput, Record<string, any>, Record<string, any>>>;
  deleteTemplate: (id: string) => Promise<FetchResult<{ id: string; }, Record<string, any>, Record<string, any>>>;
}

const TemplateMutation = <T extends {}>(Component: React.FC<TemplateMutator<T>>) => (
  ({ children, ...props }: any) => {
    const [createMutation] = useMutation<CreateTemplateInput, create_templateVariables>(CREATE_TEMPLATE);
    const [updateMutation] = useMutation<UpdateTemplateInput, update_templateVariables>(UPDATED_TEMPLATE);
    const [deleteMutation] = useMutation<{ id: string }, delete_templateVariables>(DELETE_TEMPLATE);

    const createTemplate = (data: CreateTemplateInput) => createMutation({ variables: { data } });
    const updateTemplate = (data: UpdateTemplateInput) => updateMutation({ variables: { data } });
    const deleteTemplate = (id: string) => deleteMutation({ variables: { data: { id } } });

    return (
      <Component {...props}
        createTemplate={createTemplate}
        updateTemplate={updateTemplate}
        deleteTemplate={deleteTemplate}
      >
        {children}
      </Component>
    );
  }
);

export default TemplateMutation;
