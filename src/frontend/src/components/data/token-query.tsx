import React from 'react';
import { QueryResult, useQuery } from '@apollo/client';
import { GetToken, GetToken_token, GET_TOKEN } from '@/graphql';

export type TokenType = GetToken_token;
type TokenDataType = Partial<QueryResult<GetToken>> & { token: TokenType };

export const TokenData = React.createContext<TokenDataType>({} as TokenDataType);

const TokenQuery: React.FC = ({ children }) => {
  const result = useQuery<GetToken>(GET_TOKEN);

  return (
    <TokenData.Provider value={{ token: (result?.data?.token || {} as TokenType), ...result }}>
      {children}
    </TokenData.Provider>
  );
};

export default TokenQuery;
