# This module previously contained permission group setup logic.
# The setup_groups() function has been removed to:
# 1. Fix Django warning about database access during app initialization
# 2. Prepare for a better RBAC implementation in the future
#
# The PermissionGroup enum and ROLES_GROUPS mapping are preserved in
# karrio.server.iam.serializers for organization role management.
