from django.urls import path
from .views import generate_local_view

urlpatterns = [
    path("generate/", generate_local_view, name="generate_local"),
]
