import typing
import requests
import logging
from datetime import datetime
from django.db.models import Q

from purplship.core import utils
from purpleserver.core.utils import identity
from purpleserver.events import models

logger = logging.getLogger(__name__)
NotificationResponse = typing.Tuple[str, requests.Response]


def notify_webhook_subscribers(event: str, data: dict, event_at: datetime, test_mode: bool = None):
    logger.info(f"> starting {event} subscribers notification")
    query = (
        (Q(enabled_events__contains=[event]) | Q(enabled_events__contains=['all'])),
        (Q(disabled__isnull=True) | Q(disabled=False))
    )

    if test_mode is not None:
        query += (Q(test_mode=test_mode),)

    webhooks = models.Webhook.objects.filter(*query)

    if any(webhooks):
        payload = dict(event=event, data=data)
        responses: typing.List[NotificationResponse] = notify_subscribers(webhooks, payload)
        update_notified_webhooks(webhooks, responses, event_at)
    else:
        logger.info("no subscribers found")

    logger.info(f"> ending {event} subscribers notification")


def notify_subscribers(webhooks: typing.List[models.Webhook], payload: dict):

    def notify_subscriber(webhook: models.Webhook):
        response = identity(lambda: requests.post(
            webhook.url,
            json=payload,
            headers={'Content-type': 'application/json'}
        ))

        return webhook.id, response

    return utils.exec_async(notify_subscriber, webhooks)


def update_notified_webhooks(webhooks: typing.List[models.Webhook], responses: typing.List[NotificationResponse], event_at: datetime):
    logger.info('> saving updated webhooks')

    for webhook_id, response in responses:
        try:
            logger.debug(f"update webhook {webhook_id}")

            webhook = next((w for w in webhooks if w.id == webhook_id))
            if response.ok:
                webhook.last_event_at = event_at
                webhook.failure_streak_count = 0
            else:
                webhook.failure_streak_count += 1
                # Disable the webhook if notification failed more than 5 times
                webhook.disabled = webhook.failure_streak_count > 5

            webhook.save()

            logger.debug(f"webhook {webhook_id} updated successfully")

        except Exception as update_error:
            logger.warning(f'failed to update webhook {webhook_id}')
            logger.error(update_error, exc_info=True)
