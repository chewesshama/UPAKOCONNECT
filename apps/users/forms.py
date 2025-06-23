from django import forms
from mtaa import tanzania
from apps.users.models import CustomUser
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
)


def get_regions():
    return [(region, region) for region in list(tanzania)]

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'phone_number', 'gender',
                  'marital_status', 'nationality', 'role', 'department', 'profile_picture',
                  'region', 'district', 'ward']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['region'].widget = forms.Select(choices=get_regions())

        if 'region' in self.data:
            selected_region = self.data['region']
            try:
                districts = list(tanzania.get(selected_region).districts)
                self.fields['district'].widget = forms.Select(
                    choices=[(d, d) for d in districts]
                )
            except Exception:
                self.fields['district'].widget = forms.Select(choices=[])
        if 'district' in self.data and 'region' in self.data:
            region = self.data['region']
            district = self.data['district']
            try:
                wards = list(tanzania.get(region).districts.get(district).wards)
                self.fields['ward'].widget = forms.Select(
                    choices=[(w, w) for w in wards]
                )
            except Exception:
                self.fields['ward'].widget = forms.Select(choices=[])


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
