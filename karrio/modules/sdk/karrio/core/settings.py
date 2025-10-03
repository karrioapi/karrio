"""Karrio Settings abstract class definition"""

import abc
import attr
import typing
import functools


@attr.s(auto_attribs=True)
class Settings(abc.ABC):
    """Unified API carrier connection settings (Interface)"""

    carrier_id: str
    account_country_code: str = None
    test_mode: bool = False
    metadata: dict = {}
    config: dict = {}
    id: str = None
    tracer = None  # Will be set during Gateway initialization

    @property
    def carrier_name(self) -> typing.Optional[str]:
        return None

    @property
    def server_url(self) -> typing.Optional[str]:
        return None

    @property
    def tracking_url(self) -> typing.Optional[str]:
        return None

    @property
    def connection_config(self):
        import karrio.lib as lib

        return lib.to_connection_config(
            self.config or {},
            option_type=lib.units.create_enum(
                "ConnectionConfig",
                dict(
                    label_type=lib.units.create_enum(
                        "LabelType", ["PDF", "ZPL"]
                    ),
                )
            ),
        )

    @property
    def connection_cache(self):
        import karrio.lib as lib

        return getattr(self, "cache", None) or lib.Cache()

    def trace(self, *args, **kwargs):
        if self.tracer is None:
            import karrio.lib as lib
            self.tracer = lib.Tracer()

        return self.tracer.with_metadata(
            dict(
                connection=dict(
                    id=self.id,
                    test_mode=self.test_mode,
                    carrier_id=self.carrier_id,
                    carrier_name=self.carrier_name,
                )
            )
        )(*args, **kwargs)

    def trace_as(self, format: str):
        return functools.partial(self.trace, format=format)
