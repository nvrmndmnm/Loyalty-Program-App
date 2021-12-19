from django.urls import reverse
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model, update_session_auth_hash

from accounts.forms import PasswordChangeForm, UserChangeForm

from django.shortcuts import render, redirect
from accounts.forms import UserAdminCreationForm


def register(req):
    form = UserAdminCreationForm()
    if req.method == 'POST':
        form = UserAdminCreationForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    return render(req, 'registration/register.html', {'form': form})


class UserDetailsView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "user_detail.html"
    context_object_name = "user_object"


class ChangeProfileAccessMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object() or self.request.user.is_superuser or self.request.user.groups.filter(name="admins")


class UserUpdateView(ChangeProfileAccessMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = "edit_profile.html"
    context_object_name = "user_object"

    def get_success_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.object.pk})


class ChangePasswordView(ChangeProfileAccessMixin, UpdateView):
    model = get_user_model()
    form_class = PasswordChangeForm
    template_name = "change_password.html"
    context_object_name = "user_object"

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.instance)
        return redirect("accounts:profile", pk=self.get_object().pk)
