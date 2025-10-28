import typing
import requests
from datetime import datetime
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import get_user_model

from karrio.core import utils
from karrio.server.core.utils import identity
from karrio.server.core.logging import logger
from karrio.server.serializers import Context
from karrio.server.events import models
import karrio.server.events.serializers.event as serializers
NotificationResponse = typing.Tuple[str, requests.Response]
User = get_user_model()


def notify_webhook_subscribers(
    event: str,
    data: dict,
    event_at: datetime,
    ctx: dict,
    **kwargs,
):
    logger.info("Starting webhook subscribers notification", event=event)
    context = retrieve_context(ctx)
    query = (
        (Q(enabled_events__icontains=event) | Q(enabled_events__icontains="all")),
        (Q(disabled__isnull=True) | Q(disabled=False)),
    )

    webhooks = models.Webhook.access_by(context).filter(*query)
    serializers.EventSerializer.map(
        data=dict(
            type=event,
            data=data,
            test_mode=context.test_mode,
            pending_webhooks=webhooks.count(),
        ),
        context=context,
    ).save()

    if any(webhooks):
        payload = dict(event=event, data=data)
        responses: typing.List[NotificationResponse] = notify_subscribers(
            webhooks, payload
        )
        update_notified_webhooks(webhooks, responses, event_at)
    else:
        logger.info("No webhook subscribers found", event=event)

    logger.info("Finished webhook subscribers notification", event=event)


def notify_subscribers(webhooks: typing.List[models.Webhook], payload: dict):
    def notify_subscriber(webhook: models.Webhook):
        response = identity(
            lambda: requests.post(
                webhook.url,
                json=payload,
                headers={
                    "Content-type": "application/json",
                    "X-Event-Id": webhook.secret,
                },
            )
        )

        return webhook.id, response

    return utils.exec_async(notify_subscriber, webhooks)


def update_notified_webhooks(
    webhooks: typing.List[models.Webhook],
    responses: typing.List[NotificationResponse],
    event_at: datetime,
):
    logger.info("Saving updated webhooks")

    for webhook_id, response in responses:
        try:
            logger.debug("Updating webhook", webhook_id=webhook_id)

            webhook = next((w for w in webhooks if w.id == webhook_id))
            if response.ok:
                webhook.last_event_at = event_at
                webhook.failure_streak_count = 0
            else:
                webhook.failure_streak_count += 1
                # Disable the webhook if notification failed more than 5 times
                webhook.disabled = webhook.failure_streak_count > 5

            webhook.save()

            logger.debug("Webhook updated successfully", webhook_id=webhook_id)

        except Exception as update_error:
            logger.warning("Failed to update webhook", webhook_id=webhook_id, error=str(update_error))
            logger.exception("Webhook update error", webhook_id=webhook_id)


def retrieve_context(info: dict) -> Context:
    org = None

    if settings.MULTI_ORGANIZATIONS and "org_id" in info:
        import karrio.server.orgs.models as orgs_models

        org = orgs_models.Organization.objects.filter(id=info["org_id"]).first()

    return Context(
        org=org,
        user=User.objects.filter(id=info["user_id"]).first(),
        test_mode=info.get("test_mode"),
    )
