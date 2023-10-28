from json import JSONDecodeError

from django.shortcuts import render, redirect
from .models import User, Order, SatelliteModel
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
import os
import datetime
from .mathutils import calculate
from django.http import HttpResponse, HttpResponseForbidden
import json


def now():
    offset = datetime.timezone(datetime.timedelta(hours=3))
    return datetime.datetime.now(offset)


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
                                               "current_time": now(),
                                               'api_key': os.getenv('API_KEY'), 'new_id': new_id})


@login_required(login_url='/auth')
def post(request):
    if request.method == 'POST':
        try:
            is_map = request.POST['is_map']
            if is_map == 'true':
                coordinates = list(map(float, request.POST['points'].split(',')))
                points = []
                for i in range(1, len(coordinates), 2):
                    points.append((coordinates[i - 1], coordinates[i]))
            else:
                points = json.loads(request.POST['textarea'])['coordinates'][0]
            name = request.POST['name']
            method = request.POST['method']
            resolution = request.POST['resolution']
            calculated_time = calculate(points)
            date = now() + datetime.timedelta(minutes=calculated_time)
            Order.objects.create(
                user=request.user, name=name, points=points, date=date,
                method=method, resolution=resolution, is_cancelled=calculated_time == -1)
        except JSONDecodeError:
            Order.objects.create(
                user=request.user, name='Неверный формат geoJSON', points='none', date=now(),
                method='none', resolution='none', is_cancelled=True)
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


def get_satellites_json(request):
    data = list(map(lambda x: {
        'x': x.s,
        't': x.t,
        'view_angle': x.view_angle
    }, SatelliteModel.objects.all()))
    return HttpResponse(json.dumps({'result': data}), content_type="application/json")


def logout_page(request):
    logout(request)
    return redirect('/')

