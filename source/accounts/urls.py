from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from accounts import views as accounts_views

app_name = 'accounts'

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("create/", accounts_views.RegisterView.as_view(), name="register"),
    path("<int:pk>/", accounts_views.UserDetailsView.as_view(), name="profile"),
    path("<int:pk>/edit/", accounts_views.UserUpdateView.as_view(), name="edit_profile"),
    path("<int:pk>/change-password/", accounts_views.ChangePasswordView.as_view(), name="change_password")
]
