from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from mtaa import tanzania
from .models import Patient
from apps.complaints.models import Department
from apps.users.models import CustomUser
from phonenumber_field.formfields import PhoneNumberField
from django_countries.fields import CountryField
from apps.core.utils import get_regions



class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate region choices
        self.fields['delivery_place_region'].choices = [(r, r) for r in list(tanzania)]

        # Dynamically load districts based on selected region
        if 'delivery_place_region' in self.data:
            region = self.data.get('delivery_place_region')
            if region and region in list(tanzania):
                self.fields['delivery_place_district'].choices = [(d, d) for d in list(tanzania.get(region).districts)]


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter first name"})
    )
    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter last name"})
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter username"})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email"})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"})
    )
    gender = forms.ChoiceField(
        choices=CustomUser.GENDER_CHOICES,
        label="Gender",
        widget=forms.Select(attrs={"class": "form-control", "placeholder": "Select gender"})
    )
    marital_status = forms.ChoiceField(
        choices=CustomUser.MARITAL_STATUS_CHOICES,
        label="Marital Status",
        widget=forms.Select(attrs={"class": "form-control", "placeholder": "Select marital status"})
    )
    nationality = CountryField(blank_label="(Select Country)").formfield(
        widget=forms.Select(attrs={"class": "form-control", "placeholder": "Select country"})
    )
    phone_number = PhoneNumberField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter phone number (e.g., +255123456789)"})
    )
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label="Position",
        widget=forms.Select(attrs={"class": "form-control", "placeholder": "Select position"})
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        label="Department",
        widget=forms.Select(attrs={"class": "form-control", "placeholder": "Select department"})
    )
    region = forms.ChoiceField(
        choices=get_regions(),
        required=False,
        label="Region",
        widget=forms.Select(attrs={"class": "form-control", "id": "id_region", "placeholder": "Select region"})
    )
    district = forms.CharField(  # Changed to CharField
        required=False,
        label="District",
        widget=forms.Select(attrs={"class": "form-control", "id": "id_district", "placeholder": "Select district"})
    )
    ward = forms.CharField(  # Changed to CharField
        required=False,
        label="Ward",
        widget=forms.Select(attrs={"class": "form-control", "id": "id_ward", "placeholder": "Select ward"})
    )
    profile_picture = forms.ImageField(
        required=False,
        label="Profile Picture",
        widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Upload profile picture"})
    )

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
            "gender",
            "marital_status",
            "nationality",
            "phone_number",
            "role",
            "department",
            "region",
            "district",
            "ward",
            "profile_picture",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.gender = self.cleaned_data["gender"]
        user.marital_status = self.cleaned_data["marital_status"]
        user.nationality = self.cleaned_data["nationality"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.role = self.cleaned_data["role"]
        user.department = self.cleaned_data["department"]
        user.region = self.cleaned_data["region"]
        user.district = self.cleaned_data["district"]
        user.ward = self.cleaned_data["ward"]
        user.profile_picture = self.cleaned_data["profile_picture"]
        if commit:
            user.save()
            if self.cleaned_data["role"]:
                user.groups.add(self.cleaned_data["role"])
        return user