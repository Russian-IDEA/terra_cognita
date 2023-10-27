from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
import os


@ensure_csrf_cookie
def home(request):
    error_code = 0
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        to_register = request.POST['toSignUp']
        if to_register == 'true':
            try:
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect('/profile')
            except IntegrityError:
                error_code = 2
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/profile')
            error_code = 1
    return render(request, "main/index.html", {'error_code': error_code})


@login_required(login_url='/')
def profile(request):
    return render(request, "main/profile.html", {'user': request.user.username})


def add(request):
    return render(request, 'main/add.html', {'api_key': os.getenv('API_KEY')})


def logout_page(request):
    logout(request)
    return redirect('/')

