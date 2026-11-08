from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here.


def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def register_view(request):
    form = RegisterForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')

        # Check for duplicate username
        if Register.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return render(request, 'register.html', {'form': form})

        # Check for duplicate email
        if Register.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use a different email address.")
            return render(request, 'register.html', {'form': form})

        user = form.save(commit=False)
        user.role = "User"
        user.save()
        messages.success(request, "Registration successful! Please login with your credentials.")
        return redirect('login')
    else:
        print(form.errors)
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            if user.role == "Admin":
                return redirect('admin_places')
            return redirect('user_places')
        messages.error(request, "Invalid username or password")
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


# ---------------- ADMIN SIDE ----------------

@login_required
def admin_places(request):
    if request.user.role != "Admin":
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('user_places')
    places = Places.objects.all()
    return render(request, 'admin_places.html', {'places': places})


@login_required
def add_place(request):
    if request.user.role != "Admin":
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('user_places')

    form = PlaceForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Place added successfully")
        return redirect('admin_places')

    return render(request, 'add_edit_place.html', {'form': form, 'title': 'Add Place'})


@login_required
def edit_place(request, pk):
    if request.user.role != "Admin":
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('user_places')

    place = get_object_or_404(Places, id=pk)
    form = PlaceForm(request.POST or None, request.FILES or None, instance=place)
    if form.is_valid():
        form.save()
        messages.success(request, "Place updated successfully")
        return redirect('admin_places')

    return render(request, 'add_edit_place.html', {'form': form, 'title': 'Edit Place'})


@login_required
def delete_place(request, pk):
    if request.user.role == "Admin":
        Places.objects.filter(id=pk).delete()
        messages.success(request, "Place deleted successfully.")
    else:
        messages.error(request, "Access denied. Admin privileges required.")
    return redirect('admin_places')


# ---------------- USER SIDE ----------------

@login_required
def user_places(request):
    places = Places.objects.all()
    search_applied = False

    # Search filters (your existing code)
    if request.GET.get('name'):
        places = places.filter(name__icontains=request.GET.get('name'))
        search_applied = True
    if request.GET.get('location'):
        places = places.filter(location__icontains=request.GET.get('location'))
        search_applied = True
    if request.GET.get('season'):
        places = places.filter(best_season__icontains=request.GET.get('season'))
        search_applied = True
    if request.GET.get('category'):
        places = places.filter(category=request.GET.get('category'))
        search_applied = True

    if search_applied:
        if places.exists():
            messages.info(request, f"Found {places.count()} place(s) matching your search criteria.")
        else:
            messages.warning(request, "No places found matching your search criteria.")

    # Create an empty form just for the category choices
    form = PlaceForm()

    return render(request, 'user_places.html', {
        'places': places,
        'form': form,  # ← Pass the form here!
    })


@login_required
def admin_users(request):
    if request.user.role != "Admin":
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('user_places')

    # Get all users (excluding the current superuser if needed, or include everyone)
    users = Register.objects.filter(is_superuser=False).order_by('-date_joined')

    return render(request, 'admin_users.html', {
        'users': users,
        'total_users': users.count(),
    })