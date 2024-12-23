from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='startpage'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('temperature_charts/', views.temperature_charts, name='temperature_charts'),
    path('show_graph1/', views.show_graph1, name='show_graph1'),
    path('show_graph2/', views.show_graph2, name='show_graph2'),
    
   
]

