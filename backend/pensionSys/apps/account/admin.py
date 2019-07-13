from django.contrib import admin
from .models import MyUser,MyUserManager
from django.contrib.auth.admin import UserAdmin
# admin.site.register(MyUser, MyUserManager)
# Register your models here.
admin.site.register(MyUser)