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


def org_user_verified_callback(user):
    import purpleserver.orgs.models as orgs

    org = orgs.Organization.objects.filter(users__id=user.id).first()
    org.is_active = True
    user.is_active = True

    org.save()
    user.save()

EMAIL_VERIFIED_CALLBACK = org_user_verified_callback
