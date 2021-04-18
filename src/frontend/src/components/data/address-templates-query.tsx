import React from 'react';
import { LazyQueryResult, useLazyQuery } from '@apollo/client';
import { get_address_templates, GET_ADDRESS_TEMPLATES, get_address_templates_address_templates_edges, PageInfo } from '@/graphql';
import { AddressTemplate } from '@/library/types';


type Edges = (get_address_templates_address_templates_edges | null)[];
export type AddressTemplatesType = LazyQueryResult<get_address_templates, any> & { 
  templates: AddressTemplate[];
  next?: string | null;
  previous?: string | null;
  load: (options?: any) => void;
  loadMore: (cursor?: string | null) => void;
};

export const AddressTemplates = React.createContext<AddressTemplatesType>({} as AddressTemplatesType);

const AddressTemplatesQuery: React.FC = ({ children }) => {
  const [load, result] = useLazyQuery<get_address_templates>(GET_ADDRESS_TEMPLATES);

  const extract = (edges?: Edges) => (edges || []).map(item => item?.node as AddressTemplate);
  const loadMore = (cursor?: string | null) => result?.fetchMore && result.fetchMore({ variables: { cursor } });
  
  return (
    <AddressTemplates.Provider value={{
      load,
      loadMore,
      templates: extract(result.data?.address_templates?.edges),
      next: result.data?.address_templates?.pageInfo?.hasNextPage ? result.data?.address_templates?.pageInfo?.endCursor : null,
      previous: result.data?.address_templates?.pageInfo?.hasPreviousPage ? result.data?.address_templates?.pageInfo?.startCursor : null,
      ...result
    }}>
      {children}
    </AddressTemplates.Provider>
  );
};

export default AddressTemplatesQuery;
