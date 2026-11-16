# Nạp Celery app cùng Django để @shared_task dùng đúng app này
from .celery import app as celery_app

__all__ = ("celery_app",)
