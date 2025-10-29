from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from aiapp.views import home_view

urlpatterns = [
    path("", home_view, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include("aiapp.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
