from typing import Type


def validate_and_save(serializer_type: Type, data, instance=None, **kwargs):
    if data is None:
        return None

    serializer = serializer_type(data=data) if instance is None else serializer_type(instance, data=data, partial=True)

    # We are not raising an exception nor checking the validation result because it was already done.
    serializer.is_valid(raise_exception=True)
    return serializer.save(**kwargs)
