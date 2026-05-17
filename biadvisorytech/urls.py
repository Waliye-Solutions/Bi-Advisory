from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.views.static import serve
from django.contrib.sitemaps import views
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from core.sitemaps import AllSitemap


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



# Serving static and media files (adding them to project URL)
urlpatterns += static(settings.STATIC_URL, serve, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, serve, document_root=settings.MEDIA_ROOT)




# Sitemap URLs
urlpatterns += [
    path("robots.txt/", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("sitemap.xml/", views.sitemap,
        {
            "sitemaps": {
                "core": AllSitemap,
            },
        },
        name="django.contrib.sitemaps.views.sitemap"
    ),
]
