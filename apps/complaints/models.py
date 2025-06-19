from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from mtaa import districts
from apps.users.models import CustomUser


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

STATUS_CHOICES = (
    ("Opened", "Opened"),
    ("Forwarded", "Forwarded"),
    ("Closed", "Closed"),
)

class Complaint(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    complainant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    attachments = models.FileField(upload_to='complaint_attachments/', blank=True, null=True)
    targeted_department = models.ForeignKey(Department, related_name="complaint_department", on_delete=models.CASCADE)
    targeted_personnel = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="complaints_targeted"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Opened")
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    department_history = models.ManyToManyField(Department, through='DepartmentHistory', related_name="history", blank=True)

    class Meta:
        ordering = ['-date_added']

    def save(self, *args, **kwargs):
        if self.pk is not None:
            original_complaint = Complaint.objects.get(pk=self.pk)
            if self.status != original_complaint.status:
                DepartmentHistory.objects.create(
                    complaint=self,
                    department=self.targeted_department,
                    status=self.status
                )

        super(Complaint, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title},  by  {self.complainant}"


class Remark(models.Model):
    respondent = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name="remarks")
    content = models.TextField()
    attachments = models.FileField(upload_to='remark_attachments/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Opened")
    remark_targeted_personnel = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="remark_target", default=1
    )
    remark_targeted_department = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.status == "Forwarded":
            self.complaint.targeted_department = self.remark_targeted_department
            self.complaint.status = self.status
            self.complaint.save()
        super(Remark, self).save(*args, **kwargs)

    def __str__(self):
        return f"Remark for Complaint {self.complaint.title}"

class DepartmentHistory(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Opened")

    def __str__(self):
        return f"{self.status} ({self.department})"
