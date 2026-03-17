"""
Configuration file for API keys and settings.
"""
import os
from apps.profiles.models import APIKey

# News API Key
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
try:
    if APIKey.objects.filter(ai_name="News API Key").exists():
        NEWS_API_KEY = APIKey.objects.get(ai_name="News API Key").key
    else:
        NEWS_API_KEY = NEWS_API_KEY
except Exception:
    NEWS_API_KEY = NEWS_API_KEY

# GNews API Key
try:
    if APIKey.objects.filter(ai_name="GNews API Key").exists():
        GNEWS_API_KEY = APIKey.objects.get(ai_name="GNews API Key").key
    else:
        GNEWS_API_KEY = GNEWS_API_KEY
except Exception:
    GNEWS_API_KEY = GNEWS_API_KEY

# OpenAI API Key
# if APIKey.objects.filter(ai_name="OpenAI API Key").exists():
#     OPENAI_API_KEY = APIKey.objects.get(ai_name="OpenAI API Key").key
# else:

# OPENAI_API_KEY = "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"  # Your OpenAI API key

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Perplexity API Key
try:
    if APIKey.objects.filter(ai_name="Perplexity API Key").exists():
        PERPLEXITY_API_KEY = APIKey.objects.get(ai_name="Perplexity API Key").key
    else:
        # PERPLEXITY_API_KEY = "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"
        PERPLEXITY_API_KEY = PERPLEXITY_API_KEY
except Exception:
    # PERPLEXITY_API_KEY = "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"
    PERPLEXITY_API_KEY = PERPLEXITY_API_KEY

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Other configuration settings
DEFAULT_REGION = "us"
DEFAULT_NUM_RESULTS = 15
DEFAULT_LANGUAGE = "en"
PROMPT_VERSION = "v01"
