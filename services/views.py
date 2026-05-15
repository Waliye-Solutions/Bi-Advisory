from django.http import Http404
from django.shortcuts import render

from services.models import Service


def services_list_view(request):
    services = Service.objects.all()
    context = {
        "services": services,
        "services_page_is_active": True,
    }
    template_name = "services/services_list.html"
    return render(request, template_name, context)


def service_detail_view(request, service_id):
    try:
        service = Service.objects.get(pk=service_id)
    except Service.DoesNotExist:
        raise Http404
    
    context = {
        "service": service,
        "other_services": Service.objects.only("name").exclude(pk=service.pk),
        "services_page_is_active": True,
    }
    template_name = "services/service_detail.html"
    return render(request, template_name, context)
