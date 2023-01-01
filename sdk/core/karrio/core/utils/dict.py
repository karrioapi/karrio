import enum
import attr
import json
import types
import jstruct.utils as jstruct
from typing import Union, Any, TypeVar, Callable, Type, Optional

T = TypeVar("T")


class DICTPARSE:
    @staticmethod
    def jsonify(entity: Union[dict, Any]) -> str:
        """Serialize value to JSON.

        :param value: a value that can be serialized to JSON.
        :return: a string.
        """

        def _parser(item):
            if attr.has(item):
                if isinstance(item, Callable) and hasattr(item, "__name__"):
                    return item.__name__
                return attr.asdict(item)
            if isinstance(item, types.FunctionType):
                return None
            if isinstance(item, type):
                return str(item)
            if isinstance(item, Callable):
                return str(item)
            if isinstance(item, enum.Enum):
                return item.value
            if hasattr(item, "__dict__"):
                return item.__dict__

            return item

        return json.dumps(
            entity,
            default=_parser,
            sort_keys=True,
            indent=4,
        )

    @staticmethod
    def to_dict(entity: Any, clear_empty: bool = None) -> dict:
        """Parse value into a Python dictionay.

        :param value: a value that can converted in dictionary.
        :return: a dictionary.
        """
        _clear_empty = clear_empty is not False
        return json.loads(
            (
                DICTPARSE.jsonify(entity)
                if not isinstance(entity, (str, bytes))
                else entity
            ),
            object_hook=lambda d: {
                k: v
                for k, v in d.items()
                if (v not in (None, [], "") if _clear_empty else True)
            },
        )

    @staticmethod
    def to_object(object_type: Type[T], data: dict = None) -> Optional[T]:
        """Create an instance of "object_type" from the "data".

        :param object_type: an object class.
        :param data: the data to pass for intantiation.
        :return: an object instance or None.
        """
        if data is None or object_type is None:
            return None

        entity: object_type = jstruct.instantiate(object_type, data)  # type: ignore
        return entity
