import React from 'react';
import { LazyQueryResult, useLazyQuery } from '@apollo/client';
import { get_user_connections, GET_USER_CONNECTIONS, get_user_connections_user_connections } from '@/graphql';


export type UserConnectionType = get_user_connections_user_connections;

type UserConnectionsQueryResult = LazyQueryResult<get_user_connections, any> & {
  user_connections: UserConnectionType[];
  load: (options?: any) => void;
};

export const UserConnections = React.createContext<UserConnectionsQueryResult>({} as UserConnectionsQueryResult);

const UserConnectionsQuery: React.FC = ({ children }) => {
  const [load, result] = useLazyQuery<get_user_connections>(GET_USER_CONNECTIONS);

  const extract = (results: any[]): UserConnectionType[] => results.filter(r => r !== null);

  return (
    <UserConnections.Provider value={{ load, user_connections: extract(result.data?.user_connections || []), ...result }}>
      {children}
    </UserConnections.Provider>
  );
};

export default UserConnectionsQuery;
