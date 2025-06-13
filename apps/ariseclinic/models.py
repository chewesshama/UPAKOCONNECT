#from django.utils import timezone
#from django.core.exceptions import ValidationError
#from django.db import models
#from django.contrib.auth.models import AbstractUser

#class User(AbstractUser):
#    phone_number = models.CharField(max_length=15, blank=True, null=True)
#    region = models.CharField(max_length=100, blank=True, null=True)
#    district = models.CharField(
#        max_length=100, blank=True
#    )
#
#    def save(self, *args, **kwargs):
#        super(User, self).save(*args, **kwargs)
#
#    def __str__(self):
#        return self.username
