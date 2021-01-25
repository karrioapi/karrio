"""purpleserver URL Configuration

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

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


admin.site.site_header = "Purplship"
admin.site.site_title = "Purplphip shipping API"
admin.site.index_title = "Administration"

schema_view = get_schema_view(
   openapi.Info(
      title="Purplship Open Source Multi-carrier Shipping API",
      default_version=f'v1-{settings.VERSION}',
      description=("""
      Purplship is an open source multi-carrier shipping API that simplifies the integration of logistic carrier services

      The **proxy** endpoints are stateless and forwards calls to carriers web services.
      """),
      contact=openapi.Contact(email="hello@purplship.com"),
      license=openapi.License(name="AGPLv3+ License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path(settings.OPEN_API_PATH, schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    path('admin/', admin.site.urls, name='app_admin'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    *[path('', include(urls)) for urls in settings.PURPLSHIP_URLS],
]

urlpatterns += staticfiles_urlpatterns()

