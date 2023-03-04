import datetime
from django.urls import reverse
from django.contrib import admin
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from rest_framework_tracking.admin import APIRequestLog

from karrio.server.tracing import models


class TracingRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "log", "key", "test_mode", "request_timestamp", "created_at")
    search_fields = ("meta__request_log_id", "meta__carrier_name")
    list_filter = ("key", "test_mode")
    readonly_fields = [
        f.name
        for f in models.TracingRecord._meta.get_fields()
        if f.name not in ["org", "link"]
    ]

    def get_queryset(self, request):
        if settings.MULTI_ORGANIZATIONS:
            return (
                models.TracingRecord.objects
                .all()
                .filter(link__org__users__id=request.user.id)
                .order_by("-timestamp")
            )

        return super().get_queryset(request).order_by("-timestamp")

    def has_add_permission(self, request) -> bool:
        return False

    def log(self, obj):
        log_id = obj.meta.get("request_log_id")

        if any(str(log_id)):
            return mark_safe(
                '<a href="{}">{}</a>'.format(
                    reverse(
                        f"admin:{APIRequestLog._meta.app_label}_{APIRequestLog._meta.model_name}_change",
                        args=(log_id,),
                    ),
                    log_id,
                )
            )

        return ""

    def request_timestamp(self, obj):
        timestamp = datetime.datetime.fromtimestamp(obj.timestamp)

        if timestamp:
            return timestamp.strftime("%Y-%m-%d %H:%M:%S")

        return ""

    request_timestamp.admin_order_field = "timestamp"


admin.site.register(models.TracingRecord, TracingRecordAdmin)
