import { ApolloClient, InMemoryCache } from '@apollo/client';

export const graphClient = new ApolloClient({
  uri: '/graphql',
  cache: new InMemoryCache({ addTypename: false })
});
