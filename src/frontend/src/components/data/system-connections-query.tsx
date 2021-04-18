import React from 'react';
import { LazyQueryResult, useLazyQuery } from '@apollo/client';
import { get_system_connections, GET_SYSTEM_CONNECTIONS, get_system_connections_system_connections } from '@/graphql';


export type SystemConnectionType = get_system_connections_system_connections;

type SystemConnectionsQueryResult = LazyQueryResult<get_system_connections, any> & {
  system_connections: SystemConnectionType[];
  load: (options?: any) => void;
};

export const SystemConnections = React.createContext<SystemConnectionsQueryResult>({} as SystemConnectionsQueryResult);

const SystemConnectionsQuery: React.FC = ({ children }) => {
  const [load, result] = useLazyQuery<get_system_connections>(GET_SYSTEM_CONNECTIONS);

  const extract = (results: any[]): SystemConnectionType[] => (results).filter(r => r !== null);

  return (
    <SystemConnections.Provider  value={{ load, system_connections: extract(result.data?.system_connections || []), ...result }}>
      {children}
    </SystemConnections.Provider>
  );
};

export default SystemConnectionsQuery;
