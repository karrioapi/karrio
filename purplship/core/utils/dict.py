import attr
import json
from typing import Union, Any, TypeVar

T = TypeVar("T")


@attr.s(auto_attribs=True)
class JWrapper:
    value: Any


class DICTPARSE:

    @staticmethod
    def jsonify(entity: Union[dict, T]) -> str:
        """Return a JSON.

        recursively parse a data type using __dict__ into a JSON
        """
        return json.dumps(
            attr.asdict(JWrapper(value=entity)).get("value"),
            default=lambda o: o.__dict__ if hasattr(o, "__dict__") else o,
            sort_keys=True,
            indent=4,
        )

    @staticmethod
    def to_dict(entity: Any) -> dict:
        """Return a python dictionary.

        recursively parse a data type using __dict__ into a JSON
        """
        return json.loads(
            DICTPARSE.jsonify(entity) if not isinstance(entity, str) else entity,
            object_hook=lambda d: {k: v for k, v in d.items() if v not in (None, [], "")},
        )

