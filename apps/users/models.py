from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
#from mtaa import tanzania
from apps.core.utils import get_regions


class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    MARITAL_STATUS_CHOICES = (
        ('single', 'Single'),
        ('married', 'Married'),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    
    nationality = CountryField(blank_label="(Select Country)", default='TZ')
    phone_number = PhoneNumberField(null=True, blank=True)

    role = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(
        'complaints.Department',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    region = models.CharField(max_length=100, choices=get_regions(), blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    ward = models.CharField(max_length=100, blank=True, null=True)

    profile_picture = models.ImageField(upload_to="profile_pictures/", default="default_pic.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "CustomUser"
        ordering = ['-created_at']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username
