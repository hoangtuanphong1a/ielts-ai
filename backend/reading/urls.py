from rest_framework.routers import DefaultRouter

from .views import AttemptViewSet, PassageViewSet

router = DefaultRouter()
router.register("passages", PassageViewSet, basename="passage")
router.register("attempts", AttemptViewSet, basename="reading-attempt")

urlpatterns = router.urls
