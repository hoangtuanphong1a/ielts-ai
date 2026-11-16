from datetime import timedelta
from pathlib import Path
import os
import sys

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# .env nằm ở thư mục gốc ielts-ai/ (cùng chỗ docker-compose.yml)
load_dotenv(BASE_DIR.parent / ".env")

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "accounts",
    "writing",
    "vocab",
    "coach",
    "reading",
    "drf_spectacular",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

TESTING = "test" in sys.argv

# Test luôn chạy SQLite (nhanh, không cần Docker). Dev/prod theo DB_ENGINE trong .env.
if TESTING or os.environ.get("DB_ENGINE", "sqlite") == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "ielts_ai"),
            "USER": os.environ.get("POSTGRES_USER", "ielts"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
            "HOST": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
            "PORT": os.environ.get("POSTGRES_PORT", "5434"),
            "CONN_MAX_AGE": 60,
        }
    }

REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6380/0")

# Celery (T0.8). Test chạy task ngay tại chỗ (eager), không cần Redis/worker.
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TASK_ALWAYS_EAGER = TESTING or os.environ.get("CELERY_EAGER", "0") == "1"
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_TIMEZONE = "Asia/Ho_Chi_Minh"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Ho_Chi_Minh"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_THROTTLE_RATES": {
        "password_reset": "5/hour",  # chống spam email / dò tài khoản
    },
}

# Email: dev in ra console; prod đặt EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend + EMAIL_HOST...
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "IELTS AI <no-reply@ielts-ai.local>")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")
PASSWORD_RESET_TIMEOUT = 60 * 60  # link đặt lại mật khẩu hết hạn sau 1 giờ (T1.2)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

CORS_ALLOWED_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]

# Đường dẫn model ML đã train (nếu có). Không có file -> dùng scorer heuristic.
ML_MODEL_PATH = BASE_DIR / "ml" / "artifacts" / "band_model.joblib"

# API docs (T0.8): /api/schema/ (OpenAPI) và /api/docs/ (Swagger UI)
SPECTACULAR_SETTINGS = {
    "TITLE": "IELTS AI API",
    "DESCRIPTION": "Personalised IELTS preparation powered by AI/NLP. Auth: JWT Bearer (POST /api/auth/token/).",
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
}

# T2.3: LanguageTool local (docker-compose). Test: None -> bỏ qua kiểm tra ngữ pháp.
LANGUAGETOOL_URL = None if TESTING else os.environ.get("LANGUAGETOOL_URL", "http://127.0.0.1:8081")
