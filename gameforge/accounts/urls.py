from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

# Essayer d'importer les vues API si elles existent
try:
    from .views import RegisterView, MeView
    has_api_views = True
except ImportError:
    has_api_views = False

urlpatterns = [
    # Vues HTML traditionnelles
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]

# Ajouter les routes API si elles existent
if has_api_views:
    urlpatterns += [
        path("api/register/", RegisterView.as_view(), name="api_register"),
        path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
        path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
        path("api/me/", MeView.as_view(), name="me"),
    ]
