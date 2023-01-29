import enum
from karrio.server.serializers import *


class UserRole(enum.Enum):
    member = "member"
    developer= "developer"
    admin = "admin"


USER_ROLES = [(c.name, c.name) for c in list(UserRole)]
