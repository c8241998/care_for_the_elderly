from datetime import time
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from apps.account import models as account_models
from apps.camera import models as camera_models
from apps.volunteer import models as volunteer_models
from apps.elder import models as elder_models
from apps.worker import models as worker_models
from util.json import jsonRes
from django.shortcuts import HttpResponse,render,redirect
import time
from apps.AI.process import manul_load

manul_load()

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            re = account_models.MyUser.objects.get(email=email)
        except account_models.MyUser.DoesNotExist:
            return jsonRes("user_not_found",400)
        re = auth.authenticate( username=email, password=password)
        if re is None:
            return jsonRes("password_incorrect", 401)
        auth.login(request, re)
        return jsonRes("success", 200)

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponse("")
    # return redirect('/landing')

def landing(request):
    return render(request,"login.html")

def home(request):
    user = get_user(request)
    if user.is_anonymous():
        return render(request, 'login.html')
    else:
        return render(request, 'frame.html')

def mainpage(request):
    return render(request,"mainpage.html")

def delete(request):
    pass

def modifyPwd(request):
    if request.method == "POST":
        old_pass = request.POST.get('old_pass')
        new_pass = request.POST.get('new_pass')
        user = get_user(request)
        if user.check_password(old_pass):
            user.set_password(new_pass)
            user.save()
            return jsonRes("success", 200)
        else:
            return jsonRes("密码错误", 403)
    return render(request,"modifyPwd.html")