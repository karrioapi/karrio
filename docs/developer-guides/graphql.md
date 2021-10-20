# GraphQL API


## The Shipping App API

purplship leverage a GraphQL API to expose access to shipping related objects data available in the system.
GraphQL is a query language that allows clients to talk to an API server. Unlike REST, it gives the client 
control over how much or how little data they want to request about each object and allows relations within 
the object graph to be traversed easily.

To learn more about GraphQL language and its concepts, see the official [GraphQL website](https://graphql.org/).

The API endpoint is available at `/graphql/` and requires queries to be submitted using HTTP `POST` method and the 
`application/json` content type.


## GraphQL Playground

purplship exposes an interactive GraphQL editor under `/graphql/`, allowing access to the GraphQL API from your browser.

GraphQL Playground is an external interactive editor for your GraphQL queries. It is based on Graphiql and accessible 
through the web browser.

Using Playground is easy and intuitive with its sidebar navigation contain a listing of all operations available 
in the API. The Playground allows you to quickly familiarize yourself with the GraphQL API, perform example operations, 
and send your first queries.

!!! example ""
    <figure>
      <img src="/images/graphiQL.png" />
    </figure>

