from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("judge.urls")),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("accounts.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
