import karrio
import karrio.lib as lib

cached_payment_method_id = {
    f"payment|freightcom|net_terms|api_key": dict(
        id="string",
        type= "net-terms",
        label="Net Terms"
    )
}
gateway = karrio.gateway["freightcom"].create(
    dict(
        api_key="api_key",
        config=dict(
            payment_method_type="net_terms"
        )
    ),
    cache=lib.Cache(**cached_payment_method_id),
)
