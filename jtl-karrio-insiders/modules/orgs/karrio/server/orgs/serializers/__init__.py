import karrio.lib as lib
from karrio.server.serializers import *


class UserRole(lib.StrEnum):
    member = "member"
    developer = "developer"
    admin = "admin"


USER_ROLES = [(c.name, c.name) for c in list(UserRole)]
