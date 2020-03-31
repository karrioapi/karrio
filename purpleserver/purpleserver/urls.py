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
import logging
from django.contrib import admin
from django.urls import include, path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

import purpleserver.proxy.views
from purpleserver.proxy.router import router as proxy_router
from purpleserver.core.views import router as core_router

logging.getLogger('purplship').setLevel(logging.NOTSET)

admin.site.site_header = "PurplShip Board"

schema_view = get_schema_view(
   openapi.Info(
      title="PurplShip Multi-carrier API",
      default_version='v1',
      description="The Open Source Multi-carrier API",
      contact=openapi.Contact(email="support@purplship.com"),
      license=openapi.License(name="AGPLv3+ License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('dashboard/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('v1/', include(proxy_router.urls + core_router.urls)),
]
