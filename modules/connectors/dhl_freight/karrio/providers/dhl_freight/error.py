import karrio.core.models as models
import karrio.lib as lib
import karrio.providers.dhl_freight.utils as provider_utils
import karrio.schemas.dhl_freight.error_response as dhl_freight_err


def parse_error_response(
    responses: list[dict] | dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> list[models.Message]:
    """Parse the three DHL Freight error shapes. See SPECS.md "Error parsing".

    1. Booking validation: ``{status: "Error", validationErrors: [{errorCode,
       message, field}]}`` (the ``sendtransportinstruction`` endpoint).
    2. RFC-7807 ``problem+json``: ``{statusCode|status, title, detail,
       instance, invalidParams}`` (DHL gateway).
    3. OAuth2 token error: ``{error, error_description}`` (auth endpoint).
    """
    results = responses if isinstance(responses, list) else [responses]
    errors: list[dict] = [
        r
        for r in results
        if r.get("validationErrors")
        or (r.get("statusCode") and int(r.get("statusCode", 200)) >= 400)
        or r.get("error")
        or str(r.get("status") or "").lower() == "error"
        or r.get("title", "").lower() not in ("", "ok")
    ]

    messages: list[models.Message] = []
    for raw in errors:
        typed = lib.to_object(dhl_freight_err.ErrorResponseType, raw)

        # 1. Booking validation errors — one message per entry.
        for ve in typed.validationErrors or []:
            messages.append(
                models.Message(
                    carrier_id=settings.carrier_id,
                    carrier_name=settings.carrier_name,
                    code=str(ve.errorCode or "validation_error"),
                    message=ve.message,
                    details=lib.to_dict(dict(field=ve.field)),
                )
            )

        if typed.validationErrors:
            continue

        # 2/3. Gateway problem+json / OAuth2 token error.
        # `error_description` is read from the raw dict (kcli flattens it to
        # `errordescription`); the rest come from the typed object.
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=str(typed.statusCode or typed.error or raw.get("code") or "unknown"),
                message=(raw.get("error_description") or typed.detail or raw.get("message") or typed.title),
                details=lib.to_dict(
                    dict(
                        title=typed.title,
                        instance=typed.instance,
                        invalidParams=raw.get("invalidParams"),
                    )
                ),
            )
        )

    return messages
