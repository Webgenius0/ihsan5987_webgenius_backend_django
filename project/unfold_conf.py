from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static


UNFOLD = {
    "SITE_TITLE": "SMAILTALK",
    "SITE_HEADER": "SMAILTALK",
    "SITE_SUBHEADER": "Manage your Platform",
    "CUSTOM_CSS": [
        "css/unfold_custom.css",  # relative to static/
    ],
    "SITE_URL": "/",
    # "SITE_ICON": lambda request: static("icon.svg"),  # both modes, optimise for 32px height
    "SITE_ICON": {
        "light": lambda request: static("logo/brand.png"),  # light mode
        "dark": lambda request: static("logo/brand.png"),  # dark mode
    },
    # "SITE_LOGO": lambda request: static("logo.svg"),  # both modes, optimise for 32px height
    # "SITE_LOGO": {
    #     "light": lambda request: static("logo/logo.jpg"),  # light mode
    #     "dark": lambda request: static("logo/logo.jpg"),  # dark mode
    # },
    "SITE_SYMBOL": "speed",  # symbol from icon set
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "500x500",
            "type": "image/svg+xml",
            "href": lambda request: static("logo/logo.jpg"),
        },
    ],
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
    "SHOW_DASHBOARD": True,  # Enable dashboard
    "THEME": "auto",  # Enable theme switching: "light", "dark", or "auto"
    "COLORS": {
        "primary": {
            "50": "255, 248, 235",
            "100": "255, 242, 213",
            "200": "255, 228, 172",
            "300": "255, 212, 131",
            "400": "255, 198, 102",
            "500": "255, 189, 89",
            "600": "226, 158, 61",
            "700": "190, 125, 42",
            "800": "153, 96, 31",
            "900": "120, 74, 24",
            "950": "76, 45, 13",
        }
    },
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Dashboard"),
                "icon": "dashboard",
                "separator": True,  # Top border
                "collapsible": False,  # Not collapsible
                "items": [
                    {
                        "title": _("Admin Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": _("User Management"),
                "icon": "manage_accounts",
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "group",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:users_user_changelist"),
                    },
                    {
                        "title": _("Profiles"),
                        "icon": "badge",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:profiles_profile_changelist"),
                    },
                   
                ],
            },
            {
                "title": _("News Content"),
                "icon": "article",
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Trending"),
                        "icon": "trending_up",
                        "link": reverse_lazy("admin:home_trending_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Update Me"),
                        "icon": "arrow_circle_up",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:home_updateme_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Recommendation"),
                        "icon": "recommend",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:home_recommendation_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("News by Search"),
                        "icon": "search",
                        "link": reverse_lazy("admin:home_search_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    }
                ],
            },
            {
                "title": _("Content Management"),
                "icon": "article",
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Categories"),
                        "icon": "category",
                        "link": reverse_lazy("admin:home_category_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Subcategories"),
                        "icon": "subdirectory_arrow_right",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:home_subcategory_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Search History"),
                        "icon": "history",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:home_searchhistory_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Preferences"),
                        "icon": "favorite",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:home_preference_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Community Posts"),
                        "icon": "forum",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:community_hubs_post_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Comments"),
                        "icon": "comment",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:community_hubs_comment_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Likes"),
                        "icon": "thumb_up",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:community_hubs_like_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Comment Reports"),
                        "icon": "report",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy(
                            "admin:community_hubs_commentreport_changelist"
                        ),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("Business Operations"),
                "icon": "business",
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Packages"),
                        "icon": "card_membership",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:subscription_package_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Notifications"),
                        "icon": "notifications_active",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy(
                            "admin:notifications_notification_changelist"
                        ),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Subscriptions"),
                        "icon": "subscriptions",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy(
                            "admin:subscription_subscription_changelist"
                        ),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("System Administration"),
                "icon": "admin_panel_settings",
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Periodic Tasks"),
                        "icon": "schedule",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy(
                            "admin:django_celery_beat_periodictask_changelist"
                        ),
                    },
                    {
                        "title": _("FAQs"),
                        "icon": "help_center",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:profiles_faq_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Contact Us"),
                        "icon": "contact_support",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:profiles_contactus_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Feedback"),
                        "icon": "feedback",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:profiles_feedback_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("App Settings"),
                        "icon": "settings_applications",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:profiles_appinfo_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("API Management"),
                        "icon": "api",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:profiles_apikey_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
        ],
    },
    "DASHBOARD_CALLBACK": "apps.profiles.admin_dashboard.dashboard_callback",
}
