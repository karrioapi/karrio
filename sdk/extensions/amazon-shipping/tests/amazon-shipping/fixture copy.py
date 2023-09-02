import karrio

gateway = karrio.gateway["amazon_mws"].create(
    dict(
        seller_id="SELLER_ID",
        developer_id="DEVELOPER_ID",
        mws_auth_token="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        x_amz_access_token="amzn.mws.a8b4e7a6-f0b4-4b0a-b0b4-b0b4b0b4b0b4",
    )
)
