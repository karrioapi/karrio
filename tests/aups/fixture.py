from purplship.mappers.aups import AustraliaPostClient, AustraliaPostProxy

proxy = AustraliaPostProxy(
    AustraliaPostClient(
        server_url="https://digitalapi.auspost.com.au/test",
        username="username",
        password="password",
        account_number="1234567",
    )
)
