# Architecture Overview

Purplship has three main components:

1. The first component is the Purplship SDK which unifies and standardize
   the communication to shipping carriers to one interface. It is designed
   to be extensible to allow integration of additional carrier support.

2. The second component is the Purplship Server which is the backend server
   that exposes a Shipping REST API, a GraphQL API and a Shipping Web App. 
   The server is written in Python with Django. It maintains its state in a 
   PostgresSQL database.

3. The third component is the Purplship Web App which implements the user
   interface that operation members can be used to manage fulfilment processes.
   the app is a React application that runs in the browser and talks to the
   Purplship server using the REST and Graph APIs.
   
   
<figure>
  <img src="/images/purplship-server-architecture.svg" height="300" />
</figure>
