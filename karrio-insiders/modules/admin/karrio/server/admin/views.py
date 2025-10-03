from django.urls import path
from django.views.decorators.csrf import csrf_exempt

import karrio.server.graph.views as views
import karrio.server.admin.schema as schema


urlpatterns = [
    path(
        "admin/graphql/",
        csrf_exempt(views.GraphQLView.as_view(schema=schema.schema)),
        name="admin-graph",
    ),
    path(
        "admin/graphql",
        csrf_exempt(views.GraphQLView.as_view(schema=schema.schema)),
        name="admin-graph",
    ),
]
