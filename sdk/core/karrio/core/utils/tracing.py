import uuid
import attr
import time
import typing
import functools
import concurrent.futures as futures

T = typing.TypeVar("T")
Trace = typing.Callable[[T, str], T]


@attr.s(auto_attribs=True)
class Record:
    key: str
    data: typing.Any
    timestamp: float
    metadata: dict = {}


@attr.s(auto_attribs=True)
class Tracer:
    id: str = attr.ib(factory=lambda: str(uuid.uuid4()))
    callback: typing.Callable[[Record], typing.Any] = None
    records: typing.List[Record] = attr.field(default=[])

    def trace(self, data: typing.Any, key: str, metadata: dict = None) -> typing.Any:
        self._save(Record(key=key, data=data, metadata=metadata, timestamp=time.time()))

        return data

    def with_key(self, key: str):
        return functools.partial(self.trace, key=key)

    def _save(self, record: Record):
        def actual_save():
            if self.callback:
                self.callback(record)

            self.records = [
                *(self.records or []),
                record,
            ]

        with futures.ThreadPoolExecutor(max_workers=1) as promise:
            promise.submit(actual_save)
