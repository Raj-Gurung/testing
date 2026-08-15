from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from training.models import Profile


def home_view(request):
    return render(request, 'home.html')


def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    return render(request, 'contact.html')


def guidelines_view(request):
    return render(request, 'guidelines.html')


@login_required(login_url='/login/')
def quiz_view(request):
    return render(request, 'quiz.html')


@login_required(login_url='/login/')
def crane_view(request):
    return render(request, 'crane.html')


@login_required(login_url='/login/')
def forklift_view(request):
    return render(request, 'forklift.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not password:
            error = "Please enter both username and password."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif User.objects.filter(username=username).exists():
            error = f"Username '{username}' is already taken."
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            messages.success(request, f"Account created successfully! Welcome, {username}.")
            return redirect('home')

    return render(request, 'signup.html', {'error': error})


def login_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile') and request.user.profile.role == 'admin':
            return redirect('admin_dashboard')
        return redirect('home')

    error = None
    next_url = request.GET.get('next', '') or request.POST.get('next', '')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")

            if next_url and next_url.startswith('/'):
                return redirect(next_url)

            if hasattr(user, 'profile') and user.profile.role == 'admin':
                return redirect('admin_dashboard')
            return redirect('home')
        else:
            error = "Invalid username or password."

    return render(request, 'login.html', {'error': error, 'next': next_url})


def logout_view(request):
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect('login')


@login_required(login_url='/login/')
def admin_dashboard_view(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'admin':
        messages.error(request, "Access restricted to administrators.")
        return redirect('home')
    return render(request, 'admin_dashboard.html')
