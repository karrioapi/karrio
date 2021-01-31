from enum import Enum as BaseEnum, Flag as BaseFlag, EnumMeta


class MetaEnum(EnumMeta):

    def __contains__(cls, item):
        if item is None:
            return False
        if isinstance(item, str):
            return item in cls.__members__

        return super().__contains__(item)


class Enum(BaseEnum, metaclass=MetaEnum):
    pass


class Flag(BaseFlag, metaclass=MetaEnum):
    pass
