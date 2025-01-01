from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import WingPart, BodyPart, AvionicsPart, TailPart, AirCraft
from .forms import WingPartForm, BodyPartForm, AirCraftForm, TailPartForm, AvionicsPartForm
from functools import wraps
from django.http import JsonResponse
# Create your views here.




def index(request):
    """route user to home page"""
    return render(request, 'production/index.html')

def login_required_with_message(view_func):
    """
    Decorator to ensure the user is authenticated before accessing the view.

    If the user is not authenticated:
    - Displays an error message.
    - Redirects to the login page for standard requests.
    - For AJAX requests, returns a JSON response with a 401 Unauthorized status.

    Args:
        view_func (function): The view function to be decorated.

    Returns:
        function: The wrapped view function.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Bu sayfaya erismek icin giris yapmaniz gerekiyor.")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # For AJAX requests, return a JSON response with status 401
                return JsonResponse({"error": "Unauthorized. Please log in."}, status=401)
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def user_team_required(team_name):
    """
    Decorator to restrict access to views based on the user's team.

    Ensures that the user belongs to the specified team:
    - Displays an error message and redirects to the index page for unauthorized users.
    - For AJAX requests, returns a JSON response with appropriate status codes:
      - 403 Forbidden for unauthorized users.
      - 400 Bad Request if the employee profile is not found.

    Args:
        team_name (str): The required team name.

    Returns:
        function: A decorator that wraps the view function.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            try:
                employee = request.user.employee_profile
                if employee.team != team_name:
                    messages.error(request, "Bu sayfaya erismek icin yetkili degilsiniz.")
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # For AJAX requests, return a JSON response with status 403
                        return JsonResponse({"error": "Forbidden. You lack the necessary team permissions."}, status=403)
                    return redirect("index")
            except AttributeError:
                messages.error(request, "Herhangi bir takima ait degilsiniz.")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # For AJAX requests, return a JSON response with status 400
                    return JsonResponse({"error": "Bad Request. Employee profile not found."}, status=400)
                return redirect("index")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# List parts view to show the parts created
@login_required_with_message
def list_parts(request):
    """
    View for listing parts based on the user's team.

    Checks the user's team affiliation and retrieves the corresponding parts:
    - 'kanat': Retrieves WingPart objects.
    - 'govde': Retrieves BodyPart objects.
    - 'kuyruk': Retrieves TailPart objects.
    - 'aviyonik': Retrieves AvionicsPart objects.
    - If the user is not in a recognized team, displays an error and redirects to the index page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the list of parts for the team or redirects with an error.
    """
    # Check if the user belongs to any team
    try:
        employee = request.user.employee_profile
    except AttributeError:
        messages.error(request, "Hicbir takima ait değilsiniz.")
        return redirect("index")
    
    #determine which team user belongs
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
@login_required_with_message
def produce_parts(request):
    """
    View for rendering the form to produce parts based on the user's team.

    Checks the user's team affiliation and renders the corresponding form:
    - 'kanat': Displays the WingPartForm.
    - 'govde': Displays the BodyPartForm.
    - 'kuyruk': Displays the TailPartForm.
    - 'aviyonik': Displays the AvionicsPartForm.
    - If the user is not in a recognized team, displays an error and redirects to the index page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the form for part production or redirects with an error.
    """
    # Check if the user belongs to any team
    try:
        employee = request.user.employee_profile
    except AttributeError:
        messages.error(request, "Hicbir takima ait değilsiniz.")
        return redirect("index")
    
    #determine which team user belongs
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




@login_required_with_message
@user_team_required("montaj")
def assemble_and_view_drones(request):
    """
    View for assembling and viewing aircraft.

    Handles aircraft creation using a form. If the form is submitted and valid, 
    the aircraft is saved and the user is redirected back to the same page. 
    Displays all existing aircraft objects to the user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the assembly and viewing page.
    """
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


@login_required_with_message
def delete_part(request, part_id):
    """
    View for deleting a part based on the user's team.

    Determines the correct model to delete based on the user's team. 
    If the user is not authorized, an error message is displayed. 

    Args:
        request (HttpRequest): The HTTP request object.
        part_id (int): The ID of the part to be deleted.

    Returns:
        HttpResponse: Redirects to the parts listing page or an error message.
    """
    # Check if the user belongs to any team.
    try:
        user_team = request.user.employee_profile.team
    except AttributeError:
        messages.error(request, "Hicbir takima ait değilsiniz.")
        return redirect("index")
    
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
@login_required_with_message
@user_team_required("kanat")
def add_wing_part(request):
    """
    view to add parts based on the team and form class.

    Args:
        request (HttpRequest): The HTTP request object.
        team_name (str): The name of the team that has access to this view.
        form_class (Form): The form class used for creating the part.
        success_message (str): The success message to display upon successful creation.

    Returns:
        HttpResponse: Redirects to the parts listing page or an error message.
    """
    if request.method == 'POST':
        form = WingPartForm(request.POST)
        if form.is_valid():
            part = form.save()
            messages.success(request, "Kanat Parcasi basari ile eklendi.")
            return redirect('listParts')
        else:
            messages.error(request, "Kanat Parcasi eklenirken bir soun olustu.")
            return redirect('produceParts')
    else:
        return redirect('index')

@login_required_with_message
@user_team_required("govde")
def add_body_part(request):
    if request.method == 'POST':
        form = BodyPartForm(request.POST)
        if form.is_valid():
            part = form.save()
            messages.success(request, "Govde Parcasi basari ile eklendi.")
            return redirect('listParts')
        else:
            messages.error(request, "Govde Parcasi eklenirken bir soun olustu.")
            return redirect('produceParts')
    else:
        return redirect('index')

@login_required_with_message
@user_team_required("kuyruk")
def add_tail_part(request):
    if request.method == 'POST':
        form = TailPartForm(request.POST)
        if form.is_valid():
            part = form.save()
            messages.success(request, "Kuyruk Parcasi basari ile eklendi.")
            return redirect('listParts')
        else:
            messages.error(request, "Kuyruk Parcasi eklenirken bir soun olustu.")
    else:
        return redirect('index')

@login_required_with_message
@user_team_required("aviyonik")
def add_avionik_part(request):
    if request.method == 'POST':
        form = AvionicsPartForm(request.POST)
        if form.is_valid():
            part = form.save()
            messages.success(request, "Aviyonik Parcasi basari ile eklendi.")
            return redirect('listParts')
        else:
            messages.error(request, "Aviyonik Parcasi eklenirken bir soun olustu.")
    else:
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