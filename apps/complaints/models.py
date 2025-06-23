from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Department"
        ordering = ['-created_at']

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

    complainant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True
    )

    targeted_department = models.ForeignKey(
        Department,
        related_name="complaint_department",
        on_delete=models.CASCADE
    )

    targeted_personnel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints_against')

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Opened"
    )

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    department_history = models.ManyToManyField(
        Department,
        through='DepartmentHistory',
        related_name="history",
        blank=True
    )

    class Meta:
        ordering = ['-date_added']

    def save(self, *args, **kwargs):
        if self.pk is not None:
            original = Complaint.objects.get(pk=self.pk)
            if self.status != original.status:
                DepartmentHistory.objects.create(
                    complaint=self,
                    department=self.targeted_department,
                    status=self.status
                )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}, by {self.complainant}"


class ComplaintAttachment(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='complaint_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.complaint.title}"


class Remark(models.Model):
    respondent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )   

    complaint = models.ForeignKey(
        Complaint,
        on_delete=models.CASCADE,
        related_name="remarks"
    )

    content = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Opened"
    )

    remark_targeted_personnel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="remark_target",
        default=None,
        null=True, 
        blank=True
    )

    remark_targeted_department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        default=None,
        null=True, 
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Remark"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.status == "Forwarded":
            self.complaint.targeted_department = self.remark_targeted_department
            self.complaint.status = self.status
            self.complaint.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Remark for Complaint {self.complaint.title}"


class RemarkAttachment(models.Model):
    remark = models.ForeignKey(Remark, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='remark_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for Remark on {self.remark.complaint.title}"

class DepartmentHistory(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Opened")

    def __str__(self):
        return f"{self.status} ({self.department})"

