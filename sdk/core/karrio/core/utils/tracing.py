import uuid
import attr
import time
import typing
import functools
import concurrent.futures as futures

Trace = typing.Callable[[typing.Any, str], typing.Any]


@attr.s(auto_attribs=True)
class Record:
    key: str
    data: typing.Any
    timestamp: float
    metadata: dict = {}


@attr.s(auto_attribs=True)
class Tracer:
    id: str = attr.ib(factory=lambda: str(uuid.uuid4()))
    _recordings: typing.Dict[futures.Future, dict] = {}
    _context: typing.Dict[str, typing.Any] = {}

    def trace(
        self, data: typing.Any, key: str, metadata: dict = {}, format: str = None
    ) -> typing.Any:
        def _save():
            return Record(
                key=key,
                data={"format": format, **data},
                timestamp=time.time(),
                metadata=metadata,
            )

        promise = futures.ThreadPoolExecutor(max_workers=1)
        self._recordings.update({promise.submit(_save): data})

        return data

    def with_metadata(self, metadata: dict):
        return functools.partial(self.trace, metadata=metadata)

    @property
    def records(self) -> typing.List[Record]:
        return [rec.result() for rec in futures.as_completed(self._recordings)]

    @property
    def context(self) -> typing.Dict[str, typing.Any]:
        return self._context

    def add_context(self, data: typing.Dict[str, typing.Any]):
        self._context.update(data)
