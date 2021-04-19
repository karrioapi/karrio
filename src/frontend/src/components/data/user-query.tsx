import React from 'react';
import { QueryResult, useQuery } from '@apollo/client';
import { GetUser, GetUser_user, GET_USER } from '@/graphql';

export type UserType = GetUser_user;
type UserDataType = QueryResult<GetUser> & { user: UserType };

export const UserData = React.createContext<UserDataType>({} as UserDataType);

const UserQuery: React.FC = ({ children }) => {
  const result = useQuery<GetUser>(GET_USER);

  return (
    <UserData.Provider value={{ user: result.data?.user as UserType, ...result }}>
      {children}
    </UserData.Provider>
  );
};

export default UserQuery;
