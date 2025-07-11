from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", include("apps.core.urls"), name="core"),
    path("clinic/", include("apps.ariseclinic.urls"), name="clinic"),
    path("global/", include("apps.globalfellowship.urls"), name="global"),
    path("accounts/", include("apps.users.urls"), name="users"),
    path("complaints/", include("apps.complaints.urls"), name="complaints"),
    path('admin/', admin.site.urls),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

