# Extensibility

The obvious way to extend the Purplship Server would be to download the source code and modify it directly. 
After all it's an open-source platform. We advise against this as experience teaches us that once your store 
diverges from the upstream Purplship Server, it becomes hard to keep it updated. 

Because of this we advice the use development of `Apps` that are external applications that talk to Purplship Server 
using its GraphQL and REST APIs additionally, they can subscribe to events using webhooks.


<figure>
  <img src="/images/purplship-apps-architecture.svg" height="300" />
</figure>
