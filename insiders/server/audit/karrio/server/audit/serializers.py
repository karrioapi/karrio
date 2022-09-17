import enum


class LogEntryAction(enum.Enum):
    create = "create"
    update = "update"
    delete = "delete"
