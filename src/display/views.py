from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def display_scores(request):
    return HttpResponse(f"Results go here")