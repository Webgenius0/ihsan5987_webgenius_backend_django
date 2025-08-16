# SmallTalk - AI-Powered Conversation Assistant

SmallTalk is a Django-based API that provides AI-powered conversation assistance with features like news updates, trending topics, recommendations, and search capabilities. The system integrates with multiple external APIs to provide rich, contextual information for small talk conversations.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Guide](#setup-guide)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Database Setup](#database-setup)
  - [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
  - [Authentication](#authentication)
  - [API Endpoints](#api-endpoints)
  - [External APIs](#external-apis)
- [Project Apps](#project-apps)
- [Celery & Background Tasks](#celery--background-tasks)
- [Deployment](#deployment)

## Features

- News aggregation from multiple sources
- Trending topics detection
- Personalized recommendations
- Smart search capabilities
- Community hubs for user discussions
- User profiles and preferences
- Subscription management
- Push notifications
- Admin dashboard with Unfold

## Project Structure

```
.
├── apps/                    # Django apps
│   ├── community_hubs/     # Community discussion features
│   ├── home/               # Core features (categories, topics, updates)
│   ├── notifications/      # Push notifications
│   ├── profiles/           # User profiles
│   ├── subscription/       # Subscription management
│   └── users/              # User authentication and management
├── project/                # Main Django project settings
├── SmallTalk/              # AI/LLM utilities and configurations
├── static/                 # Static files
├── media/                  # Media files
└── utility/                # Utility scripts
```

## Setup Guide

### Prerequisites

- Python 3.8+
- PostgreSQL
- Redis (for Celery)
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ihsan5987_django
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Stripe settings
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret

# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key

# Email settings
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
ADMIN_EMAIL=your_admin_email@gmail.com

# Supabase settings
SUPABASE_PROJECT_ID=your_supabase_project_id

# Database settings (if using different database)
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port
```

### Database Setup

1. Ensure PostgreSQL is running
2. Create the database:
   ```bash
   createdb postgres
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```

### Running the Application

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. (Optional) Start Celery worker for background tasks:
   ```bash
   celery -A project worker --loglevel=info
   ```

3. (Optional) Start Celery beat for scheduled tasks:
   ```bash
   celery -A project beat --loglevel=info
   ```

The application will be available at `http://127.0.0.1:8000/`

## API Documentation

### Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. Obtain a token by sending a POST request to `/api/token/` with username and password
2. Include the token in the Authorization header for subsequent requests:
   ```
   Authorization: Bearer <your_token>
   ```

### API Endpoints

#### Core API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/home/categories/` | GET | List all categories |
| `/api/home/categories/<id>/` | GET | Get specific category |
| `/api/home/subcategories/` | GET | List all subcategories |
| `/api/home/subcategories/<id>/` | GET | Get specific subcategory |
| `/api/home/topics/` | GET | List all topics |
| `/api/home/topics/<id>/` | GET | Get specific topic |
| `/api/home/update/` | GET | Get latest updates |
| `/api/home/update/<id>/` | GET | Get specific update |
| `/api/home/trending-now/` | GET | Get trending topics |
| `/api/home/trending-now/<id>/` | GET | Get specific trending topic |
| `/api/home/recommendations/` | GET | Get recommendations |
| `/api/home/recommendations/<id>/` | GET | Get specific recommendation |
| `/api/home/preferences/` | GET/POST | Get or create user preferences |
| `/api/home/bookmarks/` | GET/POST | Get or create bookmarks |
| `/api/home/search-bar/` | GET | Perform search |
| `/api/home/search-history/` | GET | Get search history |
| `/api/home/search-history/<id>/` | GET/DELETE | Get or delete specific search history |

#### User Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/register/` | POST | User registration |
| `/api/login/` | POST | User login |
| `/api/logout/` | POST | User logout |
| `/api/token/` | POST | Obtain JWT token |
| `/api/token/refresh/` | POST | Refresh JWT token |
| `/api/profile/` | GET/PUT | Get or update user profile |
| `/api/change-password/` | POST | Change user password |

#### Community Hubs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/community/posts/` | GET/POST | List or create community posts |

#### Notifications

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/notifications/` | GET | List user notifications |
| `/api/notifications/<id>/` | GET/PATCH | Get or update specific notification |
| `/api/notifications/mark-all-read/` | POST | Mark all notifications as read |

#### Subscriptions

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/subscriptions/plans/` | GET | List subscription plans |
| `/api/subscriptions/subscribe/` | POST | Subscribe to a plan |
| `/api/subscriptions/cancel/` | POST | Cancel subscription |
| `/api/subscriptions/webhook/` | POST | Stripe webhook endpoint |

### External APIs

The application integrates with several external APIs:

1. **OpenAI API**
   - Used for natural language processing and generation
   - Key stored in `OPENAI_API_KEY` environment variable

2. **GNews API**
   - Used for news aggregation
   - Key configured in `project/settings.py`

3. **Perplexity API** (in SmallTalk module)
   - Used for advanced search and information retrieval
   - Key stored in `SmallTalk/config.py`

4. **News API** (in SmallTalk module)
   - Alternative news source
   - Key stored in `SmallTalk/config.py`

**Note on API Keys:**
During our check, we found that the following API keys in `SmallTalk/config.py` are expired/invalid:
- News API Key
- Perplexity API Key

These need to be updated with valid keys for full functionality.

## Project Apps

### 1. Home (`apps/home/`)
Core functionality including categories, topics, updates, trending topics, recommendations, and search features.

### 2. Users (`apps/users/`)
User authentication, registration, and management.

### 3. Profiles (`apps/profiles/`)
User profile management and preferences.

### 4. Community Hubs (`apps/community_hubs/`)
Community discussion features and post management.

### 5. Notifications (`apps/notifications/`)
Push notification system using Firebase Cloud Messaging.

### 6. Subscription (`apps/subscription/`)
Subscription management with Stripe integration.

## Celery & Background Tasks

The project uses Celery for background task processing:

- **Redis** is used as the message broker
- Tasks are defined in `apps/*/tasks.py` files
- Scheduled tasks are managed through `django_celery_beat`

To run Celery:
```bash
# Start worker
celery -A project worker --loglevel=info

# Start beat scheduler
celery -A project beat --loglevel=info
```

## Deployment

The application is configured for deployment on Render with the following settings:

- PostgreSQL database connection
- CORS settings for web client
- Static and media file serving
- Environment variable configuration

For production deployment:
1. Set all required environment variables
2. Configure the database connection
3. Set up Redis for Celery
4. Configure email settings
5. Set up Stripe webhook endpoint