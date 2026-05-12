import os
import pandas as pd
from collections import defaultdict
from django.utils import timezone
from datetime import timedelta
from celery import shared_task
from .models import (
    Recommendation,
    Category,
    Subcategory,
    UpdateMe,
    Trending,
    Search,
)
from scripts.recommendation import generate_recommendation
from scripts.update_me import generate_update_me_element, generate_update_me_news_set
from scripts.trending import generate_trending_set


# Always use absolute path for categories file
categories_file = "Categories.xlsx"
categories_path = os.path.join(os.path.dirname(__file__), categories_file)
RECOMMENDATION_BATCH_SIZE = 5

# Read Excel file
try:
    df = pd.read_excel(categories_path)
    subcategories = df["Subcategory"].dropna().tolist()
except Exception as e:
    print(f"Error reading Categories.xlsx: {e}")
    df = pd.DataFrame()
    subcategories = []


def get_balanced_subcategories(limit=RECOMMENDATION_BATCH_SIZE):
    """
    Pick subcategories in round-robin order across categories
    so one category cannot dominate a batch.
    """
    if limit <= 0:
        return []

    if "Category" not in df.columns or "Subcategory" not in df.columns:
        return subcategories[:limit]

    rows = (
        df[["Category", "Subcategory"]]
        .dropna(subset=["Category", "Subcategory"])
        .astype(str)
        .apply(lambda col: col.str.strip())
    )

    grouped = defaultdict(list)
    category_order = []
    for _, row in rows.iterrows():
        category_name = row["Category"]
        subcategory_name = row["Subcategory"]
        if not category_name or not subcategory_name:
            continue
        if category_name not in grouped:
            category_order.append(category_name)
        grouped[category_name].append(subcategory_name)

    selected = []
    idx = 0
    while len(selected) < limit:
        made_progress = False
        for category_name in category_order:
            items = grouped[category_name]
            if idx < len(items):
                selected.append(items[idx])
                made_progress = True
                if len(selected) >= limit:
                    break
        if not made_progress:
            break
        idx += 1

    return selected


@shared_task
def recommandation_task():
    print("get recommandation task started")
    selected_subcategories = get_balanced_subcategories()
    recommendations = []
    for subcat in selected_subcategories:
        try:
            recommendations.append(
                generate_recommendation(
                    subcat, prompt_version="v02", categories_file=categories_path
                )
            )
            print("recommendation generated")
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            continue
    print("recommendation task completed", len(recommendations))
    # save the recommendations to the database
    for item in recommendations:
        try:

            category_name = item.get("category", "Others")
            category = Category.objects.filter(
                category_name__iexact=category_name
            ).first()
            if not category:
                category = Category.objects.create(category_name=category_name)
                subcategory_name = item.get("subcategory", "")
                subcategory = Subcategory.objects.create(
                    category=category,
                    subcategory_name=subcategory_name
                )
            else:
                subcategory = category.subcategories.filter(
                    subcategory_name__iexact=item.get("subcategory", "")
                    ).first() or Subcategory.objects.create(
                        category=category,
                        subcategory_name=item.get("subcategory", "")
                    )
            


            Recommendation.objects.create(
                category=category,
                subcategory=subcategory,
                topic=item.get("topic", ""),
                headline=item.get("headline", ""),
                introduction=item.get("introduction", ""),
                key_tips_and_takeaways=item.get("key_tips_and_takeaways", ""),
                fun_facts=item.get("fun_facts", ""),
                conclusion=item.get("conclusion", ""),
                picture_url=item.get("image_url", ""),
            )
            print("recommendation saved")
        except Exception as e:
            print(f"Error saving recommendation: {e}")
            continue


@shared_task
def updateme_task():
    print("update me task started in time")

    # ----- 1️⃣ Save top 3 news -----
    top_three = generate_update_me_news_set()
    for news in top_three:
        try:
            # --- CATEGORY ---
            category_name = (news.get("category") or "Others").strip()
            category = Category.objects.filter(
                category_name__iexact=category_name
            ).first()
            if not category:
                category = Category.objects.create(category_name=category_name)

            # --- SUBCATEGORY ---
            subcategory_name = (news.get("subcategory") or "").strip()
            subcategory = None
            if subcategory_name:
                subcategory = Subcategory.objects.filter(
                    category=category, subcategory_name__iexact=subcategory_name
                ).first()
                if not subcategory:
                    subcategory = Subcategory.objects.create(
                        category=category, subcategory_name=subcategory_name
                    )

            # --- SAVE UPDATE ME ---
            UpdateMe.objects.create(
                category=category,
                subcategory=subcategory,
                topic=news.get("topic", ""),
                short_info=news.get("short_info", ""),
                reference_url=news.get("reference_url", ""),
                background_story=news.get("background_story", ""),
                picture_url=news.get("picture_url", ""),
                is_top3=True,
            )
            print("Top 3 UpdateMe news saved successfully")
        except Exception as e:
            print(f"Error saving Top 3 UpdateMe news: {e}")
            continue

    # ----- 2️⃣ Generate update me for each subtopic -----
    update_me = []
    for subtopic in subcategories[:5]:
        print("subcategory: ", subtopic)
        try:
            update_me.append(
                generate_update_me_element(
                    keywords=subtopic,
                    prompt_type="update_me_general",
                    categories_file=categories_path,
                    prompt_version="v01",
                )
            )
            print("update me element generated")
        except Exception as e:
            print(f"Error generating update me element: {e}")
            continue

    # ----- 3️⃣ Save generated update me -----
    for item in update_me:
        try:
            # --- CATEGORY ---
            category_name = (item.get("category") or "Others").strip()
            category = Category.objects.filter(
                category_name__iexact=category_name
            ).first()
            if not category:
                category = Category.objects.create(category_name=category_name)

            # --- SUBCATEGORY ---
            subcategory_name = (item.get("subcategory") or "").strip()
            subcategory = None
            if subcategory_name:
                subcategory = Subcategory.objects.filter(
                    category=category, subcategory_name__iexact=subcategory_name
                ).first()
                if not subcategory:
                    subcategory = Subcategory.objects.create(
                        category=category, subcategory_name=subcategory_name
                    )

            # --- SAVE UPDATE ME ---
            UpdateMe.objects.create(
                category=category,
                subcategory=subcategory,
                topic=item.get("topic", ""),
                short_info=item.get("short_info", ""),
                reference_url=item.get("reference_url", ""),
                background_story=item.get("background_story", ""),
                picture_url=item.get("picture_url", ""),
                is_archive=item.get("is_archive", False),
            )
            print("UpdateMe saved successfully")
        except Exception as e:
            print(f"Error saving UpdateMe: {e}")
            continue


@shared_task
def trending_task():
    print("trending task started")
    try:
        trending_topics = generate_trending_set(categories_file=categories_path)
    except Exception as e:
        print(f"Error generating trending set: {e}")
        trending_topics = []

    for trend in trending_topics:
        try:
            # ----- CATEGORY -----
            category_name = trend.get("category", "Others").strip() or "Others"

            category = Category.objects.filter(
                category_name__iexact=category_name
            ).first()

            if not category:
                category = Category.objects.create(category_name=category_name)

            # ----- SUBCATEGORY -----
            subcategory_name = trend.get("subcategory", "")
            subcategory_name = (subcategory_name or "").strip()

            subcategory = None

            if subcategory_name:  # only create when name exists
                subcategory = Subcategory.objects.filter(
                    category=category,
                    subcategory_name__iexact=subcategory_name,
                ).first()

                if not subcategory:
                    subcategory = Subcategory.objects.create(
                        category=category, subcategory_name=subcategory_name
                    )

            # ----- SAVE TREND -----
            Trending.objects.create(
                category=category,
                subcategory=subcategory,  # None is allowed
                topic=trend.get("topic", ""),
                description=trend.get("description", ""),
                why_trending=trend.get("why_is_it_trending", []),
                key_points=trend.get("key_points", []),
                outlook=trend.get("overlook_what_might_happen_next", []),
                picture_url=trend.get("picture_url") or trend.get("image_url"),
                links_and_sources=trend.get("links_and_sources"),
            )

            print("New trending news saved to database, successfully!")

        except Exception as e:
            print(f"Error saving trending news data: {e}")
            continue


# delete previous search result after each 3 days
@shared_task
def delete_old_search_results():
    cutoff_date = timezone.now() - timedelta(days=3)
    try:
        from .models import Search

        Search.objects.filter(created_at__lt=cutoff_date).delete()
    except Exception as e:
        print(f"Error deleting old search results: {e}")
        return

    print("Old search results deleted successfully.")


# make a task that loop over updateme , recommendation and trending to false is_active after 24 hours
# the time is set by the django celery beat, so when i set the time it it will run automatically
@shared_task
def deactivate_old_news():
    print("deactivate old news started")
    try:
        from .models import UpdateMe, Recommendation, Trending

        UpdateMe.objects.filter(is_active=True).update(is_active=False)
        Recommendation.objects.filter(is_active=True).update(is_active=False)
        Trending.objects.filter(is_active=True).update(is_active=False)
    except Exception as e:
        print(f"Error deactivating old news: {e}")
        return

    print("deactivate old news completed")


@shared_task
def delete_3_days_old_news():
    print("delete old news task started")
    cutoff_date = timezone.now() - timedelta(days=3)
    try:
        from .models import UpdateMe, Recommendation, Trending

        UpdateMe.objects.filter(created_at__lt=cutoff_date).delete()
        Recommendation.objects.filter(created_at__lt=cutoff_date).delete()
        Trending.objects.filter(created_at__lt=cutoff_date).delete()
    except Exception as e:
        print(f"Error deleting old news: {e}")
        return

    print("delete old news task completed")
