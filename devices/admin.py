from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

# импортировали определение Device из models.py
from .models import Device

from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
# включить управление устройствами в интерфейсе администратора
admin.site.register(Device)

admin.site.register(CustomUser, UserAdmin)
