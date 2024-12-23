from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from influxdb_client import InfluxDBClient
from influxdb_client.client.query_api import QueryApi
from .forms import LoginForm
import plotly.graph_objs as go

from django.http import HttpResponse

from .models import Device
from django.template import loader
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Temperature
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
from influxdb_client import InfluxDBClient
from PIL import Image 

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from influxdb_client import InfluxDBClient
from influxdb_client.client.query_api import QueryApi
from .forms import LoginForm
from .models import Profile
import plotly.graph_objs as go

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User



def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'home.html')


def temperature_chart(request):
    temperatures = Temperature.objects.all().order_by('timestamp')
    df = pd.DataFrame(list(temperatures.values('value', 'timestamp')))
    
    df = pd.DataFrame(list(temperatures.values()))
  
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    plt.figure(figsize=(10, 5))
    plt.plot(df['timestamp'], df['value'], marker='o')
    plt.title('Temperature Over Time')
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    #return render(request, 'devices/chart.html', {'data': string.decode('utf-8')})
    return render(request, 'devices/chart.html', {'image_base64': image_base64})


def get_devices(request):
    # return HttpResponse('We will see the list of devices here')
    queryset = Device.objects.all()#выбираем список объектов из БД
    template = loader.get_template('devices.html')
    context = {'devices': queryset}
    return HttpResponse(template.render(context, request))

#def get_devices(request):
 #   return HttpResponse('We will see the list of devices here')
def get_device(request, id):
   return HttpResponse(f'We will see our device #{id} here')
   
   
url = "http://localhost:8086"
token = "IAqkdbzq-c0WHBVbkwQGPAHlltrtCtd_zkaMlqMvJ89rFeihEdZgsSaLDZdY9Zw3p9VTEZYjzHwf_PCXPJlqrg=="
org = "smarthome"
bucket = "devices"

# Создание клиента InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)

def get_temperature_data():
    query = f'from(bucket: "{bucket}") |> range(start: -1y) |> filter(fn: (r) => r._measurement == "temperature")'
    result = client.query_api().query(query, org=org)
    
    temperatures = []
    times = []
    
    for table in result:
        for record in table.records:
            temperatures.append(record.get_value())
            times.append(record.get_time())
    
    return times, temperatures

def plot_temperature(request):
    times, temperatures = get_temperature_data()
    
    plt.figure(figsize=(10, 5))
    plt.plot(times, temperatures, marker='o')
    plt.title('Температура за последний час')
    plt.xlabel('Время')
    plt.ylabel('Температура')
    plt.grid(True)
    
    # Сохранение графика в байтовый поток
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Кодирование изображения в base64
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    
    buf.close()
    
    return render(request, 'devices/chart.html', {'image_base64': image_base64})
    
    


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print('username',username)
                if username == 'nik1':
                    return redirect('dashboard')
                if username == 'nik2':
                    return redirect('dashboard2')
                
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
'''
@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    influx_config = profile.influx_config
    INFLUXDB_CONFIG = {
    'url': 'http://localhost:8086',
    'token': "IAqkdbzq-c0WHBVbkwQGPAHlltrtCtd_zkaMlqMvJ89rFeihEdZgsSaLDZdY9Zw3p9VTEZYjzHwf_PCXPJlqrg==",
    'org': 'smarthome',
    'bucket': 'devices',
    }
    client = InfluxDBClient(url=INFLUXDB_CONFIG['url'], token=INFLUXDB_CONFIG['token'], org=INFLUXDB_CONFIG['org'])
    query_api = client.query_api()

    query = f'from(bucket:"{INFLUXDB_CONFIG["bucket"]}") |> range(start: -1m) |> filter(fn: (r) => r._measurement == "temperature")'
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
    
    
@login_required
def dashboard2(request):
    profile = Profile.objects.get(user=request.user)
    influx_config = profile.influx_config
    INFLUXDB_CONFIG = {
    'url': 'http://localhost:8086',
    'token': "IAqkdbzq-c0WHBVbkwQGPAHlltrtCtd_zkaMlqMvJ89rFeihEdZgsSaLDZdY9Zw3p9VTEZYjzHwf_PCXPJlqrg==",
    'org': 'smarthome',
    'bucket': 'devices2',
    }
    client = InfluxDBClient(url=INFLUXDB_CONFIG['url'], token=INFLUXDB_CONFIG['token'], org=INFLUXDB_CONFIG['org'])
    query_api = client.query_api()

    query = f'from(bucket:"{INFLUXDB_CONFIG["bucket"]}") |> range(start: -1m) |> filter(fn: (r) => r._measurement == "temperature")'
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
    
    
    
    
# Найдите всех пользователей, у которых нет профиля
for user in User.objects.filter(profile__isnull=True):
    # Создайте профиль для каждого пользователя
    Profile.objects.create(user=user)
    print(f"Profile created for user: {user.username}")
'''
from django.contrib.auth.decorators import login_required, permission_required
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
@permission_required('devices.view_sensor1', raise_exception=True)
def sensor1_chart(request):
    profile = request.user.profile
    influx_config = profile.influx_config
    client = InfluxDBClient(url=influx_config['url'], token=influx_config['token'], org=influx_config['org'])
    query_api = client.query_api()

    query = f'from(bucket:"{influx_config["bucket"]}") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "temperature" and r.sensor == "sensor1")'
    result = query_api.query(org=influx_config['org'], query=query)

    temperatures = []
    timestamps = []
    for table in result:
        for record in table.records:
            temperatures.append(record.get_value())
            timestamps.append(record.get_time())

    fig = go.Figure(data=go.Scatter(x=timestamps, y=temperatures, mode='lines'))
    graph = fig.to_html(full_html=False, default_height=500, default_width=700)

    return render(request, 'sensor1_chart.html', {'graph': graph})

@login_required
@permission_required('devices.view_sensor2', raise_exception=True)
def sensor2_chart(request):
    profile = request.user.profile
    influx_config = profile.influx_config
    client = InfluxDBClient(url=influx_config['url'], token=influx_config['token'], org=influx_config['org'])
    query_api = client.query_api()

    query = f'from(bucket:"{influx_config["bucket"]}") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "temperature" and r.sensor == "sensor2")'
    result = query_api.query(org=influx_config['org'], query=query)

    temperatures = []
    timestamps = []
    for table in result:
        for record in table.records:
            temperatures.append(record.get_value())
            timestamps.append(record.get_time())

    fig = go.Figure(data=go.Scatter(x=timestamps, y=temperatures, mode='lines'))
    graph = fig.to_html(full_html=False, default_height=500, default_width=700)

    return render(request, 'sensor2_chart.html', {'graph': graph})
    
    




    
    
