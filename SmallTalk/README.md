# SmallTalk Module

The SmallTalk module provides AI-powered conversation assistance features for the main Django application. It integrates with various external APIs to generate contextual information for small talk conversations.

## Features

- News aggregation and summarization
- Trending topics detection
- Personalized recommendations
- Smart search capabilities
- Natural language processing

## Configuration

API keys are configured in `SmallTalk/config.py`:

```python
# News API Key (used for news aggregation)
NEWS_API_KEY = "your_newsapi_key"

# GNews API Key (alternative news source)
GNEWS_API_KEY = "your_gnews_key"

# OpenAI API Key (for LLM capabilities)
OPENAI_API_KEY = "your_openai_key"

# Perplexity API Key (for advanced search)
PERPLEXITY_API_KEY = "your_perplexity_key"
```

## API Key Status

To check the status of API keys, run:
```bash
python utility/check_api_keys.py
```

## Core Components

### 1. API Utilities (`api_utils.py`)

Provides helper functions for:
- News fetching from Google News and RSS feeds
- Trending topics extraction
- Image fetching for topics
- Alternative news sources

### 2. LLM Utilities (`llm_utils.py`)

Handles interactions with language models:
- OpenAI GPT integration
- Perplexity API integration
- JSON response validation and fixing
- Prompt building for various use cases

### 3. Recommendation Engine (`recommendation.py`)

Generates personalized recommendations based on:
- User preferences
- Current trends
- Historical interactions

## Usage Examples

### Basic Search
```python
from SmallTalk.search_bar import search_bar

# Get search results for a topic
results = search_bar("artificial intelligence")
```

### Trending Topics
```python
from SmallTalk.trending import generate_trending

# Generate trending topics
trending = generate_trending("technology")
```

### Recommendations
```python
from SmallTalk.recommendation import generate_recommendation

# Generate recommendations
recommendations = generate_recommendation("science")
```

## API Integration Details

### OpenAI API
- Used for natural language processing
- Model: GPT-3.5-turbo (configurable)
- Features: Text generation, summarization, question answering

### Perplexity API
- Used for advanced search and information retrieval
- Model: Sonar series
- Features: Real-time information retrieval, fact checking

### GNews API
- Used for news aggregation
- Features: Top headlines, search by keywords, multiple sources

### News API
- Alternative news source
- Features: Top headlines, everything endpoint, sources

## Error Handling

The module includes comprehensive error handling for:
- API rate limits
- Invalid API keys
- Network issues
- JSON parsing errors
- Timeout errors

## Testing

To test the API keys, run:
```bash
python utility/check_api_keys.py
```

This will check the validity of all configured API keys and report any expired or invalid ones.
