import os
import pandas as pd
from celery import shared_task

from .models import (
    Recommendation,
    Category,
    Subcategory,
    Topic,
    UpdateMe,
    Trending,
)

from SmallTalk.recommendation import generate_recommendation
from SmallTalk.update_me import generate_update_me_element
from SmallTalk.trending import generate_trending_set

# Always use absolute path for categories file
categories_file = "Categories.xlsx"
categories_path = os.path.join(os.path.dirname(__file__), categories_file)

# Read Excel file
try:
    df = pd.read_excel(categories_path)
    subcategories = df["Subcategory"].dropna().tolist()
except Exception as e:
    print(f"Error reading Categories.xlsx: {e}")
    subcategories = []


@shared_task
def recommandation_task():
    print("get recommandation task started")
    recommendations = []
    for subcat in subcategories[:]:
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
            category = Category.objects.filter(category_name__iexact=category_name).first()
            if not category:
                category = Category.objects.create(category_name=category_name)

            topic_name = item.get("topic", "Unknown")
            topic = Topic.objects.filter(name__iexact=topic_name).first()
            if not topic:
                topic = Topic.objects.create(name=topic_name)

            Recommendation.objects.create(
                category=category,
                topic=topic,
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
    update_me = []
    for subtopic in subcategories[:10]:
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

    # save the update me to the database
    for item in update_me:
        try:
            category_name = item.get("category", "Others")
            category = Category.objects.filter(category_name__iexact=category_name).first()
            if not category:
                category = Category.objects.create(category_name=category_name)

            subcategory_name = item.get("subcategory", "")
            subcategory = Subcategory.objects.filter(subcategory_name__iexact=subcategory_name).first()
            if not subcategory:
                subcategory = Subcategory.objects.create(subcategory_name=subcategory_name)

            topic_name = item.get("topic", "Unknown")
            topic = Topic.objects.filter(name__iexact=topic_name).first()
            if not topic:
                topic = Topic.objects.create(name=topic_name)

            UpdateMe.objects.create(
                category=category,
                subcategory=subcategory,
                topic=topic,
                short_info=item.get("short_info", ""),
                reference_url=item.get("reference_url", ""),
                background_story=item.get("background_story", ""),
                picture_url=item.get("picture_url", ""),
            )
            print("UpdateMe saved successfully")
        except Exception as e:
            print(f"Error saving UpdateMe: {e}")
            continue

        # generate update me user


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
            category_name = trend.get("category", "Others")
            category = Category.objects.filter(category_name__iexact=category_name).first()
            if not category:
                category = Category.objects.create(category_name=category_name)

            subcategory_name = trend.get("subcategory", "")
            subcategory = Subcategory.objects.filter(subcategory_name__iexact=subcategory_name).first()
            if not subcategory:
                subcategory = Subcategory.objects.create(subcategory_name=subcategory_name)

            Trending.objects.create(
                category=category,
                subcategory=subcategory,
                description=trend.get("description", ""),
                why_trending=trend.get("why_is_it_trending", []),
                key_points=trend.get("key_points", []),
                outlook=trend.get("overlook_what_might_happen_next", []),
                picture_url=trend.get("picture_url", ""),
            )
            print("New trending news saved to database, successfully!")
        except Exception as e:
            print(f"Error saving trending news data: {e}")
            continue
