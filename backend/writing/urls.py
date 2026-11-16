from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SubmissionViewSet, WritingPromptViewSet, progress

router = DefaultRouter()
router.register("prompts", WritingPromptViewSet, basename="prompt")
router.register("submissions", SubmissionViewSet, basename="submission")

urlpatterns = [path("progress/", progress)] + router.urls
