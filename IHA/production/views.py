from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from .models import WingPart, BodyPart, AvionicsPart, TailPart, AirCraft
from .forms import WingPartForm, BodyPartForm, AirCraftForm, TailPartForm, AvionicsPartForm
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
# Create your views here.




def index(request):
    return render(request, 'production/index.html')


# List parts view to show the parts created
def list_parts(request):
    employee = request.user.employee_profile
    
    if employee.team == 'kanat':
        parts = WingPart.objects.all()
    elif employee.team == 'govde':
        parts = BodyPart.objects.all()
    elif employee.team == 'kuyruk':
        parts = TailPart.objects.all()
    elif employee.team == 'aviyonik':
        parts = AvionicsPart.objects.all()
    else:
        messages.error(request, "Bu islemi yapabilmek için yetkili degilsiniz.")
        return redirect('index')

    return render(request, 'production/list_parts.html', {'parts': parts})

# View for producing parts
def produce_parts(request):
    # Check the user’s team to display the appropriate form
    if not request.user.is_authenticated:
        messages.error(request, "Bu sayfaya erisebilmek icin giris yapmaniz gerekir.")
        return redirect('login')

    employee = request.user.employee_profile  

    if employee.team == 'kanat':
        form = WingPartForm()
    elif employee.team == 'govde':
        form = BodyPartForm()
    elif employee.team == 'kuyruk':
        form = TailPartForm()
    elif employee.team == 'aviyonik':
        form = AvionicsPartForm()
    else:
        messages.error(request, "Bu islemi yapabilmek için yetkili degilsiniz.")
        return redirect('index')
    
    return render(request, 'production/produce_parts.html', {'form': form})


# Helper function to check if the user is in the assembly team
def is_assembly_team(user):
    return user.employee_profile.team == "montaj"


@login_required
@user_passes_test(is_assembly_team, login_url="login")
def assemble_and_view_drones(request):
    if request.method == "POST":
        form = AirCraftForm(request.POST)
        if form.is_valid():
            aircraft = form.save()
            messages.success(request, f"'{aircraft.aircraftname}' adli ucak basari ile olusturuldu.")
            return redirect("assemble_and_view_drones")
        else:
            messages.error(request, "ucak uretirken hata meydana geldi.")
    else:
        form = AirCraftForm()

    # Get all existing aircraft objects
    aircrafts = AirCraft.objects.all()

    context = {
        "form": form,
        "aircrafts": aircrafts,
    }
    return render(request, "production/assemble_and_view_drones.html", context)


def delete_part(request, part_id):
    # Get the user's team
    user_team = request.user.employee_profile.team
    part_model = None

    # Determine the correct model based on the team
    if user_team == 'kanat':
        part_model = WingPart
    elif user_team == 'govde':
        part_model = BodyPart
    elif user_team == 'kuyruk':
        part_model = TailPart
    elif user_team == 'aviyonik':
        part_model = AvionicsPart

    if part_model is None:
        return HttpResponseForbidden("Bu parcayi silmek için yetkin yok.")

    # Get the part object and check if it exists
    part = get_object_or_404(part_model, pk=part_id)

    # Delete the part
    part.delete()

    # Redirect to the parts listing page
    return redirect('listParts')




# Functions for adding parts for each team
def add_wing_part(request):
    if request.method == 'POST' and request.user.has_perm('production.add_wingpart'):
        form = WingPartForm(request.POST)
        if form.is_valid():
            part = form.save()
            messages.success(request, "Kanat Parcasi basari ile eklendi.")
            return redirect('listParts')
        else:
            messages.error(request, "Kanat Parcasi eklenirken bir soun olustu.")
    else:
        messages.error(request, "Kanat parcasi ekleme yetkiniz yok.")
        return redirect('index')

def add_body_part(request):
    if request.method == 'POST' and request.user.has_perm('production.add_bodypart'):
        form = BodyPartForm(request.POST)
        if form.is_valid():
            part = form.save()
            messages.success(request, "Govde Parcasi basari ile eklendi.")
            return redirect('listParts')
        else:
            messages.error(request, "Govde Parcasi eklenirken bir soun olustu.")
    else:
        messages.error(request, "Govde parcasi ekleme yetkiniz yok.")
        return redirect('index')

def add_tail_part(request):
    if request.method == 'POST' and request.user.has_perm('production.add_tailpart'):
        form = TailPartForm(request.POST)
        if form.is_valid():
            part = form.save()
            messages.success(request, "Kuyruk Parcasi basari ile eklendi.")
            return redirect('listParts')
        else:
            messages.error(request, "Kuyruk Parcasi eklenirken bir soun olustu.")
    else:
        messages.error(request, "Kuyruk parcasi ekleme yetkiniz yok.")
        return redirect('index')

def add_avionik_part(request):
    if request.method == 'POST' and request.user.has_perm('production.add_avionicspart'):
        form = AvionicsPartForm(request.POST)
        if form.is_valid():
            part = form.save()
            messages.success(request, "Aviyonik Parcasi basari ile eklendi.")
            return redirect('listParts')
        else:
            messages.error(request, "Aviyonik Parcasi eklenirken bir soun olustu.")
    else:
        messages.error(request, "Aviyonik parcasi ekleme yetkiniz yok.")
        return redirect('index')
    





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