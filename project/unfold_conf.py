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
                "title": _("Users"),
                "icon": "person",
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("All Users "),
                        "icon": "Groups",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:users_user_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("Profiles"),
                "icon": "person",
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("All Profiles"),
                        "icon": "person",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:profiles_profile_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("FAQ Category"),
                        "icon": "category",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:profiles_faqcategory_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("FAQ Admin"),
                        "icon": "category_search",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:profiles_faq_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Contact Us"),
                        "icon": "contact_page",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:profiles_contactus_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Notification Setting"),
                        "icon": "notification_settings",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy(
                            "admin:profiles_notificationsetting_changelist"
                        ),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Feedback"),
                        "icon": "feedback",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:profiles_feedback_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("App Info"),
                        "icon": "info",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:profiles_appinfo_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("Home"),
                "icon": "home",
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Category"),
                        "icon": "category",
                        "link": reverse_lazy("admin:home_category_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Subcategory"),
                        "icon": "category",
                        "link": reverse_lazy("admin:home_subcategory_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Topic Tag"),
                        "icon": "label",
                        "link": reverse_lazy("admin:home_topictag_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Topic"),
                        "icon": "topic",
                        "link": reverse_lazy("admin:home_topic_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Search Option"),
                        "icon": "saved_search",
                        "link": reverse_lazy("admin:home_searchoption_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Search"),
                        "icon": "search",
                        "link": reverse_lazy("admin:home_search_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Search Tag"),
                        "icon": "sell",
                        "link": reverse_lazy("admin:home_searchtag_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Search History"),
                        "icon": "search_activity",
                        "link": reverse_lazy("admin:home_searchhistory_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Recommendation"),
                        "icon": "recommend",
                        "link": reverse_lazy("admin:home_recommendation_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Update Me"),
                        "icon": "update",
                        "link": reverse_lazy("admin:home_updateme_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Keyword"),
                        "icon": "key",
                        "link": reverse_lazy("admin:home_keyword_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Trending"),
                        "icon": "trending_up",
                        "link": reverse_lazy("admin:home_trending_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Trending User"),
                        "icon": "person_pin",
                        "link": reverse_lazy("admin:home_trendinguser_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Recommendation User"),
                        "icon": "thumb_up",
                        "link": reverse_lazy(
                            "admin:home_recommendationuser_changelist"
                        ),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Bookmark"),
                        "icon": "bookmark",
                        "link": reverse_lazy("admin:home_bookmark_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Preference"),
                        "icon": "tune",
                        "link": reverse_lazy("admin:home_preference_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("Subscriptions"),
                "icon": "subscriptions",
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Packages"),
                        "icon": "package",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:subscription_package_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Subscriber"),
                        "icon": "subscriptions",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy(
                            "admin:subscription_subscription_changelist"
                        ),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("Community Hubs"),
                "icon": "communities",
                "separator": True,  # Top border
                "collapsible": False,  # Collapsible group of links
                "items": [
                    {
                        "title": _("Post"),
                        "icon": "post",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:community_hubs_post_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Comment"),
                        "icon": "comment",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:community_hubs_comment_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Like"),
                        "icon": "thumb_up",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:community_hubs_like_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Comment Report"),
                        "icon": "comments_disabled",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy(
                            "admin:community_hubs_commentreport_changelist"
                        ),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
        ],
    },
}
