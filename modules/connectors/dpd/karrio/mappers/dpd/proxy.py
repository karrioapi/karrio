"""Karrio DPD client proxy."""

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.core.errors as errors
import karrio.schemas.dpd.LoginServiceV21 as dpd
import karrio.providers.dpd.error as provider_error
import karrio.mappers.dpd.settings as provider_settings
import karrio.universal.mappers.rating_proxy as rating_proxy


class Proxy(rating_proxy.RatingMixinProxy, proxy.Proxy):
    settings: provider_settings.Settings

    def authenticate(self, _=None) -> lib.Deserializable[dict]:
        """Retrieve the auth token using the delis_id|password pair
        or collect it from the cache if an unexpired token exist.
        """
        cache_key = f"{self.settings.carrier_name}|{self.settings.delis_id}|{self.settings.password}"

        def _extract_login_details(node: lib.Element):
            data: dpd.GetAuthResponseDto = lib.find_element(
                "return",
                node,
                dpd.GetAuthResponseDto,
                first=True,
            )
            return dict(
                depot=data.depot,
                token=data.authToken,
                expiry=lib.fdatetime(
                    data.authTokenExpires,
                    current_format="%Y-%m-%dT%H:%M:%S.%f",
                ),
            )

        def get_token():
            result = lib.request(
                url=f"{self.settings.server_url}/soap/services/LoginService/V2_1",
                data=lib.envelope_serializer(
                    lib.Envelope(
                        Header=lib.Header(),
                        Body=lib.Body(
                            dpd.getAuth(
                                delisId=self.settings.delis_id,
                                password=self.settings.password,
                                messageLanguage=self.settings.message_language,
                            )
                        ),
                    ),
                    namespace=(
                        'xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
                        'xmlns:ns="http://dpd.com/common/service/types/LoginService/2.1"'
                    ),
                    prefixes=dict(
                        Envelope="soapenv",
                        getAuth="ns",
                        delisId="",
                        password="",
                        messageLanguage="",
                    ),
                ),
                method="POST",
                headers={
                    "Content-Type": "text/xml;charset=UTF-8",
                    "SOAPAction": "http://dpd.com/common/service/types/LoginService/2.1/getAuth",
                },
                max_retries=2,
            )
            response = lib.to_element(result)
            messages = provider_error.parse_error_response(response, self.settings)

            if any(messages):
                raise errors.ParsedMessagesError(messages=messages)

            return _extract_login_details(response)

        token = self.settings.connection_cache.thread_safe(
            refresh_func=get_token,
            cache_key=cache_key,
            buffer_minutes=30,
            token_field="token",
        )

        return lib.Deserializable(token.get_state())

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        return super().get_rates(request)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        access_token = self.authenticate().deserialize()
        response = lib.request(
            url=f"{self.settings.server_url}/soap/services/ShipmentService/V3_3",
            data=request.serialize().replace("[AUTH_TOKEN]", access_token),
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "text/xml;charset=UTF-8",
                "SOAPAction": "http://dpd.com/common/service/types/ShipmentService/3.3/storeOrders",
            },
        )

        return lib.Deserializable(response, lib.to_element)

    def get_tracking(self, requests: lib.Serializable) -> lib.Deserializable:
        access_token = self.authenticate().deserialize()

        def _track(payload):
            tracking_number, data = payload
            return tracking_number, lib.request(
                url=f"{self.settings.server_url}/soap/services/ParcelLifeCycleService/V2_0",
                trace=self.trace_as("xml"),
                method="POST",
                data=data.replace("[AUTH_TOKEN]", access_token),
                headers={
                    "Content-Type": "text/xml;charset=UTF-8",
                    "SOAPAction": "http://dpd.com/common/service/types/ParcelLifeCycleService/2.0/getTrackingData",
                },
            )

        responses = lib.run_concurently(_track, requests.serialize().items())

        return lib.Deserializable(
            responses,
            lambda results: [(res[0], lib.to_element(res[1])) for res in results],
        )
