from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),
    #path("<int:id>/", views.get_device, name="device"),
    path('login/', views.login_view, name='login'),
    path('chart/', views.temperature_chart, name='temperature_chart'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard2/', views.dashboard, name='dashboard2'),

    #path('', views.home, name='home'),
    #path('register/', views.register, name='register'),
    #path('login/', views.login_view, name='login'),
    #path('dashboard/', views.dashboard, name='dashboard'),
    #path('sensor1/', views.sensor1_chart, name='sensor1_chart'),
    #path('sensor2/', views.sensor2_chart, name='sensor2_chart'),
]
