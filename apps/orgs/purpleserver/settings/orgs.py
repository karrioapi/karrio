from purpleserver.settings.base import (
    INSTALLED_APPS,
    PURPLSHIP_URLS
)

PURPLSHIP_URLS += ['purpleserver.orgs.urls']

INSTALLED_APPS = [
    *INSTALLED_APPS,

    'django_extensions',
    'organizations',

    'purpleserver.orgs',
]


PURPLSHIP_ENTITY_ACCESS_METHOD = 'purpleserver.orgs.middleware.OrganizationAccess'

# ORGS_SLUGFIELD = 'django_extensions.db.fields.AutoSlugField'

# INVITATION_BACKEND = 'myapp.backends.MyInvitationBackend'
