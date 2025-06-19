from django.db import models
from django.contrib.auth.models import AbstractUser
from django.apps import apps

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('pastor', 'Pastor'),
        ('member', 'Member'),
        ('visitor', 'Visitor'),
    )
    
    departments = models.ForeignKey(
        'complaints.Department',
        on_delete=models.DO_NOTHING,
        related_name="user_department",
        null=True, blank=True
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", default="default_pic.jpg", blank=True, null=True
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.departments:
            Department = apps.get_model('complaints', 'Department')
            default_department, created = Department.objects.get_or_create(
                name="Default",
                defaults={"description": "Auto-created default department"}
            )
            self.departments = default_department
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
