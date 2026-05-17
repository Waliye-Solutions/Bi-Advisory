from django.urls import reverse
from django.contrib.sitemaps import Sitemap


class AllSitemap(Sitemap):
    priority = 1.0
    changefreq = "daily"
    
    def items(self):
        return ["core:home", "core:about-us", "contacts:contact", "services:services-list"]
    
    def location(self, item): # type: ignore
        return reverse(item)
