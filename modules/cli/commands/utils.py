import pydoc
import karrio.lib as lib


class CarrierFeatures(lib.StrEnum):
    tracking = "tracking"
    rating = "rating"
    shipping = "shipping"
    pickup = "pickup"
    address = "address"
    upload = "upload"
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
