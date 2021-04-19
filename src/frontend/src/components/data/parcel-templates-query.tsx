import React from 'react';
import { LazyQueryResult, useLazyQuery } from '@apollo/client';
import { get_parcel_templates, GET_PARCEL_TEMPLATES, get_parcel_templates_parcel_templates_edges, get_parcel_templates_parcel_templates_edges_node, get_parcel_templates_parcel_templates_edges_node_parcel, PageInfo } from '@/graphql';
import { ParcelTemplateType } from '@/library/types';


type Edges = (get_parcel_templates_parcel_templates_edges | null)[];
export type ParcelTemplatesType = LazyQueryResult<get_parcel_templates, any> & { 
  templates: ParcelTemplateType[];
  next?: string | null;
  previous?: string | null;
  load: (options?: any) => void;
  loadMore: (cursor?: string | null) => void;
};

export const ParcelTemplates = React.createContext<ParcelTemplatesType>({} as ParcelTemplatesType);

const ParcelTemplatesQuery: React.FC = ({ children }) => {
  const [load, result] = useLazyQuery<get_parcel_templates>(GET_PARCEL_TEMPLATES);

  const extract = (edges?: Edges) => (edges || []).map(item => item?.node as ParcelTemplateType);
  const loadMore = (cursor?: string | null) => result?.fetchMore && result.fetchMore({ variables: { cursor } });

  return (
    <ParcelTemplates.Provider value={{
      load,
      loadMore,
      templates: extract(result.data?.parcel_templates?.edges || []),
      next: result.data?.parcel_templates?.pageInfo?.hasNextPage ? result.data?.parcel_templates?.pageInfo?.endCursor : null,
      previous: result.data?.parcel_templates?.pageInfo?.hasPreviousPage ? result.data?.parcel_templates?.pageInfo?.startCursor : null,
      ...result
    }}>
      {children}
    </ParcelTemplates.Provider>
  );
};

export default ParcelTemplatesQuery;
