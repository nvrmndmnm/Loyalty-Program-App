from django import forms
from django.forms import widgets
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserAdminCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['phone', 'name', 'birth_date', 'email']
        widgets = {
            "birth_date": forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
        }


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["name", "email"]
        label = {"name": "Name", "email": "Email"}


class PasswordChangeForm(forms.ModelForm):
    old_password = forms.CharField(label="Old password", strip=False, widget=forms.PasswordInput)
    password = forms.CharField(label="New password", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirm password", strip=False, widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data["password"]
        password_confirm = self.cleaned_data["password_confirm"]
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords are not equal")
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.instance.check_password(old_password):
            raise forms.ValidationError("Wrong old password")
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ["old_password", "password", "password_confirm"]
