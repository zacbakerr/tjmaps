from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("kefilwe/", include("kefilwe.urls")),
    path("admin/", admin.site.urls),
]