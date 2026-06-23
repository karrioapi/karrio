from decouple import config

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="admin@example.com")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_FROM_ADDRESS = config("EMAIL_FROM_ADDRESS", default="noreply@example.com")

# django-otp's email plugin reads `settings.OTP_EMAIL_SENDER` for the From
# header, NOT `EMAIL_FROM_ADDRESS`. Without this, OTP challenge emails go out
# as `webmaster@localhost` (Django's DEFAULT_FROM_EMAIL fallback) and get
# rejected by strict SMTP relays (e.g. SendGrid 550 — sender not verified).
# This holds the import-time value; the constance signal handler in
# `karrio.server.core.signals.update_settings` keeps it in sync with
# `EMAIL_FROM_ADDRESS` whenever an admin updates the Email Config page.
OTP_EMAIL_SENDER = config("OTP_EMAIL_SENDER", default="") or EMAIL_FROM_ADDRESS

EMAIL_SERVER = EMAIL_HOST
EMAIL_ADDRESS = EMAIL_HOST_USER
EMAIL_PASSWORD = EMAIL_HOST_PASSWORD

EMAIL_ACTIVE_FIELD = "is_active"
EMAIL_MAIL_SUBJECT = "Verify Your New Account Email"
EMAIL_MAIL_HTML = "registration/registration_confirm_email.html"
EMAIL_MAIL_PLAIN = "registration/registration_confirm_email.txt"
EMAIL_PAGE_TEMPLATE = "registration/registration_confirm_done.html"

EMAIL_TOKEN_LIFE = 60 * 60
EMAIL_ENABLED = False


def user_verified_callback(user):
    from karrio.server.conf import settings

    if not settings.ALLOW_ADMIN_APPROVED_SIGNUP:
        user.is_active = True
        user.save()


EMAIL_VERIFIED_CALLBACK = user_verified_callback

# Compatibility with django-email-verification expected settings
# Some versions expect EMAIL_MAIL_CALLBACK to be present.
# Reuse the same verified callback to activate the user when appropriate.
EMAIL_MAIL_CALLBACK = user_verified_callback
