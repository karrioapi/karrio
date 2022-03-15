from django_email_verification.token import default_token_generator
from django_email_verification.confirm import (
    Thread,
    InvalidUserModel,
    EmailMultiAlternatives,
    _get_validated_field,
    render_to_string,
)


def send_email(user, redirect_url, thread=True, **kwargs):
    try:
        user.save()

        if kwargs.get("custom_salt"):
            default_token_generator.key_salt = kwargs["custom_salt"]

        expiry_ = kwargs.get("expiry")
        token, expiry = default_token_generator.make_token(user, expiry_)

        domain = redirect_url
        sender = _get_validated_field("EMAIL_FROM_ADDRESS")
        subject = _get_validated_field("EMAIL_MAIL_SUBJECT")
        mail_plain = _get_validated_field("EMAIL_MAIL_PLAIN")
        mail_html = _get_validated_field("EMAIL_MAIL_HTML")

        args = (
            user,
            token,
            expiry,
            sender,
            domain,
            subject,
            mail_plain,
            mail_html,
        )
        if thread:
            t = Thread(target=send_email_thread, args=args)
            t.start()
        else:
            send_email_thread(*args)
    except AttributeError:
        raise InvalidUserModel("The user model you provided is invalid")


def send_email_thread(
    user, token, expiry, sender, domain, subject, mail_plain, mail_html
):
    domain += "/" if not domain.endswith("/") else ""
    link = domain + token

    context = {"link": link, "expiry": expiry, "user": user}

    text = render_to_string(mail_plain, context)
    html = render_to_string(mail_html, context)

    msg = EmailMultiAlternatives(subject, text, sender, [user.email])
    msg.attach_alternative(html, "text/html")
    msg.send()
