from django.shortcuts import render

from services.models import Service
from contacts.forms import ContactForm
from testimonials.models import Testimonial


def home_view(request):
    context = {
        "home_page_is_active": True,
        "contact_form": ContactForm(),
        "testimonials": Testimonial.objects.all(),
        "services": Service.objects.all(),
    }
    template_name = "core/home.html"
    return render(request, template_name,  context)



def about_us_view(request):
    best_testimonial = Testimonial.objects.order_by("-stars").first()
    
    context = {
        "about_us_page_is_active": True,
        "best_testimonial": best_testimonial,
    }
    template_name = "core/about_us.html"
    return render(request, template_name,  context)
