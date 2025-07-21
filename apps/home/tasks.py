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

categories_file = "Categories.xlsx"
categories_path = os.path.join(os.path.dirname(__file__), categories_file)
df = pd.read_excel(categories_path)
subcategories = df["Subcategory"].dropna().tolist()


@shared_task
def recommandation_task():
    print("get recommandation task started")
    recommendations = []
    for subcat in subcategories:
        try:
            recommendations.append(
                generate_recommendation(
                    subcat, prompt_version="v02", categories_file=categories_path
                )
            )
            print("recommendation generated")
        except Exception as e:
            continue
            print(f"Error generating recommendations: {e}")
    print("recommendation task completed", len(recommendations))
    # save the recommendations to the database
    for item in recommendations:
        try:
            Recommendation.objects.create(
                category=Category.objects.get_or_create(
                    category_name__icontains=item["category"]
                )[0],
                topic=Topic.objects.get_or_create(name=item["topic"])[0],
                headline=item["headline"],
                introduction=item["introduction"],
                key_tips_and_takeaways=item["key_tips_and_takeaways"],
                fun_facts=item["fun_facts"],
                conclusion=item["conclusion"],
                picture_url=item["image_url"],
            )
            print("recommendation saved")
        except Exception as e:
            print(f"Error saving recommendation: {e}")
            continue


@shared_task
def updateme_task():
    print("update me task started")
    update_me = []
    for subtopic in subcategories:
        try:
            update_me.append(
                generate_update_me_element(
                    keywords=subtopic,
                    prompt_type="update_me_general",
                    categories_file=categories_path,
                    prompt_version="v01",
                )
            )
        except Exception as e:
            continue

    # save the update me to the database
    for item in update_me:
        try:
            UpdateMe.objects.create(
                category= Category.objects.get_or_create(category_name__icontains=item['category'])[0],
                subcategory=Subcategory.objects.get_or_create(subcategory_name__icontains=item['subcategory'])[0],
                topic=Topic.objects.get_or_create(name=item['topic'])[0],
                short_info=item['short_info'],
                reference_url=item['reference_url'],
                background_story=item['background_story'],
                picture_url=item['picture_url']
            )
        except Exception as e:
            continue


@shared_task
def trending_task():
    print("trending task started")
    trending_topics = generate_trending_set()

    for trend in trending_topics:
        try:
            Trending.objects.create(
                category=Category.objects.get_or_create(
                    category_name__icontains=trend["category"]
                )[0],
                subcategory=Subcategory.objects.get_or_create(
                    subcategory_name__icontains=trend["subcategory"]
                )[0],
                description=trend["description"],
                why_trending=trend["why_is_it_trending"],
                key_points=trend["key_points"],
                outlook=trend["overlook_what_might_happen_next"],
                picture_url=trend["picture_url"],
            )
            print('New trending news saved to database, successfully!')
        except Exception as e:
            print(f"Error saving trending news data: {e}")
            continue
