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

class Tracer:
    def __init__(self, id: str = None) -> None:
        self.id = id or str(uuid.uuid4())
        self.inner_context: typing.Dict[str, typing.Any] = {}
        self.inner_recordings: typing.Dict[futures.Future, dict] = {}

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
        self.inner_recordings.update({promise.submit(_save): data})

        return data

    def with_metadata(self, metadata: dict):
        return functools.partial(self.trace, metadata=metadata)

    @property
    def records(self) -> typing.List[Record]:
        return [rec.result() for rec in futures.as_completed(self.inner_recordings)]

    @property
    def context(self) -> typing.Dict[str, typing.Any]:
        return self.inner_context

    def add_context(self, data: typing.Dict[str, typing.Any]):
        self.inner_context.update(data)
