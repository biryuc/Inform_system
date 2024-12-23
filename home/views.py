from django.shortcuts import render

# Create your views here.

from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from influxdb_client import InfluxDBClient
import plotly.graph_objs as go
from django.contrib.auth.models import User
url_db = "http://localhost:8086"
token_db = "IAqkdbzq-c0WHBVbkwQGPAHlltrtCtd_zkaMlqMvJ89rFeihEdZgsSaLDZdY9Zw3p9VTEZYjzHwf_PCXPJlqrg=="
org_db = "smarthome"
bucket_db = "devices"


def home(request):
    
    if not request.user.is_authenticated:
        return redirect('home:login')
    return render(request, 'home.html')
    

@login_required  # Требуется авторизация для доступа к странице
def temperature_charts(request):

    # Здесь можно добавить логику для получения данных о температурах
    
    
    #temperature_data = get_temperature_data()

    # Проверка логина пользователя
    if request.user.username == 'user1':
        temperature_data = [
        {"sensor": "Sensor 1", "temperature": 22.5},
        ]
    else:
        temperature_data = [
        {"sensor": "Sensor 1","number": "1"},
        {"sensor": "Sensor 2","number": "2"},
       
        ]
        
        
    return render(request, 'temperature_charts.html', {'temperature_data': temperature_data})
    
    
def show_graph1(request):

    #profile = Profile.objects.get(user=request.user)
    #influx_config = profile.influx_config
    INFLUXDB_CONFIG = {
    'url': 'http://localhost:8086',
    'token': "IAqkdbzq-c0WHBVbkwQGPAHlltrtCtd_zkaMlqMvJ89rFeihEdZgsSaLDZdY9Zw3p9VTEZYjzHwf_PCXPJlqrg==",
    'org': 'smarthome',
    'bucket': 'devices',
    }
    client = InfluxDBClient(url=INFLUXDB_CONFIG['url'], token=INFLUXDB_CONFIG['token'], org=INFLUXDB_CONFIG['org'])
    query_api = client.query_api()

    query = f'from(bucket:"{INFLUXDB_CONFIG["bucket"]}") |> range(start: -1y) |> filter(fn: (r) => r._measurement == "temperature")'
    result = query_api.query(org=INFLUXDB_CONFIG['org'], query=query)

    temperatures = []
    timestamps = []
    for table in result:
        for record in table.records:
            temperatures.append(record.get_value())
            timestamps.append(record.get_time())

    fig = go.Figure(data=go.Scatter(x=timestamps, y=temperatures, mode='lines'))
    graph = fig.to_html(full_html=False, default_height=500, default_width=700)

    return render(request, 'dashboard.html', {'graph': graph})
    
def show_graph2(request):

    #profile = Profile.objects.get(user=request.user)
    #influx_config = profile.influx_config
    INFLUXDB_CONFIG = {
    'url': 'http://localhost:8086',
    'token': "IAqkdbzq-c0WHBVbkwQGPAHlltrtCtd_zkaMlqMvJ89rFeihEdZgsSaLDZdY9Zw3p9VTEZYjzHwf_PCXPJlqrg==",
    'org': 'smarthome',
    'bucket': 'devices2',
    }
    client = InfluxDBClient(url=INFLUXDB_CONFIG['url'], token=INFLUXDB_CONFIG['token'], org=INFLUXDB_CONFIG['org'])
    query_api = client.query_api()

    query = f'from(bucket:"{INFLUXDB_CONFIG["bucket"]}") |> range(start: -1y) |> filter(fn: (r) => r._measurement == "temperature")'
    result = query_api.query(org=INFLUXDB_CONFIG['org'], query=query)

    temperatures = []
    timestamps = []
    for table in result:
        for record in table.records:
            temperatures.append(record.get_value())
            timestamps.append(record.get_time())

    fig = go.Figure(data=go.Scatter(x=timestamps, y=temperatures, mode='lines'))
    graph = fig.to_html(full_html=False, default_height=500, default_width=700)

    return render(request, 'dashboard.html', {'graph': graph})

    
def register(request):

    if request.user.is_authenticated:
        return redirect('home:temperature_charts')  # Перенаправление на страницу с графиками
        
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate form data
        if password1 != password2:
            messages.error(request, "Пароли не совпадают.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Имя пользователя уже занято.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email уже зарегистрирован.")
        else:
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            print(f"Пользователь {username} успешно создан!")  # Отладочное сообщение
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('home:login')  # Redirect to login page

    return render(request, 'home.html')
    
    
def user_login(request):
    
    #if request.user.is_authenticated:
       # return redirect('home:temperature_charts')  # Перенаправление на страницу с графиками
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Аутентификация пользователя
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Вы успешно вошли в систему!")
            return redirect('home:temperature_charts')  # Перенаправление на страницу с графиками
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")

    return render(request, 'login.html')
    
    

