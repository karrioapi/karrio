"""
Purplship Mailer module helper
"""
import smtplib
from typing import List
from email.message import EmailMessage


def email(from_address: str, to_addresses: List[str], subject: str, content: str, smtp_config: dict) -> dict:
    msg = EmailMessage()
    msg.set_content(content)

    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = ', '.join(to_addresses)

    with smtplib.SMTP(**smtp_config) as protocol:
        protocol.send_message(msg)

    return dict(success=True)
