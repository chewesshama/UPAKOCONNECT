from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.users.models import CustomUser
from apps.ariseclinic.models import Patient, Baby, VisitRecord
from apps.globalfellowship.models import FellowshipMember
from apps.complaints.models import Complaint, Remark

# Define groups and what models they manage
GROUP_PERMISSIONS = {
    "Apostle": {
        "models": [CustomUser, Patient, Baby, VisitRecord, FellowshipMember, Complaint, Remark],
        "all_perms": True,
    },
    "Pastor": {
        "models": [CustomUser, Patient, Baby, VisitRecord, FellowshipMember, Complaint, Remark],
        "all_perms": True,
    },
    "Admin": {
        "models": [CustomUser, Patient, Baby, VisitRecord, FellowshipMember, Complaint, Remark],
        "all_perms": True,
    },
    "Doctor": {
        "models": [Patient, Baby, VisitRecord],
        "add_only": [Complaint],
    },
    "Nurse": {
        "models": [Patient, Baby, VisitRecord],
        "add_only": [Complaint],
    },
    "Mapokezi": {
        "models": [FellowshipMember],
        "add_only": [Complaint],
    },
}


@receiver(post_save, sender=CustomUser)
def assign_user_to_group(sender, instance, created, **kwargs):
    if created and instance.role:
        group = instance.role
        group.user_set.add(instance)


@receiver(post_save, sender=Group)
def assign_permissions_to_group(sender, instance, created, **kwargs):
    name = instance.name
    if name in GROUP_PERMISSIONS:
        config = GROUP_PERMISSIONS[name]
        if config.get("all_perms"):
            for model in config["models"]:
                ct = ContentType.objects.get_for_model(model)
                perms = Permission.objects.filter(content_type=ct)
                instance.permissions.set(list(instance.permissions.all()) + list(perms))
        if "add_only" in config:
            for model in config["add_only"]:
                ct = ContentType.objects.get_for_model(model)
                add_perm = Permission.objects.get(content_type=ct, codename=f"add_{model._meta.model_name}")
                instance.permissions.add(add_perm)
