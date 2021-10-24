from django.shortcuts import render
from django.views.generic import ListView
from .models import User
# Create your views here.
class HomePage(ListView):
    model = User
    template_name = 'base.html'
