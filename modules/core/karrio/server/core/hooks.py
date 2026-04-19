"""
Lightweight hook system for extending class methods.

This module is intentionally free of karrio.server.core imports to avoid
circular dependencies. It can be safely imported from model modules.

Usage::

    from karrio.server.core.hooks import hookable

    @hookable
    class MyModel(models.Model):
        def get_credentials(self, user_id=None):
            return dict(self.credentials or {})

    # Later, in an extension module's AppConfig.ready():
    MyModel.hooks.before("get_credentials", validate_access)
    MyModel.hooks.after("get_credentials", decrypt_fields)
    MyModel.hooks.override("get_credentials", encrypted_get)
"""

import contextlib
import functools
import typing
from collections.abc import Callable


class HookError(Exception):
    """Raised when a hook is misconfigured or returns an invalid value."""

    pass


class HookRegistry:
    """
    Lazy hook registry for a @hookable class.

    Supports three phases:
    - before: validation/gating — raise to abort, return value ignored
    - after:  result transformation — MUST return a value
    - override: replaces the original method entirely (at most one per method)

    Execution order: before hooks → override OR original → after hooks.
    """

    def __init__(self, klass):
        self._klass = klass
        self._hooks: dict[str, dict[str, typing.Any]] = {}
        self._originals: dict[str, typing.Any] = {}
        self._wrapped: set[str] = set()

    def before(self, name: str, fn: Callable) -> None:
        """Register a before hook. Receives the same args as the method."""
        self._ensure_wrapped(name)
        self._hooks[name]["before"].append(fn)

    def after(self, name: str, fn: Callable) -> None:
        """Register an after hook. Receives (result, *args, **kwargs), must return."""
        self._ensure_wrapped(name)
        self._hooks[name]["after"].append(fn)

    def override(self, name: str, fn: Callable) -> None:
        """Register an override (replaces original). At most one per method."""
        self._ensure_wrapped(name)
        if self._hooks[name]["override"] is not None:
            raise HookError(f"Override already registered for {self._klass.__name__}.{name}")
        self._hooks[name]["override"] = fn

    def remove(self, name: str, phase: str, fn: Callable) -> None:
        """Remove a previously registered hook."""
        if name not in self._hooks:
            return
        if phase == "override":
            self._hooks[name]["override"] = None
        else:
            with contextlib.suppress(ValueError):
                self._hooks[name][phase].remove(fn)

    class _Scoped:
        """Context manager for temporary hook registration (useful in tests)."""

        def __init__(self, registry: "HookRegistry", name: str, phase: str, fn: Callable):
            self._registry = registry
            self._name = name
            self._phase = phase
            self._fn = fn

        def __enter__(self):
            if self._phase == "override":
                self._registry.override(self._name, self._fn)
            elif self._phase == "before":
                self._registry.before(self._name, self._fn)
            else:
                self._registry.after(self._name, self._fn)
            return self

        def __exit__(self, *exc):
            self._registry.remove(self._name, self._phase, self._fn)
            return False

    def scoped(self, name: str, phase: str, fn: Callable) -> "_Scoped":
        """Temporarily register a hook for the duration of a with-block."""
        return self._Scoped(self, name, phase, fn)

    # ── internal ──────────────────────────────────────────────────────

    def _ensure_wrapped(self, name: str) -> None:
        """Lazily wrap a method/property on first hook registration."""
        if name in self._wrapped:
            return

        raw = self._klass.__dict__.get(name)
        resolved = getattr(self._klass, name, None)

        if raw is None and resolved is None:
            raise HookError(f"{self._klass.__name__} has no attribute '{name}'")

        self._hooks[name] = {"before": [], "after": [], "override": None}
        hooks_ref = self._hooks

        if isinstance(raw, staticmethod):
            original = raw.__func__
            self._originals[name] = original

            @functools.wraps(original)
            def static_wrapper(*args, **kwargs):
                return self._execute(name, hooks_ref, original, args, kwargs)

            setattr(self._klass, name, staticmethod(static_wrapper))

        elif isinstance(raw, classmethod):
            original = raw.__func__
            self._originals[name] = original

            @functools.wraps(original)
            def cls_wrapper(*args, **kwargs):
                return self._execute(name, hooks_ref, original, args, kwargs)

            setattr(self._klass, name, classmethod(cls_wrapper))

        elif isinstance(raw, property):
            original_fget = raw.fget
            self._originals[name] = original_fget

            @functools.wraps(original_fget)
            def prop_wrapper(instance):
                return self._execute(name, hooks_ref, original_fget, (instance,), {})

            setattr(
                self._klass,
                name,
                property(prop_wrapper, raw.fset, raw.fdel, raw.__doc__),
            )

        else:
            original = resolved if resolved is not None else raw
            self._originals[name] = original

            @functools.wraps(original)
            def method_wrapper(*args, **kwargs):
                return self._execute(name, hooks_ref, original, args, kwargs)

            setattr(self._klass, name, method_wrapper)

        self._wrapped.add(name)

    @staticmethod
    def _execute(name, hooks_ref, original, args, kwargs):
        method_hooks = hooks_ref[name]

        # Phase 1: before hooks
        for fn in method_hooks["before"]:
            fn(*args, **kwargs)

        # Phase 2: override or original
        override = method_hooks["override"]
        result = override(*args, **kwargs) if override is not None else original(*args, **kwargs)

        # Phase 3: after hooks
        for fn in method_hooks["after"]:
            new_result = fn(result, *args, **kwargs)
            if new_result is None and result is not None:
                raise HookError(
                    f"After hook '{fn.__name__}' on '{name}' returned None — after hooks must return a value"
                )
            result = new_result

        return result


def hookable(klass):
    """
    Mark a class as extensible via hooks.

    Usage::

        @hookable
        class Rates:
            def fetch(self, payload): ...

        # Later, in an extension module's AppConfig.ready():
        Rates.hooks.before("fetch", validate_limits)
        Rates.hooks.after("fetch", apply_markups)
        Rates.hooks.override("fetch", custom_fetch)

    No methods are wrapped at decoration time — wrapping happens lazily
    on first hook registration, so unhookable methods pay zero cost.
    """
    klass.hooks = HookRegistry(klass)
    return klass
