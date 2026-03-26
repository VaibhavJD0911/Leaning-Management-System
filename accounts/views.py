from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')

        return render(request, 'accounts/login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.roles = role   # ✅ FIXED
        user.save()

        login(request, user)
        return redirect('dashboard')

    return render(request, 'accounts/register.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
