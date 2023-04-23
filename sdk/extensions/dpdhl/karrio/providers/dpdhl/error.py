from urllib.error import HTTPError
import dpdhl_lib.business_interface as dpdhl
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.dpdhl.utils as provider_utils


def parse_error_response(
    response: lib.Element,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    return [
        *_parse_xml_error_response(response, settings, **kwargs),
        *_parse_html_error_response(response, settings, **kwargs),
        *_parse_data_error_response(response, settings, **kwargs),
    ]


def _parse_data_error_response(
    response: lib.Element,
    settings: provider_utils.Settings,
) -> models.Message:
    if (
        str(response.tag).endswith("data")
        and response.get("code") is not None
        and response.get("code") != "0"
    ):
        return [
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                message=response.get("error"),
                code=response.get("code"),
            )
        ]

    return []


def _parse_xml_error_response(
    response: lib.Element,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    errors: typing.List[dpdhl.Statusinformation] = [
        status
        for status in lib.find_element("Status", response, dpdhl.Statusinformation)
        if (status.statusText != "ok")
    ]

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=error.statusCode,
            message=error.statusText,
            details={
                **(
                    lib.failsafe(
                        lambda: lib.to_dict(
                            {
                                "message": lib.join(
                                    *[
                                        _
                                        for _ in error.statusMessage
                                        if isinstance(_, str)
                                    ],
                                    join=" ",
                                )
                            }
                        )
                    )
                    or {}
                    if any(error.statusMessage or [])
                    else {}
                ),
                **(
                    lib.failsafe(
                        lambda: lib.to_dict(
                            {
                                "error": lib.join(
                                    *[
                                        f"{_.statusElement}: {_.statusMessage}"
                                        for _ in error.errorMessage
                                    ],
                                    join=" ",
                                )
                            }
                        )
                    )
                    or {}
                    if any(error.errorMessage or [])
                    else {}
                ),
                **(
                    lib.failsafe(
                        lambda: lib.to_dict(
                            {
                                "warning": lib.join(
                                    *(
                                        [
                                            _
                                            for _ in error.warningMessage
                                            if isinstance(_, str)
                                        ]
                                        if isinstance(error.warningMessage, list)
                                        else (
                                            [error.warningMessage]
                                            if isinstance(error.warningMessage, str)
                                            else []
                                        )
                                    ),
                                    join=" ",
                                )
                            }
                        )
                    )
                    or {}
                    if any(error.warningMessage or [])
                    else {}
                ),
                **kwargs,
            },
        )
        for error in errors
    ]


def _parse_html_error_response(
    response: lib.Element,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    body = lib.find_element("body", response, first=True)

    if body is None:
        return []

    return [
        models.Message(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            code=lib.find_element("h1", body, first=True).text,
            message=lib.find_element("p", body, first=True).text,
        )
    ]
