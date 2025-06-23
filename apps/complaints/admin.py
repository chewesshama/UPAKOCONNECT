from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Complaint,
    Department,
    Remark,
    DepartmentHistory,
    ComplaintAttachment,
    RemarkAttachment
)

admin.site.register(Department)
admin.site.register(Complaint)
admin.site.register(Remark)
admin.site.register(DepartmentHistory)
admin.site.register(ComplaintAttachment)
admin.site.register(RemarkAttachment)


#admin.site.site_header = "CMS admin area"
#admin.site.site_title = "CMS admin site"
#admin.site.site_url = 'http://127.0.0.1:8000/home/'
