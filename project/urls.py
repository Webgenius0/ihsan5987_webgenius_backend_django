from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="SmallTalk",
        default_version="v1",
        description="API documentation",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.users.urls")),
    path("api/home/", include("apps.home.urls")),
    path("api/profiles/", include("apps.profiles.urls")),
    path("api/community/", include("apps.community_hubs.urls")),
    path("api/notifications/", include("apps.notifications.urls")),
    path("api/subscriptions/", include("apps.subscription.urls")),
    
    path("schema/", include("schema_viewer.urls")),  # database schema
    path("swagger/",schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui",),  # Swagger API documentation
]
