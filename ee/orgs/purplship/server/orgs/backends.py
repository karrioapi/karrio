from django.contrib.auth import get_user_model
from organizations.backends.defaults import InvitationBackend, RegistrationBackend

from purplship.server.user.views import SignUpForm
from purplship.server.orgs.models import Organization


class PurplshipInvitationsBackend(InvitationBackend):

    def __init__(self, org_model=None, namespace=None):
        self.user_model = get_user_model()
        self.org_model = org_model or Organization
        self.namespace = namespace

    def invite_by_email(self, email, sender=None, request=None, **kwargs):
        try:
            user = self.user_model.objects.get(email=email)
        except self.user_model.DoesNotExist:
            user = self.user_model.objects.create(
                email=email,
                password=self.user_model.objects.make_random_password()
            )
            user.is_active = False
            user.save()
        self.send_invitation(user, sender, **kwargs)
        return user


class PurplshipRegistrationBackend(RegistrationBackend):
    form_class = SignUpForm
