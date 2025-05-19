from django.apps import AppConfig


class CommunityHubsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.community_hubs'

    def ready(self):
        import apps.notifications.signals