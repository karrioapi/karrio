from purplship.server.settings.base import *


PURPLSHIP_URLS += ['purplship.server.orgs.urls']

INSTALLED_APPS += [
    'django_extensions',
    'purplship.server.orgs',
]

PURPLSHIP_ENTITY_ACCESS_METHOD = 'purplship.server.orgs.middleware.OrganizationAccess'

ORGS_SLUGFIELD = 'django_extensions.db.fields.AutoSlugField'
INVITATION_BACKEND = 'purplship.server.orgs.backends.PurplshipInvitationsBackend'
REGISTRATION_BACKEND = 'purplship.server.orgs.backends.PurplshipRegistrationBackend'


def org_user_verified_callback(user):
    import purplship.server.orgs.models as orgs

    org = orgs.Organization.objects.filter(users__id=user.id).first()
    org.is_active = True
    user.is_active = True

    org.save()
    user.save()

EMAIL_VERIFIED_CALLBACK = org_user_verified_callback
