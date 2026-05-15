from services import views
from django.urls import path

app_name = "services"

urlpatterns = [
    path("", views.services_list_view, name="services-list"),
    path("p-<int:service_id>/", views.service_detail_view, name="services-detail"),
]
