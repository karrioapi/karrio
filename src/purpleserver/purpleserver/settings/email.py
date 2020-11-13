from decouple import config


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default=None)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default=None)
EMAIL_HOST = config('EMAIL_HOST', default=None)
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)

EMAIL_ACTIVE_FIELD = 'is_active'
EMAIL_SERVER = EMAIL_HOST
EMAIL_ADDRESS = EMAIL_HOST_USER
EMAIL_FROM_ADDRESS = config('EMAIL_FROM_ADDRESS', default='noreply@purplship.com')
EMAIL_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_MAIL_SUBJECT = 'Purplship - Verify Your New Account Email'
EMAIL_MAIL_HTML = 'registration/registration_confirm_email.html'
EMAIL_PAGE_TEMPLATE = 'registration/registration_confirm_done.html'
EMAIL_PAGE_DOMAIN = config('DOMAIN', default='http://127.0.0.1:8000/')
