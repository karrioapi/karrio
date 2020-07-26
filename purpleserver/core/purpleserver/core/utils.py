from typing import Type, TypeVar, Generic, Optional, Union, Callable, Any
from rest_framework.serializers import Serializer

T = TypeVar('T')


def identity(value: Union[Any, Callable]) -> T:
    """
    :param value: function or value desired to be wrapped
    :return: value or callable return
    """
    return value() if callable(value) else value


def validate_and_save(serializer_type: Type, data, instance=None, **kwargs):
    if data is None:
        return None

    serializer = serializer_type(data=data) if instance is None else serializer_type(instance, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    return serializer.save(**kwargs)


class _SerializerDecoratorInitializer(Generic[T]):

    def __getitem__(self, serializer_type: Type[Serializer]):
        class Decorator:
            def __init__(self, instance=None, data: Union[str, dict] = None):
                self._instance = instance

                if data is None and instance is None:
                    self._serializer = None

                else:
                    self._serializer: serializer_type = (
                        serializer_type(data=data) if instance is None else
                        serializer_type(instance, data=data, partial=True)
                    )

                    self._serializer.is_valid(raise_exception=True)

            @property
            def data(self) -> Optional[dict]:
                return self._serializer.validated_data if self._serializer is not None else None

            @property
            def instance(self):
                return self._instance

            def save(self, **kwargs) -> 'Decorator':
                if self._serializer is not None:
                    self._instance = self._serializer.save(**kwargs)

                return self

        return Decorator


SerializerDecorator = _SerializerDecoratorInitializer()
