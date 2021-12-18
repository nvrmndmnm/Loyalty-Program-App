from django import forms


class UserSearchForm(forms.Form):
    id = forms.CharField(max_length=150, required=False, label='Search')
