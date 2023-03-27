import typing
import concurrent.futures as futures


class AbstractCache:
    def get(self, key: str):
        pass

    def set(self, key: str, value: typing.Any, **kwargs):
        pass


class Cache:
    def __init__(self, cache: typing.Optional[AbstractCache] = None, **kwargs) -> None:
        self._cache = cache  # system cache
        self._values: typing.Dict[str, futures.Future] = {}  # shallow cache

        for key, value in kwargs.items():
            self.set(key, value)

    def get(self, key: str):
        _value = self._values.get(key)
        _cache_value = None if self._cache is None else self._cache.get(key)
        _result = None

        if _value is not None:
            _result = _value.result()

        if self._cache is not None and _cache_value is not None:
            _result = _cache_value

        # sync value in shallow cache if it only exist in the cache
        if _value is None and _cache_value is not None:
            self.set(key, _cache_value)

        # sync value in cache if it only exist shallow cache
        if _cache_value is None and _value is not None and self._cache is not None:
            self._cache.set(key, _cache_value)

        return _result

    def set(self, key: str, value: typing.Any, timeout: int = 86400):
        def _save():
            if isinstance(value, typing.Callable):
                return value()

            return value

        executor = futures.ThreadPoolExecutor(max_workers=1)
        promise = executor.submit(_save)
        self._values.update({key: promise})

        # set value in cache if it exist
        if self._cache is not None:
            promise.add_done_callback(lambda _: self._cache.set(key, _.result(), timeout=timeout))
