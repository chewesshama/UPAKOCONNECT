from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from apps.users.models import CustomUser
#from mtaa import tanzania
from apps.core.utils import get_regions


class FellowshipMember(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    original_location = CountryField()
    current_location_region = models.CharField(max_length=100, choices=get_regions())
    current_location_district = models.CharField(max_length=100)
    current_location_ward = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=10, choices=[('single', 'Single'), ('married', 'Married')])
    phone_number = PhoneNumberField(null=True, blank=True)
    nationality = CountryField()
    email = models.EmailField()
    date_of_arrival = models.DateField()
    date_of_departure = models.DateField(null=True, blank=True)
    occupation = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=50, blank=True)
    ticket = models.FileField(upload_to='tickets/', blank=True)
    gender = models.CharField(max_length=10, choices=[("M", "Male"), ("F", "Female")])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "FellowshipMember"
        ordering = ['-created_at']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_current_location(self):
        return f"{self.current_location_ward}, {self.current_location_district}, {self.current_location_region}"

    def __str__(self):
        return self.full_name