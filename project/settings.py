from .unfold_conf import UNFOLD
import os
from pathlib import Path
import cloudinary
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-@unv(phjz=6caf$!bew*e01cj9xz*eg-#11x7n=(^sc3aca7k!"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

AUTH_USER_MODEL = "users.User"

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "fcm_django",
    "rest_framework_simplejwt.token_blacklist",
    "apps.home",
    "apps.users",
    "import_export",
    "schema_viewer",
    # cloudinary
    "cloudinary",
    "django_celery_beat",
    # my apps
    "apps.profiles.apps.ProfilesConfig",
    "apps.subscription.apps.SubscriptionConfig",
    "apps.community_hubs",
    "apps.notifications",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 3d party middleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "querycount.middleware.QueryCountMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres.odpilpqlyscsreefmtit",
        "PASSWORD": "shcQivH9xxH31J1X1Hxohjbh",
        "HOST": "aws-0-eu-central-1.pooler.supabase.com",
        "PORT": "5432",
        "OPTIONS": {
            "sslmode": "require",
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Dhaka"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # collectstatic target
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

# Email sending setup
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"  # or your SMTP provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "towhidulislam.mail@gmail.com"
EMAIL_HOST_PASSWORD = "bdui nxzn dogt fqxl"

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMIN_EMAIL = "towhidulislam.mail@gmail.com"

# CORS setup
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://ihsan5987-django.onrender.com",
]

# csrf setup
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://ihsan5987-django.onrender.com",
    "https://ece4-103-174-189-33.ngrok-free.app",
]

# GNEWS_API_KEY
GNEWS_API_KEY = "c8953ffc8769d9e01b10e01713d86e34"
# Cloudinary setup
cloudinary.config(
    cloud_name="dt99uhnhh",
    api_key="441948348178278",
    api_secret="OAgOpdxpTDNw9LvMzvDekZdweSI",
    secure=True,
)

# Simple JWT setup
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    # Refresh Token Rotation
    "ROTATE_REFRESH_TOKENS": True,  # generates a new refresh token when used
    "BLACKLIST_AFTER_ROTATION": True,
}

# Stripe settings
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

STRIPE_SUCCESS_URL = "http://127.0.0.1:8000/api/subscriptions/success/"
STRIPE_CANCEL_URL = "http://127.0.0.1:8000/api/subscriptions/cancel/"


# Unfold Admin Customization

# unfold admin config
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "django_errors.log",
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,  # Keep 5 old log files
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "WARNING",
        },
    },
    "root": {
        "handlers": ["file", "console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "WARNING",
            "propagate": True,
        },
    },
}


CELERY_BROKER_URL = "redis://localhost:6379/0"  # or RabbitMQ if you're using it
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
