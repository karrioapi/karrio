from purpleserver.settings.base import *


PURPLSHIP_URLS += ['purpleserver.orgs.urls']

INSTALLED_APPS += [
    'django_extensions',
    'purpleserver.orgs',
]

PURPLSHIP_ENTITY_ACCESS_METHOD = 'purpleserver.orgs.middleware.OrganizationAccess'

ORGS_SLUGFIELD = 'django_extensions.db.fields.AutoSlugField'
INVITATION_BACKEND = 'purpleserver.orgs.backends.PurplshipInvitationsBackend'
REGISTRATION_BACKEND = 'purpleserver.orgs.backends.PurplshipRegistrationBackend'
