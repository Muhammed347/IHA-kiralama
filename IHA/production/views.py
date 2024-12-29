from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return render(request, 'production/index.html')


def list_parts(request):
    return render(request, 'production/list_parts.html')

def create_parts(request):
    return render(request, 'production/produce_parts.html')

def assemble_and_view_drones(request):
    return render(request, 'production/assemble_and_view_drones.html')