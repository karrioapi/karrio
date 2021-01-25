from purplship.references import collect_providers_data, collect_references

from purpleserver.core.serializers import CustomsContentType


PACKAGE_MAPPERS = collect_providers_data()

REFERENCE_MODELS = {
    **collect_references(),
    "customs_content_type": {c.name: c.value for c in list(CustomsContentType)},
}
