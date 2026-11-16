"""Celery app (T0.8).

Chạy worker (Windows cần --pool=solo):
    celery -A config worker -l info --pool=solo
"""
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("ielts_ai")
# Đọc mọi biến CELERY_* trong settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")
# Tự tìm tasks.py trong các app đã cài
app.autodiscover_tasks()


@app.task
def ping():
    """Task kiểm tra worker còn sống."""
    return "pong"
