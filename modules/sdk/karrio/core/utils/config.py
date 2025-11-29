"""Karrio system configuration utilities module."""

import abc
import typing


class AbstractSystemConfig(abc.ABC):
    """Abstract base class for system configuration."""

    @abc.abstractmethod
    def get(self, key: str, default: typing.Any = None) -> typing.Any:
        """Get a configuration value by key."""
        ...

    @abc.abstractmethod
    def __getitem__(self, key: str) -> typing.Any:
        """Get a configuration value by key."""
        ...

    @abc.abstractmethod
    def __contains__(self, key: str) -> bool:
        """Check if key exists in config."""
        ...


class SystemConfig(AbstractSystemConfig):
    """System configuration utility.

    Works as a simple dictionary by default but can be configured
    with an external config backend (e.g., Django constance).
    """

    def __init__(
        self,
        config: typing.Optional[AbstractSystemConfig] = None,
        **kwargs,
    ) -> None:
        self._config = config  # external config backend
        self._values: typing.Dict[str, typing.Any] = kwargs  # local values

    def get(self, key: str, default: typing.Any = None) -> typing.Any:
        """Get a configuration value by key.

        Checks local values first, then external config backend.
        """
        if key in self._values:
            return self._values[key]

        if self._config is not None:
            return self._config.get(key, default)

        return default

    def __getitem__(self, key: str) -> typing.Any:
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __contains__(self, key: str) -> bool:
        if key in self._values:
            return True
        if self._config is not None:
            return key in self._config
        return False

    def set(self, key: str, value: typing.Any) -> None:
        """Set a local configuration value."""
        self._values[key] = value
