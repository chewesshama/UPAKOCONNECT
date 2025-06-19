from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
)
from multiupload.fields import MultiMediaField
# from multiupload.widgets import MultiFileInput
from .models import Remark, Department, Complaint
from apps.users.models import CustomUser
from django.contrib.auth.models import Group
#from mtaa import tanzania, districts


class DepartmentForm(forms.ModelForm):
    name = forms.CharField(
        label="name", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    description = forms.CharField(
        label="description",
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Department
        fields = [
            "name",
            "description",
        ]


class CEORegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="firstname", widget=forms.TextInput)

    last_name = forms.CharField(label="lastname", widget=forms.TextInput)

    username = forms.CharField(
        label="username", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        label="email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        label="Department",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Position",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "group",
            "department",
            "password1",
            "password2",
        ]


class HODRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label="firstname", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(
        label="lastname", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    username = forms.CharField(
        label="username", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        label="email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
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
        ]


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    username.label = "Username"
    username.label_classes = ["text-danger"]


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        label="firstname", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(
        label="lastname", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    username = forms.CharField(
        label="username", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        label="email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    profile_picture = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    region = forms.CharField(
        label="Region",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    district = forms.CharField(
        label="District",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    phone_number = forms.CharField(
        label="phone number", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "profile_picture",
            "phone_number",
            "region",
            "district",
        )


class SearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Search...",
                "data-toggle": "tooltip",
                "title": "Enter your search here",
            }
        ),
        label="Search",
    )


class PasswordChangeCustomForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="old Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = CustomUser
        fields = ["old_password", "new_password1", "new_password2"]


class MultiFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", forms.ClearableFileInput(attrs={"multiple": True}))
        super().__init__(*args, **kwargs)


class AddComplaintForm(forms.ModelForm):
    title = forms.CharField(
        label="title",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    description = forms.CharField(
        label="description",
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )

    attachments = MultiMediaField(
        min_num=1,
        max_num=5,
        max_file_size=1024 * 1024 * 5,
        media_type="image",  # 'audio', 'video' or 'image'
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        required=False,
    )

    targeted_personnel = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    targeted_department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        label="Department",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    STATUS_CHOICES = (
        ("Opened", "Opened"),
        ("Forwarded", "Forwarded"),
        ("Closed", "Closed"),
    )

    class Meta:
        model = Complaint
        fields = [
            "title",
            "description",
            "attachments",
            "targeted_department",
            "targeted_personnel",
        ]


class UpdateComplaintForm(forms.ModelForm):
    title = forms.CharField(
        label="title",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    description = forms.CharField(
        label="description",
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Complaint
        fields = [
            "title",
            "description",
        ]


class AddRemarkForm(forms.ModelForm):
    complaint = forms.ModelChoiceField(
        queryset=Complaint.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    content = forms.CharField(
        label="description", widget=forms.Textarea(attrs={"class": "form-control"})
    )

    attachments = MultiMediaField(
        min_num=1,
        max_num=5,
        max_file_size=1024 * 1024 * 5,
        media_type="image",  # 'audio', 'video' or 'image'
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        required = False,
    )

    remark_targeted_personnel = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        label="Forward / respond to",
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    remark_targeted_department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        label="Department",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    STATUS_CHOICES = (
        ("Forwarded", "Forwarded"),
        ("Closed", "Closed"),
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        label="status",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Remark
        fields = [
            "complaint",
            "content",
            "attachments",
            "remark_targeted_department",
            "remark_targeted_personnel",
            "status",
        ]


class UpdateRemarkForm(forms.ModelForm):
    content = forms.CharField(
        label="description", widget=forms.Textarea(attrs={"class": "form-control"})
    )

    remark_targeted_personnel = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        label="Forward / respond to",
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    remark_targeted_department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        label="Department",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    STATUS_CHOICES = (
        ("Forwarded", "Forwarded"),
        ("Closed", "Closed"),
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        label="status",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Remark
        fields = [
            "content",
            "remark_targeted_department",
            "remark_targeted_personnel",
            "status",
        ]
