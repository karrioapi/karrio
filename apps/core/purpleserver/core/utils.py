import functools
from typing import TypeVar, Union, Callable, Any, List

T = TypeVar('T')


def identity(value: Union[Any, Callable]) -> T:
    """
    :param value: function or value desired to be wrapped
    :return: value or callable return
    """
    return value() if callable(value) else value


def post_processing(methods: List[str] = None):

    def class_wrapper(klass):
        setattr(klass, 'post_process_functions', getattr(klass, 'post_process_functions') or [])

        for name in methods:
            method = getattr(klass, name)

            def wrapper(*args, **kwargs):
                result = method(*args, **kwargs)
                processes = klass.post_process_functions
                return functools.reduce(
                    lambda processed_result, process: process(processed_result), processes, result
                )

            setattr(klass, name, wrapper)

        return klass

    return class_wrapper
