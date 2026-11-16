from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny

urlpatterns = [
    path("admin/", admin.site.urls),
    # Tài liệu API (T0.8): xem không cần đăng nhập
    path("api/schema/", SpectacularAPIView.as_view(permission_classes=[AllowAny]), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema", permission_classes=[AllowAny])),
    path("api/auth/", include("accounts.urls")),
    path("api/writing/", include("writing.urls")),
    path("api/vocab/", include("vocab.urls")),
    path("api/coach/", include("coach.urls")),
    path("api/reading/", include("reading.urls")),
]
