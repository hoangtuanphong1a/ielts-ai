from django.urls import path

from .views import today, week

urlpatterns = [path("today/", today), path("week/", week)]
