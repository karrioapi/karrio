import logging
from functools import reduce
from collections import OrderedDict
from typing import Callable, TypeVar, Any, Generic, List, Tuple, Dict

logger = logging.getLogger(__name__)
T = TypeVar("T")


class Job:
    def __init__(self, id: str, data: Any = None, fallback: Any = None, **extra):
        self.id: str = id
        self.data = data
        self.fallback = fallback
        for name, value in extra.items():
            self.__setattr__(name, value)


Step = Callable[[Any], Job]
Steps = Dict[str, Step]
Process = Callable[[Job], Any]


class Pipeline(Generic[T]):
    def __init__(self, **steps):
        self.steps: Steps = OrderedDict(steps.items())

    def __getitem__(self, step_name):
        return self.steps.get(step_name)

    def apply(self, process: Process, initial: List[T] = None) -> List[T]:
        if initial is None:
            initial = []

        def run(result: List[T], next_step: Tuple[str, Step]):
            name, step = next_step
            logger.debug(f"run step {name}...")
            last_run_result = result[-1] if len(result) > 0 else None
            job = step(last_run_result)
            return result + [process(job)]

        return reduce(run, self.steps.items(), initial)
