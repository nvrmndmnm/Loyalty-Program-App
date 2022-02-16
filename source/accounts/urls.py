from django.contrib.auth.views import LoginView, LogoutView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, reverse_lazy
from accounts import views as accounts_views

app_name = 'accounts'

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path("create/", accounts_views.RegisterView.as_view(), name="register"),
    path("<int:pk>/", accounts_views.UserDetailsView.as_view(), name="profile"),
    path("<int:pk>/edit/", accounts_views.UserUpdateView.as_view(), name="edit_profile"),
    path("<int:pk>/change-password/", accounts_views.ChangePasswordView.as_view(), name="change_password"),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html",
                                          success_url=reverse_lazy('accounts:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done/',
         PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
         name='password_reset_complete'),
]
