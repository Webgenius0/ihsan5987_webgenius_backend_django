from decouple import config
from datetime import date
from .ai_scripts import generate_update_element
from apps.home.models import (
    UpdateMe,
    Category,
    Subcategory,
    Topic
)
keywords = "football world cup 2024"
openai_api_key = config("OPENAI_API_KEY")


def save_update_me():
    data = generate_update_element(keywords, openai_api_key)

    if data:
        print("Generated data:", data)

        category_name = data.get("category")
        subcategory_name = data.get("subcategory")
        topic_title = data.get("topic")
        short_info = data.get("short_info", [])
        reference_url = data.get("reference_url")
        background_story = data.get("background_story", {})
        picture_url = data.get("picture_url")

        # Fetch or create related models
        category, _ = Category.objects.get_or_create(name=category_name)
        subcategory, _ = Subcategory.objects.get_or_create(name=subcategory_name)
        topic, _ = Topic.objects.get_or_create(name=topic_title)

        # Save the update
        UpdateMe.objects.create(
            user_id=1,  # Replace with the correct user ID or logic
            category=category,
            subcategory=subcategory,
            topic=topic,
            short_info=short_info,
            reference_url=reference_url,
            background_story=background_story,
            picture_url=picture_url,
            created_at=date.today(),
            interest=True
        )
        print("News update saved successfully.")
    else:
        print("No data generated.")
