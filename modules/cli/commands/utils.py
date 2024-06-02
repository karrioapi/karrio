import importlib
import pydoc
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


def instantiate_tree(cls, indent=0):
    tree = f"{cls.__name__}(\n"
    indent += 1
    for name, typ in cls.__annotations__.items():
        if typ.__name__ == "Optional" and hasattr(typ, "__args__"):
            typ = typ.__args__[0]
        if typ.__name__ == "List" and hasattr(typ, "__args__"):
            typ = typ.__args__[0]
            tree += (
                " " * indent * 4
                + f"{name}=[\n"
                + " " * indent * 5
                + f"{instantiate_tree(typ, indent + 1)}\n"
                + " " * indent * 4
                + "],\n"
            )
        elif hasattr(typ, "__annotations__"):
            tree += " " * indent * 4 + f"{name}={instantiate_tree(typ, indent)},\n"
        else:
            tree += " " * indent * 4 + f"{name}=None,\n"
    tree += " " * (indent - 1) * 4 + ")"
    return tree


def instantiate_class_from_module(module_name: str, class_name: str):
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    return instantiate_tree(cls)
