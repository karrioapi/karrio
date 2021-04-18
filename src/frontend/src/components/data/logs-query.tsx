import React from 'react';
import { LazyQueryResult, useLazyQuery } from '@apollo/client';
import { get_logs, GET_LOGS, get_logs_logs_edges, PageInfo } from '@/graphql';
import { LogType } from '@/library/types';


type Edges = (get_logs_logs_edges | null)[];
type LogsType = LazyQueryResult<get_logs, any> & { 
  logs: LogType[];
  next?: string | null;
  previous?: string | null;
  load: (options?: any) => void;
  loadMore: (cursor?: string | null) => void;
};

export const Logs = React.createContext<LogsType>({} as LogsType);

const LogsQuery: React.FC = ({ children }) => {
  const [load, result] = useLazyQuery<get_logs>(GET_LOGS);

  const extract = (edges?: Edges) => (edges || []).map(item => item?.node as LogType);
  const loadMore = (cursor?: string | null) => result?.fetchMore && result.fetchMore({ variables: { cursor } });

  return (
    <Logs.Provider value={{
      load,
      loadMore,
      logs: extract(result?.data?.logs?.edges),
      next: result.data?.logs?.pageInfo?.hasNextPage ? result.data?.logs?.pageInfo?.endCursor : null,
      previous: result.data?.logs?.pageInfo?.hasPreviousPage ? result.data?.logs?.pageInfo?.startCursor : null,
      ...result
    }}>
      {children}
    </Logs.Provider>
  );
};

export default LogsQuery;
