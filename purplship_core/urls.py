"""purplship_core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from rest_framework import permissions

from django.contrib import admin
from django.conf.urls import url, include
from django.shortcuts import redirect

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

import purplship_api.views
from purplship_api.router import router

admin.site.site_header = "PurplShip Board"

schema_view = get_schema_view(
   openapi.Info(
      title="PurplShip Cloud API",
      default_version='v1.0-beta',
      description="""
        Multi-carrier shipping API powered by PurlpShip
      """
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

def root_redirect(request):
    schema_view = 'cschema-redoc'
    return redirect(schema_view, permanent=True)


urlpatterns = [
    url(r'^swagger(?P<format>.json|.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^playground/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^redoc-old/$', schema_view.with_ui('redoc-old', cache_timeout=0), name='schema-redoc-old'),

    url(r'^cached/swagger(?P<format>.json|.yaml)$', schema_view.without_ui(cache_timeout=None), name='cschema-json'),
    url(r'^cached/playground/$', schema_view.with_ui('swagger', cache_timeout=None), name='cschema-swagger-ui'),
    url(r'^cached/redoc/$', schema_view.with_ui('redoc', cache_timeout=None), name='cschema-redoc'),
    
    url(r'^$', root_redirect),

    url(r'^admin/', admin.site.urls),
    
    url(r'^v1/', include(router.urls)),
]