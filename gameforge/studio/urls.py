from django.urls import path
from .views import LocalGenerateConceptView

urlpatterns = [
    path("generate/", LocalGenerateConceptView.as_view(), name="studio-generate"),
]
