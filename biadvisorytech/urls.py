from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("summernote/", include("django_summernote.urls")),
    path("hitcount/", include("hitcount.urls", namespace="hitcount")),
    
    # Local apps urls
    path("", include("core.urls", namespace="core")),
    path("contact/", include("contacts.urls", namespace="contacts")),
    path("services/", include("services.urls", namespace="services")),
    path("newsletter/", include("newsletter.urls", namespace="newsletter")),
]
