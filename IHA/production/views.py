from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
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



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})