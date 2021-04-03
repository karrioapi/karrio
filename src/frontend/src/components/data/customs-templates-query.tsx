import React from 'react';
import { LazyQueryResult, useLazyQuery } from '@apollo/client';
import { get_customs_info_templates, get_customs_info_templates_customs_templates_edges, GET_CUSTOMS_TEMPLATES } from '@/graphql';
import { CustomsTemplateType } from '@/library/types';


type Edges = (get_customs_info_templates_customs_templates_edges | null)[];
type CustomInfoTemplatesQueryResult = LazyQueryResult<get_customs_info_templates, any> & {
  templates: CustomsTemplateType[];
  next?: string | null;
  previous?: string | null;
  load: (options?: any) => void;
  loadMore: (cursor?: string | null) => void;
};

export const CustomInfoTemplates = React.createContext<CustomInfoTemplatesQueryResult>({} as CustomInfoTemplatesQueryResult);

const CustomInfoTemplatesQuery: React.FC = ({ children }) => {
  const [load, result] = useLazyQuery<get_customs_info_templates>(GET_CUSTOMS_TEMPLATES);

  const extract = (edges?: Edges): CustomsTemplateType[] => (edges || []).map(item => item?.node as CustomsTemplateType);
  const loadMore = (cursor?: string | null) => result?.fetchMore && result.fetchMore({ variables: { cursor } });

  return (
    <CustomInfoTemplates.Provider value={{
      load,
      loadMore,
      templates: extract(result?.data?.customs_templates?.edges),
      next: result.data?.customs_templates?.pageInfo?.hasNextPage ? result.data?.customs_templates?.pageInfo?.endCursor : null,
      previous: result.data?.customs_templates?.pageInfo?.hasPreviousPage ? result.data?.customs_templates?.pageInfo?.startCursor : null,
      ...result
    }}>
      {children}
    </CustomInfoTemplates.Provider>
  );
};

export default CustomInfoTemplatesQuery;
