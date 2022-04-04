"""karrio.server URL Configuration

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
from django.contrib.auth.models import Group
from django.conf import settings
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from constance.admin import Config


BASE_PATH = getattr(settings, "BASE_PATH", "")

admin.site.site_header = "Administration"
admin.site.index_title = "Administration"
admin.site.site_url = f"/{BASE_PATH}"
admin.site.index_template = "karrio/admin.html"
admin.site.unregister(Group)

if getattr(settings, "MULTI_TENANTS", False):
    admin.site.unregister([Config])

admin.autodiscover()

urlpatterns = [
    path(
        BASE_PATH,
        include(
            [
                path("", include("karrio.server.core.views.schema")),
                *[
                    path(subpath, include(urls, namespace=namespace))
                    for (subpath, urls, namespace) in settings.NAMESPACED_URLS
                ],
                path("", include("karrio.server.urls.jwt")),
                path("", include("karrio.server.user.urls")),
                *[path("", include(urls)) for urls in settings.KARRIO_URLS],
                path("admin/", admin.site.urls, name="app_admin"),
                *staticfiles_urlpatterns(),
            ]
        ),
        name="karrio:index",
    ),
]
