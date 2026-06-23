"""
MFA (TOTP) enrollment REST API.

Login + OTP-challenge already exists at /api/token + /api/token/verified
(see urls/jwt.py). This module only exposes the *enrollment* lifecycle so
non-Django-admin clients (e.g. the JTL admin dashboard) can let staff add /
confirm / remove a TOTP device without going through Django admin.

Only TOTP is exposed here. Email-based MFA (django_otp.plugins.otp_email)
isn't surfaced on these endpoints by design — the JTL admin flow uses
authenticator apps. The tenant /graphql schema has separate EmailDevice
mutations for end-customer apps that need email MFA; this REST surface
does not.

Endpoints
---------
  POST /api/mfa/totp/init      Get-or-create unconfirmed TOTPDevice; returns
                               provisioning_uri + secret for QR rendering.
  POST /api/mfa/totp/confirm   Verify OTP token, mark device confirmed.
  POST /api/mfa/totp/disable   Delete the user's TOTP device(s).
  GET  /api/mfa/status         Whether the current user has TOTP enrolled.

Authentication
--------------
Restricted to JWT (cookie or bearer). Token / Basic / OAuth2 are intentionally
excluded — those credential types don't represent an interactive session and
shouldn't be used to enroll or revoke a second factor.
"""

import base64

import karrio.server.openapi as openapi
from django.utils.translation import gettext_lazy as _
from django_otp.plugins.otp_totp.models import TOTPDevice
from karrio.server.core.authentication import JWTAuthentication
from rest_framework import exceptions, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

ENDPOINT_ID = "##"  # Per-file unique prefix for operation_id (matches jwt.py "&&", tokens.py etc.)


# --- Response / request serializers (for OpenAPI) ---


class TOTPInitResponse(serializers.Serializer):
    provisioning_uri = serializers.CharField(
        help_text="otpauth:// URI for QR code rendering or 'Scan with authenticator app' deep link.",
    )
    secret = serializers.CharField(
        help_text="Base32-encoded shared secret for manual entry into an authenticator app.",
    )


class TOTPConfirmInput(serializers.Serializer):
    otp_token = serializers.CharField(
        required=True,
        min_length=6,
        max_length=8,
        help_text="The 6-digit (or 8-digit) code currently displayed by the authenticator app.",
    )


class TOTPDisableInput(serializers.Serializer):
    otp_token = serializers.CharField(
        required=True,
        min_length=6,
        max_length=8,
        help_text=(
            "Fresh OTP code from the authenticator app. Required to disable MFA — "
            "an OTP-verified session alone is not sufficient (step-up auth)."
        ),
    )


class MFAStatusResponse(serializers.Serializer):
    enrolled = serializers.BooleanField(help_text="True if any TOTPDevice exists for the user (confirmed or not).")
    confirmed = serializers.BooleanField(help_text="True if a confirmed TOTPDevice exists.")


class SimpleResultResponse(serializers.Serializer):
    confirmed = serializers.BooleanField(required=False)
    disabled = serializers.BooleanField(required=False)


# --- Views ---


class _BaseMFAView(APIView):
    """Cookie/JWT auth only — see module docstring rationale."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class TOTPInitView(_BaseMFAView):
    @openapi.extend_schema(
        tags=["Auth"],
        operation_id=f"{ENDPOINT_ID}init_totp",
        summary="Begin TOTP enrollment",
        description=(
            "Create (or fetch) an unconfirmed TOTP device for the current user and return "
            "its provisioning URI. The client renders this URI as a QR code; the user scans "
            "it with an authenticator app and submits the first generated code to "
            "`/api/mfa/totp/confirm` to complete enrollment."
        ),
        request=None,
        responses={200: TOTPInitResponse()},
    )
    def post(self, request):
        user = request.user

        # Refuse re-enrollment if there is already a confirmed device — the
        # caller must explicitly disable first. This stops a malicious /init
        # call from silently rotating someone's TOTP secret.
        if TOTPDevice.objects.filter(user=user, confirmed=True).exists():
            raise exceptions.ValidationError(
                _("TOTP is already enrolled. Disable it before re-enrolling."),
                code="totp_already_enrolled",
            )

        # `get_or_create` would raise MultipleObjectsReturned if a race or an
        # aborted prior enrollment left more than one unconfirmed device for
        # this user. Pick the oldest existing one (so retries return the same
        # secret) and prune the rest so future init calls stay clean.
        unconfirmed = TOTPDevice.objects.filter(user=user, confirmed=False).order_by("pk")
        device = unconfirmed.first()
        if device is None:
            device = TOTPDevice.objects.create(user=user, name="default", confirmed=False)
        else:
            unconfirmed.exclude(pk=device.pk).delete()

        return Response(
            {
                "provisioning_uri": device.config_url,
                "secret": base64.b32encode(device.bin_key).decode("ascii"),
            },
            status=status.HTTP_200_OK,
        )


class TOTPConfirmView(_BaseMFAView):
    @openapi.extend_schema(
        tags=["Auth"],
        operation_id=f"{ENDPOINT_ID}confirm_totp",
        summary="Confirm TOTP enrollment",
        description=(
            "Submit the 6-digit code currently shown by the authenticator app. If valid, "
            "the device is marked `confirmed=True` and the user is enrolled."
        ),
        request=TOTPConfirmInput,
        responses={200: SimpleResultResponse()},
    )
    def post(self, request):
        serializer = TOTPConfirmInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_token = serializer.validated_data["otp_token"]

        device = TOTPDevice.objects.filter(user=request.user, confirmed=False).first()
        if device is None:
            raise exceptions.ValidationError(
                _("No pending TOTP enrollment. Call /api/mfa/totp/init first."),
                code="totp_not_initialized",
            )

        if not device.verify_token(otp_token):
            raise exceptions.ValidationError(
                {"otp_token": _("Invalid or expired OTP token")},
                code="otp_invalid",
            )

        device.confirmed = True
        device.save()

        return Response({"confirmed": True}, status=status.HTTP_200_OK)


class TOTPDisableView(_BaseMFAView):
    @openapi.extend_schema(
        tags=["Auth"],
        operation_id=f"{ENDPOINT_ID}disable_totp",
        summary="Disable TOTP",
        description=(
            "Remove the user's TOTP device(s). Requires **both** an OTP-verified JWT *and* "
            "a fresh OTP code in the request body. The session-verified check happens at "
            "auth time (`JWTAuthentication.authenticate` rejects tokens with "
            "`is_verified=False`); the fresh OTP check is step-up auth — a session "
            "verified 25 minutes ago shouldn't be able to disable MFA without re-proving "
            "the second factor right now."
        ),
        request=TOTPDisableInput,
        responses={200: SimpleResultResponse()},
    )
    def post(self, request):
        # 1. JWT is_verified=False is rejected upstream in JWTAuthentication.
        # 2. Step-up: require a fresh OTP in the body — matches the pattern
        #    that /api/token/verified uses for token upgrades.
        serializer = TOTPDisableInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_token = serializer.validated_data["otp_token"]

        device = TOTPDevice.objects.filter(user=request.user, confirmed=True).first()
        if device is None:
            raise exceptions.ValidationError(
                _("No confirmed TOTP device to disable."),
                code="totp_not_enrolled",
            )

        if not device.verify_token(otp_token):
            raise exceptions.ValidationError(
                {"otp_token": _("Invalid or expired OTP token")},
                code="otp_invalid",
            )

        TOTPDevice.objects.filter(user=request.user).delete()
        return Response({"disabled": True}, status=status.HTTP_200_OK)


class MFAStatusView(_BaseMFAView):
    @openapi.extend_schema(
        tags=["Auth"],
        operation_id=f"{ENDPOINT_ID}mfa_status",
        summary="MFA status",
        description="Whether the current user has TOTP enrolled and confirmed.",
        responses={200: MFAStatusResponse()},
    )
    def get(self, request):
        qs = TOTPDevice.objects.filter(user=request.user)
        return Response(
            {
                "enrolled": qs.exists(),
                "confirmed": qs.filter(confirmed=True).exists(),
            },
            status=status.HTTP_200_OK,
        )


from django.urls import path  # noqa: E402  (kept with urlpatterns below for locality)

urlpatterns = [
    path("api/mfa/totp/init", TOTPInitView.as_view(), name="mfa-totp-init"),
    path("api/mfa/totp/confirm", TOTPConfirmView.as_view(), name="mfa-totp-confirm"),
    path("api/mfa/totp/disable", TOTPDisableView.as_view(), name="mfa-totp-disable"),
    path("api/mfa/status", MFAStatusView.as_view(), name="mfa-status"),
]
