from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('api/home/', include('apps.home.urls')),
    path('api/profiles/', include('apps.profiles.urls')),
    path('api/community/', include('apps.community_hubs.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/subscriptions/', include('apps.subscription.urls')),

    path('schema/', include('schema_viewer.urls')),
]
