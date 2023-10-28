from django.shortcuts import render, redirect
from .models import User, Order
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
import os
import datetime
from .mathutils import calculate_time
from django.http import HttpResponse, HttpResponseForbidden


@ensure_csrf_cookie
def auth(request):
    error_code = 0
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        to_register = request.POST['toSignUp']
        if to_register == 'true':
            try:
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect('/')
            except IntegrityError:
                error_code = 2
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            error_code = 1
    return render(request, "main/auth.html", {'error_code': error_code})


@login_required(login_url='/auth')
def home(request):
    orders = request.user.order_set.order_by('id').reverse()
    try:
        new_id = list(Order.objects.all())[-1].id + 1
    except IndexError:
        new_id = 1
    return render(request, "main/index.html", {'user': request.user.username, 'orders': orders,
                                                 "current_time": datetime.datetime.now(),
                                               'api_key': os.getenv('API_KEY'), 'new_id': new_id})


@login_required(login_url='/auth')
def post(request):
    if request.method == 'POST':
        name = request.POST['name']
        coordinates = list(map(float, request.POST['points'].split(',')))
        method = request.POST['method']
        resolution = request.POST['resolution']
        points = []
        for i in range(1, len(coordinates), 2):
            points.append((coordinates[i-1], coordinates[i]))
        calculated_time = calculate_time(points)
        date = datetime.datetime.now() + datetime.timedelta(minutes=calculated_time)
        Order.objects.create(
            user=request.user, name=name, points=points, date=date,
            method=method, resolution=resolution, is_cancelled=calculated_time == -1)
    return redirect('/')


@login_required(login_url='/auth')
def download(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.user == request.user:
        photo = order.photo
        response = HttpResponse(photo.file, content_type='application/force-download')
        response['Content-Disposition'] = f'attachment; filename="{photo.file.name}"'
        return response
    return HttpResponseForbidden()


def logout_page(request):
    logout(request)
    return redirect('/')

