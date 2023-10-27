from django.shortcuts import render, redirect
from .models import User, Order
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
import os
import datetime
from random import randint


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
    if request.method == 'POST':
        name = request.POST['name']
        points = list(map(float, request.POST['points'].split(',')))
        date = datetime.datetime.now() + datetime.timedelta(seconds=randint(1_000, 1_000_000))
        Order.objects.create(
            user=request.user, name=name, x1=points[0], y1=points[1], x2=points[2], y2=points[3], date=date)
    orders = Order.objects.all().order_by('id').reverse()
    return render(request, "main/profile.html", {'user': request.user.username, 'orders': orders,
                                                 "current_time": datetime.datetime.now()})


def add(request):
    return render(request, 'main/add.html', {'api_key': os.getenv('API_KEY')})


def logout_page(request):
    logout(request)
    return redirect('/')

