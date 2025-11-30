import json
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, Count
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render


def dashboard_callback(request, context):
    # Import models inside function to avoid AppRegistryNotReady
    from apps.users.models import User
    from apps.profiles.models import Profile
    from apps.home.models import Category, Search, Recommendation, Trending, Bookmark
    from apps.community_hubs.models import Post, Comment
    from apps.notifications.models import Notification
    from apps.subscription.models import Subscription

    now = timezone.now()

    # User Statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    new_users_7d = User.objects.filter(created_at__gte=now - timedelta(days=7)).count()
    premium_users = Profile.objects.filter(premium_user=True).count()

    # Content Statistics
    total_categories = Category.objects.count()
    total_searches = Search.objects.count()
    total_recommendations = Recommendation.objects.count()
    total_bookmarks = Bookmark.objects.count()

    # Community Statistics
    total_posts = Post.objects.count()
    total_comments = Comment.objects.count()
    active_posts = Post.objects.filter(created_at__gte=now - timedelta(days=30)).count()
    active_comments = Comment.objects.filter(created_at__gte=now - timedelta(days=30)).count()

    # Business Statistics
    total_subscriptions = Subscription.objects.filter(is_active=True).count()
    total_notifications = Notification.objects.count()
    unread_notifications = Notification.objects.filter(is_read=False).count()

    # Recent Activity
    recent_posts = Post.objects.select_related('user').order_by('-created_at')[:5]
    recent_comments = Comment.objects.select_related('user', 'post').order_by('-created_at')[:5]
    recent_searches = Search.objects.order_by('-created_at')[:5]

    # Chart data for user growth (last 7 days)
    user_growth_data = []
    for i in range(7):
        day = now - timedelta(days=i)
        daily_count = User.objects.filter(created_at__date=day.date()).count()
        user_growth_data.append({
            'date': day.strftime('%Y-%m-%d'),
            'count': daily_count
        })
    user_growth_data.reverse()  # Show most recent first

    # Content distribution pie chart
    content_distribution = [
        {'label': 'Posts', 'value': total_posts},
        {'label': 'Comments', 'value': total_comments},
        {'label': 'Searches', 'value': total_searches},
        {'label': 'Recommendations', 'value': total_recommendations},
    ]

    # Top categories by usage
    top_categories = Category.objects.annotate(
        search_count=Count('search')
    ).order_by('-search_count')[:5]

    # Recent activities (expanded to include more activity types)
    recent_activities = []

    # Add recent posts
    for post in recent_posts[:2]:
        recent_activities.append({
            "icon": "article",
            "description": f"New post by {post.user.name or 'Anonymous'}: {(post.title or 'Untitled')[:30]}...",
            "timestamp": post.created_at
        })

    # Add recent comments
    for comment in recent_comments[:2]:
        recent_activities.append({
            "icon": "chat",
            "description": f"Comment by {comment.user.name or 'Anonymous'} on {(comment.post.title or 'Untitled')[:20]}...",
            "timestamp": comment.created_at
        })

    # Add recent user registrations (new users from last 7 days)
    recent_users = User.objects.filter(created_at__gte=now - timedelta(days=7)).order_by('-created_at')[:2]
    for user in recent_users:
        recent_activities.append({
            "icon": "person_add",
            "description": f"New user registered: {user.name or user.email}",
            "timestamp": user.created_at
        })

    # Add recent searches
    for search in recent_searches[:2]:
        recent_activities.append({
            "icon": "search",
            "description": f"Search performed: {(search.search_term or 'N/A')[:30]} in {search.category.category_name if search.category else 'General'}",
            "timestamp": search.created_at
        })

    # Sort activities by timestamp (most recent first)
    recent_activities.sort(key=lambda x: x['timestamp'], reverse=True)

    # Limit to 8 most recent activities
    recent_activities = recent_activities[:8]

    # Inject into context
    context.update({
        "total_users": total_users,
        "active_users": active_users,
        "new_users_7d": new_users_7d,
        "premium_users": premium_users,
        "total_categories": total_categories,
        "total_searches": total_searches,
        "total_recommendations": total_recommendations,
        "total_bookmarks": total_bookmarks,
        "total_posts": total_posts,
        "total_comments": total_comments,
        "active_posts": active_posts,
        "active_comments": active_comments,
        "total_subscriptions": total_subscriptions,
        "total_notifications": total_notifications,
        "unread_notifications": unread_notifications,
        "recent_posts": recent_posts,
        "recent_comments": recent_comments,
        "recent_searches": recent_searches,
        "user_growth_data_json": json.dumps(user_growth_data, cls=DjangoJSONEncoder),
        "content_distribution_json": json.dumps(content_distribution, cls=DjangoJSONEncoder),
        "top_categories": top_categories,
        "recent_activities": recent_activities,
    })

    return context
