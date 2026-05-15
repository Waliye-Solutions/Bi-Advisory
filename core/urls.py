from core import views
from django.urls import path

app_name = "core"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("a-propos/", views.about_us_view, name="about-us"),
]
