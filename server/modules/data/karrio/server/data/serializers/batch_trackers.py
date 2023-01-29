from django.db import transaction

import karrio.lib as lib
import karrio.server.conf as conf
import karrio.server.core.utils as utils
import karrio.server.core.gateway as gateway
import karrio.server.core.exceptions as exceptions
import karrio.server.serializers as serializers
import karrio.server.manager.models as models
import karrio.server.manager.serializers as manager
import karrio.server.data.serializers.base as base


@serializers.owned_model_serializer
class BatchTrackerData(serializers.Serializer):
    trackers = manager.TrackingData(
        many=True,
        allow_empty=False,
        help_text="The list of tracking info to process.",
    )

    @transaction.atomic
    def create(self, validated_data: dict, context: serializers.Context, **kwargs):
        import karrio.server.events.tasks as tasks
        import karrio.server.data.serializers.batch as batch

        operation_data = dict(resource_type="trackers", test_mode=context.test_mode)
        operation = (
            batch.BatchOperationModelSerializer
            .map(data=operation_data, context=context)
            .save()
            .instance
        )

        sid = transaction.savepoint()
        resources = BatchTrackerData.save_resources(
            context=context,
            data=validated_data,
            batch_id=operation.id,
            format_errors=False,
        )
        errors = [r['errors'] for r in resources if r.get('errors') is not None]
        transaction.savepoint_rollback(sid)

        if any(errors):
            raise exceptions.APIExceptions(errors, code="invalid_data")

        tasks.save_batch_resources(
            operation.id,
            data=validated_data,
            schema=conf.settings.schema,
            ctx=dict(
                test_mode=context.test_mode,
                org_id=getattr(context.org, "id", None),
                user_id=getattr(context.user, "id", None),
            ),
        )

        return operation

    @staticmethod
    def save_resources(data: dict, batch_id: str, context: serializers.Context, format_errors: bool = True):
        meta = dict(batch_id=batch_id)
        trackers_data = data['trackers']
        carrier_names = set([t['carrier_name'] for t in trackers_data])
        carriers = {
            carrier_name: utils.failsafe(lambda: gateway.Carriers.first(
                context=context,
                capability='tracking',
                carrier_name=carrier_name,
                raise_not_found=False,
            ))
            for carrier_name in carrier_names
        }
        resources = []
        trackers = []

        for index, tracker_data in enumerate(trackers_data):
            try:
                carrier_name = tracker_data['carrier_name']
                carrier = carriers[carrier_name]

                if carrier is None:
                    raise exceptions.APIException(
                        f"No carrier connection found for '{tracker_data['carrier_name']}'",
                        code="invalid_carrier",
                    )

                _tracker = (
                    models.Tracking.access_by(context)
                    .filter(tracking_number=tracker_data["tracking_number"])
                    .first()
                )
                _exists = getattr(_tracker, "carrier_name", None) == carrier_name
                tracker = (
                    _tracker if _exists
                    else models.Tracking(
                        meta=meta,
                        status="unknown",
                        test_mode=context.test_mode,
                        created_by_id=context.user.id,
                        tracking_carrier_id=carrier.id,
                        tracking_number=tracker_data["tracking_number"],
                        events = utils.default_tracking_event(
                            description="Awaiting update from carrier...",
                            code="UNKNOWN",
                        ),
                    )
                )

                if _exists is False:
                    trackers.append(tracker)

                resources.append(dict(
                    id=tracker.id,
                    status=(base.ResourceStatus.processed.value
                        if _exists else base.ResourceStatus.queued.value)
                ))
            except Exception as e:
                setattr(e, "index", index)
                resources.append(dict(
                    id=index,
                    status=base.ResourceStatus.has_errors.value,
                    errors=(lib.to_dict(e) if format_errors else e),
                ))

        if any(trackers):
            models.Tracking.objects.bulk_create(trackers)
            serializers.bulk_link_org(trackers, context)

        return resources
