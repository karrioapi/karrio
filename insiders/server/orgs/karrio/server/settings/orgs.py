from karrio.server.settings.base import *


KARRIO_URLS += ["karrio.server.orgs.urls"]

INSTALLED_APPS += [
    "django_extensions",
    "karrio.server.orgs",
]

KARRIO_ENTITY_ACCESS_METHOD = "karrio.server.orgs.middleware.OrganizationAccess"

ORGS_SLUGFIELD = "django_extensions.db.fields.AutoSlugField"
INVITATION_BACKEND = "karrio.server.orgs.backends.KarrioInvitationsBackend"
REGISTRATION_BACKEND = "karrio.server.orgs.backends.KarrioRegistrationBackend"


def org_user_verified_callback(user):
    import karrio.server.orgs.models as orgs
    from karrio.server.conf import settings

    if settings.ALLOW_ADMIN_APPROVED_SIGNUP == False:
        org = orgs.Organization.objects.filter(users__id=user.id).first()
        org.is_active = True
        user.is_active = True

        org.save()
        user.save()


EMAIL_VERIFIED_CALLBACK = org_user_verified_callback
