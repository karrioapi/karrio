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

from purpleserver.proxy.views import router as proxy_router
from purpleserver.core.views import router as core_router

logging.getLogger('purplship').setLevel(logging.NOTSET)

admin.site.site_header = "PurplShip"
admin.site.site_title = "PurplShip"
admin.site.index_title = "Administration"

schema_view = get_schema_view(
   openapi.Info(
      title="PurplShip Multi-carrier API",
      default_version='v1',
      description=(
          "PurplShip is a Multi-carrier Shipping API that simplifies the integration of logistic carrier services"
      ),
      contact=openapi.Contact(email="hello@purplship.com"),
      license=openapi.License(name="AGPLv3+ License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('v1/', include(proxy_router.urls + core_router.urls)),
]
