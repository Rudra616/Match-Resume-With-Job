from django.shortcuts import render

# Create your views here.
# app/views.py

from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello from home view")
