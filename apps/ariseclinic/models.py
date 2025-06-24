from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
#from mtaa import tanzania
from django.conf import settings
from apps.core.utils import get_regions


DELIVERY_METHODS = [
    ("normal", "Normal Delivery"),
    ("cesarean", "Cesarean Section"),
    ("induced", "Induced"),
]

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    weeks_of_pregnancy = models.PositiveIntegerField()
    expected_delivery_date = models.DateField()
    is_active_pregnancy = models.BooleanField(default=True)
    delivery_place_region = models.CharField(max_length=100, choices=get_regions())
    delivery_place_district = models.CharField(max_length=100)
    nationality = CountryField(blank_label="(Select Country)", default='TZ')
    phone_number = PhoneNumberField(null=True, blank=True)
    delivery_method = models.CharField(max_length=50, choices=DELIVERY_METHODS)
    delivery_instructions = models.TextField(blank=True)
    attended_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role__name__in': ['Doctor', 'Nurse']})
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Patient"
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name

class Baby(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mother = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="babies")
    gender = models.CharField(max_length=10, choices=[("M", "Male"), ("F", "Female")])
    dob = models.DateField()
    twins_status = models.CharField(max_length=10, choices=[("single", "Single"), ("double", "Twins"), ("triple", "Triplets")])
    weight = models.DecimalField(max_digits=4, decimal_places=2)
    health_status = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=100, choices=get_regions())
    district = models.CharField(max_length=100)
    ward = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Baby"
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name


class VisitRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    visit_date = models.DateField(default=timezone.now)
    vitals = models.TextField()
    notes = models.TextField()
    seen_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, limit_choices_to={'role__name__in': ['Doctor', 'Nurse']})
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = "VisitRecord"
        ordering = ['-created_at']

    def __str__(self):
        return self.notes