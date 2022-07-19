from decouple import config

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="admin@karrio.io")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)

EMAIL_PAGE_DOMAIN = config("DOMAIN", default="https://app.karrio.io")
EMAIL_FROM_ADDRESS = config("EMAIL_FROM_ADDRESS", default="noreply@karrio.io")

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

    if settings.ALLOW_ADMIN_APPROVED_SIGNUP == False:
        user.is_active = True
        user.save()


EMAIL_VERIFIED_CALLBACK = user_verified_callback
