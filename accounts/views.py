from django.shortcuts import render
from django.views import generic

# Create your views here.

class EmailConfirmView(generic.TemplateView):
    template_name = 'confirm-email.html'