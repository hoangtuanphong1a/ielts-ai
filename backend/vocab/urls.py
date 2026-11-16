from rest_framework.routers import DefaultRouter

from django.urls import path

from .views import CardViewSet, lookup

router = DefaultRouter()
router.register("cards", CardViewSet, basename="card")

urlpatterns = [path("lookup/", lookup)] + router.urls
