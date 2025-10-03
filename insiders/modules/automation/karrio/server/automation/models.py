import functools
import django.conf as conf
import django.utils.text as text
import django.db.models as models
import django.utils.translation as translation

import karrio.server.core.models as core
import karrio.server.automation.serializers as automation_serializers

_ = translation.gettext_lazy


class WorkflowManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


@core.register_model
class Workflow(core.OwnedEntity):
    objects = WorkflowManager()

    class Meta:
        db_table = "workflow"
        verbose_name = "Workflow"
        verbose_name_plural = "Workflows"
        ordering = ["-created_at"]

    def natural_key(self):
        return (self.slug,)

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="wkfl_"),
        editable=False,
    )
    name = models.CharField(_("name"), max_length=50)
    slug = models.CharField(_("slug"), max_length=100, db_index=True)
    is_public = models.BooleanField(null=False, default=False)
    is_active = models.BooleanField(null=False, default=False)
    description = models.CharField(max_length=150, null=True, blank=True)
    action_nodes = models.JSONField(
        blank=True, null=True, default=core.field_default([])
    )
    metadata = models.JSONField(blank=True, null=True, default=core.field_default({}))

    # Related fields
    created_by = models.ForeignKey(
        conf.settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )
    template = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clones",
    )

    # Compute fields
    @property
    def object_type(self):
        return "workflow"

    @property
    def trigger(self):
        if hasattr(self, "workflow_trigger"):
            return self.workflow_trigger

        return None

    @property
    def actions(self):
        _slugs = [_.get("slug") for _ in self.action_nodes]
        return WorkflowAction.objects.filter(slug__in=_slugs)

    @property
    def template_slug(self):
        if self.template:
            return self.template.slug

        return None


class WorkflowConnectionManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


@core.register_model
class WorkflowConnection(core.OwnedEntity):
    objects = WorkflowConnectionManager()

    class Meta:
        db_table = "workflow-connection"
        verbose_name = "Workflow Connection"
        verbose_name_plural = "Workflow Connections"
        ordering = ["-created_at"]

    def natural_key(self):
        return (self.slug,)

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="wcon_"),
        editable=False,
    )
    name = models.CharField(_("name"), max_length=50)
    slug = models.CharField(_("slug"), max_length=100, db_index=True)
    is_public = models.BooleanField(null=False, default=core.field_default(False))
    description = models.CharField(max_length=150, null=True, blank=True)
    credentials = models.JSONField(
        blank=True, null=True, default=core.field_default({})
    )
    auth_type = models.CharField(
        max_length=50,
        choices=automation_serializers.AUTH_TYPE,
        default=automation_serializers.AUTH_TYPE[0][0],
        db_index=True,
    )
    port = models.TextField(max_length=20, null=True, blank=True)
    host = models.TextField(max_length=None, null=True, blank=True)
    endpoint = models.TextField(max_length=None, null=True, blank=True)
    parameters_template = models.TextField(max_length=None, null=True, blank=True)
    auth_template = models.TextField(max_length=None, null=True, blank=True)
    metadata = models.JSONField(blank=True, null=True, default=core.field_default({}))

    # Related fields
    created_by = models.ForeignKey(
        conf.settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )
    template = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clones",
    )
    metafields = models.ManyToManyField(
        core.Metafield,
        related_name="metafield_connection",
        through="WorkflowConnectionMetafieldLink",
    )

    # Compute fields
    @property
    def object_type(self):
        return "workflow-connection"

    @property
    def template_slug(self):
        if self.template:
            return self.template.slug

        return None

    @property
    def alias(self):
        return text.slugify(self.name).replace("-", "_")

    @property
    def metafields_object(self) -> dict:
        return core.metafields_to_dict(self.metafields.all())

    @property
    def credentials_from_metafields(self) -> dict:
        """Get credentials from metafields, replacing the credentials JSONField"""
        return self.metafields_object

    @property
    def required_credentials(self) -> list:
        """Get list of required credential metafields that need to be filled"""
        return list(
            self.metafields.filter(is_required=True, value__isnull=True)
            .values_list('key', flat=True)
        )

    @property
    def is_credentials_complete(self) -> bool:
        """Check if all required credential metafields are provided"""
        return len(self.required_credentials) == 0

    def validate_credentials(self) -> dict:
        """Validate that all required credentials are provided"""
        missing = self.required_credentials
        if missing:
            return {
                'valid': False,
                'missing_fields': missing,
                'message': f"Missing required credentials: {', '.join(missing)}"
            }
        return {'valid': True, 'message': 'All required credentials provided'}


class WorkflowActionManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


@core.register_model
class WorkflowAction(core.OwnedEntity):
    objects = WorkflowActionManager()

    class Meta:
        db_table = "workflow-action"
        verbose_name = "Workflow Action"
        verbose_name_plural = "Workflow Actions"
        ordering = ["-created_at"]

    def natural_key(self):
        return (self.slug,)

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="wact_"),
        editable=False,
    )
    name = models.CharField(_("name"), max_length=50)
    slug = models.CharField(_("slug"), max_length=100, db_index=True)
    is_public = models.BooleanField(null=False, default=core.field_default(False))
    description = models.CharField(max_length=150, null=True, blank=True)
    action_type = models.CharField(
        max_length=50,
        choices=automation_serializers.ACTION_TYPE,
        default=automation_serializers.ACTION_TYPE[0][0],
        db_index=True,
    )
    port = models.PositiveIntegerField(null=True, blank=True)
    host = models.TextField(max_length=None, null=True, blank=True)
    endpoint = models.TextField(max_length=None, null=True, blank=True)
    method = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        choices=automation_serializers.HTTP_METHOD,
    )
    parameters_type = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=automation_serializers.PARAMETERS_TYPE,
    )
    content_type = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        choices=automation_serializers.HTTP_CONTENT_TYPE,
    )
    parameters_template = models.TextField(max_length=None, null=True, blank=True)
    header_template = models.TextField(max_length=None, null=True, blank=True)
    metadata = models.JSONField(blank=True, null=True, default=core.field_default({}))

    # Related fields
    created_by = models.ForeignKey(
        conf.settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )
    template = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clones",
    )
    connection = models.ForeignKey(
        "WorkflowConnection",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="connection_actions",
    )
    metafields = models.ManyToManyField(
        core.Metafield,
        related_name="metafield_action",
        through="WorkflowActionMetafieldLink",
    )

    # Compute fields
    @property
    def object_type(self):
        return "workflow-action"

    @property
    def template_slug(self):
        if self.template:
            return self.template.slug

        return None

    @property
    def alias(self):
        return text.slugify(self.name).replace("-", "_")

    @property
    def metafields_object(self) -> dict:
        return core.metafields_to_dict(self.metafields.all())


@core.register_model
class WorkflowEvent(core.OwnedEntity):
    class Meta:
        db_table = "workflow-event"
        verbose_name = "Workflow Event"
        verbose_name_plural = "Workflow Events"
        ordering = ["-created_at"]

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="wevt_"),
        editable=False,
    )
    status = models.CharField(
        max_length=50,
        choices=automation_serializers.WORKFLOW_EVENT_STATUS,
        default=automation_serializers.WORKFLOW_EVENT_STATUS[0][0],
        db_index=True,
    )
    event_type = models.CharField(
        max_length=50,
        choices=automation_serializers.WORKFLOW_EVENT_TYPE,
        default=automation_serializers.WORKFLOW_EVENT_TYPE[0][0],
        db_index=True,
    )
    test_mode = models.BooleanField(null=False, default=False)
    parameters = models.JSONField(blank=True, null=True, default=core.field_default({}))

    # Related fields
    created_by = models.ForeignKey(
        conf.settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )
    workflow = models.ForeignKey(
        "Workflow",
        on_delete=models.CASCADE,
        related_name="workflow_events",
    )

    # Compute fields
    @property
    def object_type(self):
        return "workflow-event"


class WorkflowTriggerManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)
    
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("workflow", "created_by")
        )


@core.register_model
class WorkflowTrigger(core.OwnedEntity):
    objects = WorkflowTriggerManager()

    class Meta:
        db_table = "workflow-trigger"
        verbose_name = "Workflow Trigger"
        verbose_name_plural = "Workflow Triggers"
        ordering = ["-created_at"]

    def natural_key(self):
        return (self.slug,)

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="wtrg_"),
        editable=False,
    )
    slug = models.CharField(_("slug"), max_length=100, db_index=True)
    name = models.CharField(_("name"), null=True, max_length=50)
    trigger_type = models.CharField(
        max_length=50,
        choices=automation_serializers.WORKFLOW_TRIGGER_TYPE,
        default=automation_serializers.WORKFLOW_TRIGGER_TYPE[0][0],
        db_index=True,
    )
    schedule = models.TextField(max_length=None, null=True, blank=True)
    secret = models.CharField(max_length=100, null=True, blank=True)
    secret_key = models.CharField(max_length=100, null=True, blank=True)

    # Scheduled workflow fields
    next_run_at = models.DateTimeField(null=True, blank=True, help_text="Next scheduled execution time")
    last_run_at = models.DateTimeField(null=True, blank=True, help_text="Last execution time")

    # Related fields
    created_by = models.ForeignKey(
        conf.settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )
    template = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clones",
    )
    workflow = models.OneToOneField(
        "Workflow",
        on_delete=models.CASCADE,
        related_name="workflow_trigger",
    )

    # Compute fields
    @property
    def object_type(self):
        return "workflow-trigger"

    @property
    def template_slug(self):
        if self.template:
            return self.template.slug

        return None

    @property
    def is_due(self):
        """Check if this scheduled workflow is due for execution"""
        if self.trigger_type != automation_serializers.AutomationTriggerType.scheduled.value:
            return False
        if not self.next_run_at:
            return False

        from django.utils import timezone
        return self.next_run_at <= timezone.now()

    def clean(self):
        """Validate the workflow trigger"""
        super().clean()

        # Validate cron expression for scheduled triggers
        if self.trigger_type == automation_serializers.AutomationTriggerType.scheduled.value:
            if not self.schedule:
                from django.core.exceptions import ValidationError
                raise ValidationError("Schedule is required for scheduled triggers")

            try:
                from karrio.server.automation.cron_utils import validate_cron_expression
                validate_cron_expression(self.schedule)
            except Exception as e:
                from django.core.exceptions import ValidationError
                raise ValidationError(f"Invalid cron expression: {e}")

    def update_next_run(self):
        """Calculate and update next_run_at based on cron schedule"""
        if self.trigger_type == automation_serializers.AutomationTriggerType.scheduled.value and self.schedule:
            try:
                from karrio.server.automation.cron_utils import calculate_next_run_time
                self.next_run_at = calculate_next_run_time(self.schedule)
                self.save(update_fields=['next_run_at'])
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Failed to calculate next run time for trigger {self.id}: {e}")

    def save(self, *args, **kwargs):
        """Override save to calculate next_run_at for new scheduled triggers"""
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Calculate next run time for new scheduled triggers
        if (is_new and
            self.trigger_type == automation_serializers.AutomationTriggerType.scheduled.value and
            self.schedule and
            not self.next_run_at):
            self.update_next_run()


class ShippingRuleManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


@core.register_model
class ShippingRule(core.OwnedEntity):
    objects = ShippingRuleManager()

    class Meta:
        db_table = "shipping-rule"
        verbose_name = "Shipping Rule"
        verbose_name_plural = "Shipping Rules"
        ordering = ["priority", "-created_at"]

    def natural_key(self):
        return (self.slug,)

    id = models.CharField(
        max_length=50,
        primary_key=True,
        default=functools.partial(core.uuid, prefix="shrl_"),
        editable=False,
    )
    name = models.CharField(_("name"), max_length=100)
    slug = models.CharField(_("slug"), max_length=100, db_index=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)
    conditions = models.JSONField(blank=True, null=True, default=core.field_default({}))
    actions = models.JSONField(blank=True, null=True, default=core.field_default({}))
    metadata = models.JSONField(blank=True, null=True, default=core.field_default({}))

    # Related fields
    created_by = models.ForeignKey(
        conf.settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )

    # Compute fields
    @property
    def object_type(self):
        return "shipping-rule"


"""Models automation linking (for reverse OneToMany relations)"""


class WorkflowConnectionMetafieldLink(models.Model):
    connection = models.ForeignKey(
        WorkflowConnection, on_delete=models.CASCADE, related_name="metafields_links"
    )
    metafield = models.OneToOneField(
        core.Metafield, on_delete=models.CASCADE, related_name="connection_link"
    )


class WorkflowActionMetafieldLink(models.Model):
    action = models.ForeignKey(
        WorkflowAction, on_delete=models.CASCADE, related_name="metafields_links"
    )
    metafield = models.OneToOneField(
        core.Metafield, on_delete=models.CASCADE, related_name="action_link"
    )
