"""purplship.server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


APP_VERSION = getattr(settings, "VERSION", "")
APP_NAME = getattr(settings, "APP_NAME", "Purplship")
ADMIN_PATH = "admin/" if settings.HAS_EMBEDDED_CLIENT else ""

admin.site.site_header = APP_NAME
admin.site.site_title = f"{APP_NAME} shipping API"
admin.site.index_title = "Administration"


urlpatterns = [
    path("", include("purplship.server.urls.schema")),
    path("api/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include("purplship.server.urls.jwt")),
    *[path("", include(urls)) for urls in settings.PURPLSHIP_URLS],
    path(ADMIN_PATH, admin.site.urls, name="app_admin"),
]

if settings.HAS_EMBEDDED_CLIENT:
    urlpatterns += [
        path("", include("purplship.server.user.urls")),
    ]

urlpatterns += staticfiles_urlpatterns()
