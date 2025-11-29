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
    cache = None  # Will be set during Gateway initialization
    system_config = None  # Will be set during Gateway initialization

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
                    label_type=lib.units.create_enum("LabelType", ["PDF", "ZPL"]),
                ),
            ),
        )

    @property
    def connection_cache(self):
        import karrio.lib as lib

        return getattr(self, "cache", None) or lib.Cache()

    @property
    def connection_system_config(self):
        import karrio.lib as lib

        return getattr(self, "system_config", None) or lib.SystemConfig()

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

    @classmethod
    def as_stub(cls, settings: typing.Optional[dict] = None) -> "Settings":
        """
        Create a stub instance of the Settings class with placeholder values
        for any required fields that are not provided.

        This is useful for creating a Settings instance when you don't have
        all the required credentials but need the settings object for
        operations that don't require authentication (e.g., OAuth flow).

        Args:
            settings: Optional dictionary of settings values to use

        Returns:
            A Settings instance with stub values for missing required fields
        """
        settings = settings or {}
        stub_settings = dict(settings)

        # Get attrs field definitions
        for field in getattr(cls, "__attrs_attrs__", []):
            # Skip if already provided
            if field.name in stub_settings:
                continue

            # Check if field is required (has no default or default is NOTHING)
            has_default = field.default is not attr.NOTHING
            if has_default:
                continue

            # Generate stub value based on field type
            field_type = field.type
            if field_type is str or field_type == "str":
                stub_settings[field.name] = ""
            elif field_type is int or field_type == "int":
                stub_settings[field.name] = 0
            elif field_type is float or field_type == "float":
                stub_settings[field.name] = 0.0
            elif field_type is bool or field_type == "bool":
                stub_settings[field.name] = False
            elif field_type is dict or field_type == "dict":
                stub_settings[field.name] = {}
            elif field_type is list or field_type == "list":
                stub_settings[field.name] = []
            else:
                # Default to empty string for unknown types
                stub_settings[field.name] = ""

        return cls(**stub_settings)
