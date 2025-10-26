"""
Configuration file for API keys and settings.
"""

from apps.profiles.models import APIKey

# News API Key
if APIKey.objects.filter(ai_name="News API Key").exists():
    NEWS_API_KEY = APIKey.objects.get(ai_name="News API Key").key
else:
    NEWS_API_KEY = "504d059f9d7adc20294d4045322bd5a1ec1e0b7c01e5de3d8659f65237970436"

# GNews API Key
if APIKey.objects.filter(ai_name="GNews API Key").exists():
    GNEWS_API_KEY = APIKey.objects.get(ai_name="GNews API Key").key
else:
    GNEWS_API_KEY = 'e659c908c046636704481f76110d0622'

# OpenAI API Key
if APIKey.objects.filter(ai_name="OpenAI API Key").exists():
    OPENAI_API_KEY = APIKey.objects.get(ai_name="OpenAI API Key").key
else:
    OPENAI_API_KEY = "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"  # Your OpenAI API key

# Perplexity API Key 
if APIKey.objects.filter(ai_name="Perplexity API Key").exists():
    PERPLEXITY_API_KEY = APIKey.objects.get(ai_name="Perplexity API Key").key
else:
    PERPLEXITY_API_KEY = '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'


# Other configuration settings
DEFAULT_REGION = 'us'
DEFAULT_NUM_RESULTS = 15
DEFAULT_LANGUAGE = 'en'
PROMPT_VERSION = 'v01'