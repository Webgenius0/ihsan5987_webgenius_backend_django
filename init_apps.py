import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from apps.home.models import App

apps_data = [
    ('home', 'Home'),
    ('notifications', 'Notifications'),
    ('profiles', 'Profiles'),
    ('subscription', 'Subscription'),
    ('community_hubs', 'Community Hubs'),
    ('users', 'Users'),
]

for app_name, display_name in apps_data:
    app, created = App.objects.get_or_create(
        app_name=app_name,
        defaults={'display_name': display_name, 'is_active': True}
    )
    if created:
        print(f"✓ Created App: {display_name} ({app_name})")
    else:
        print(f"✓ App already exists: {display_name} ({app_name})")

print("\nAll apps initialized successfully!")
