# import requests
# from django.conf import settings
# from .models import TrendingNews, RecommendedNews
# from datetime import datetime

def trending_news_store():
    categories = ['general', 'world', 'nation', 'business', 'technology',
                  'entertainment', 'sports', 'science', 'health', 'politics']

    for category in categories:
        params = {
            'token': settings.GNEWS_API_KEY,
            'lang': 'en',
            'country': 'us',
            'max': 10,
            'q': category,
        }

        try:
            response = requests.get("https://gnews.io/api/v4/top-headlines", params=params)
            response.raise_for_status()
            data = response.json()

            for article in data.get('articles', []):
                TrendingNews.objects.update_or_create(
                    url=article['url'],
                    defaults={
                        'title': article.get('title'),
                        'description': article.get('description'),
                        'content': article.get('content'),
                        'image': article.get('image'),
                        'published_at': article.get('publishedAt') or datetime.utcnow(),
                        'source_name': article.get('source', {}).get('name'),
                        'source_url': article.get('source', {}).get('url'),
                        'category': category,
                    }
                )
        except Exception as e:
            print(f"Error fetching {category} news: {str(e)}")


# def recommended_news_store():
#     categories = ['general', 'world', 'nation', 'business', 'technology',
#                   'entertainment', 'sports', 'science', 'health', 'politics']

#     for category in categories:
#         params = {
#             'token': settings.GNEWS_API_KEY,
#             'lang': 'en',
#             'country': 'us',
#             'max': 10,
#             'q': category,
#         }

#         try:
#             response = requests.get("https://gnews.io/api/v4/top-headlines", params=params)
#             response.raise_for_status()
#             data = response.json()

#             for article in data.get('articles', []):
#                 RecommendedNews.objects.update_or_create(
#                     url=article['url'],
#                     defaults={
#                         'title': article.get('title'),
#                         'description': article.get('description'),
#                         'content': article.get('content'),
#                         'image': article.get('image'),
#                         'published_at': article.get('publishedAt') or datetime.utcnow(),
#                         'source_name': article.get('source', {}).get('name'),
#                         'source_url': article.get('source', {}).get('url'),
#                         'category': category,
#                     }
#                 )
#         except Exception as e:
#             print(f"Error fetching {category} news: {str(e)}")
