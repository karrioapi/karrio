from collections import OrderedDict
from collections.abc import Callable
from functools import reduce
from typing import Any, Generic, TypeVar

from karrio.core.utils.logger import logger

T = TypeVar("T")


class Job:
    def __init__(self, id: str, data: Any = None, fallback: Any = None, **extra):
        self.id: str = id
        self.data = data
        self.fallback = fallback
        for name, value in extra.items():
            self.__setattr__(name, value)


Step = Callable[[Any], Job]
Steps = dict[str, Step]
Process = Callable[[Job], Any]


class Pipeline(Generic[T]):
    def __init__(self, **steps):
        self.steps: Steps = OrderedDict(steps.items())  # type: ignore

    def __getitem__(self, step_name):
        return self.steps.get(step_name)

    def apply(self, process: Process, initial: list[T] = None) -> list[T]:
        if initial is None:
            initial = []

        def run(result: list[T], next_step: tuple[str, Step]):
            name, step = next_step
            logger.debug("Running pipeline step", step_name=name)
            last_run_result = result[-1] if len(result) > 0 else None
            job = step(last_run_result)
            return result + [process(job)]

        return reduce(run, self.steps.items(), initial)
