"""
Django app configuration for JTL Custom core module.
"""

from django.apps import AppConfig


class JTLConfig(AppConfig):
    """JTL Custom core module app configuration."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'karrio.server.jtl'
    verbose_name = 'JTL Custom core'
    label = 'jtl'
