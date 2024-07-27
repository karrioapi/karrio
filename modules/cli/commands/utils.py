import pydoc
import importlib
import karrio.lib as lib


class CarrierFeatures(lib.StrEnum):
    tracking = "tracking"
    rating = "rating"
    shipping = "shipping"
    pickup = "pickup"
    address = "address"
    document = "document"
    manifest = "manifest"


DEFAULT_FEATURES = [
    "tracking",
    "rating",
    "shipping",
]


def gen(entity):
    return pydoc.render_doc(entity, renderer=pydoc.plaintext)


def format_dimension(code, dim):
    return (
        f"| `{ code }` "
        f'| { f" x ".join([str(d) for d in dim.values() if isinstance(d, float)]) } '
        f'| { f" x ".join([k for k in dim.keys() if isinstance(dim[k], float)]) }'
    )


def instantiate_tree(cls, indent=0, alias=""):
    tree = f"{alias}{cls.__name__}(\n"
    indent += 1
    items = cls.__annotations__.items() if hasattr(cls, "__annotations__") else []

    for name, typ in items:
        if typ.__name__ == "Optional" and hasattr(typ, "__args__"):
            typ = typ.__args__[0]
        if typ.__name__ == "List" and hasattr(typ, "__args__"):
            typ = typ.__args__[0]
            if hasattr(typ, "__annotations__"):
                tree += (
                    " " * indent * 4
                    + f"{name}=[\n"
                    + " " * (indent + 1) * 4
                    + f"{instantiate_tree(typ, indent + 1, alias=alias)}\n"
                    + " " * indent * 4
                    + "],\n"
                )
            else:
                tree += " " * indent * 4 + f"{name}=[],\n"
        elif hasattr(typ, "__annotations__"):
            tree += (
                " " * indent * 4
                + f"{name}={instantiate_tree(typ, indent, alias=alias)},\n"
            )
        else:
            tree += " " * indent * 4 + f"{name}=None,\n"

    tree += " " * (indent - 1) * 4 + ")"
    return tree


def instantiate_class_from_module(
    module_name: str,
    class_name: str,
    module_alias: str = "",
):
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    alias = f"{module_alias}." if module_alias != "" else ""

    return instantiate_tree(cls, alias=alias)
