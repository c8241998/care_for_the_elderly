from django.shortcuts import render
from django.http import StreamingHttpResponse,HttpResponse
from .models import stranger_log,emotion_log,fall_log,interaction_log,area_log
from django.views.decorators.csrf import csrf_exempt
from util.json import *
from util.conf import conf
from . import models

def page(request):
    conf_json = conf()
    ip1 = conf_json['ip1']
    ip2 = conf_json['ip2']
    return render(request,"camera.html",context={
        "ip1":ip1,
        "ip2":ip2
    })

def emotionpage(request):
    return render(request,"emotion.html")

@csrf_exempt
def emotioninit(request):
    try:
        emotion_logs = models.emotion_log.objects.all().order_by('id').reverse()
        list={}
        for i,emotion_log in enumerate(emotion_logs):
            list[i]=emotion_log.__str__()
        return jsonRes("success", 200,list)
    except Exception as e:
        print(e)
        return jsonRes("fail",400)

def fallpage(request):
    return render(request,"fall.html")

@csrf_exempt
def fallinit(request):
    try:
        fall_logs = models.fall_log.objects.all().order_by('id').reverse()
        list={}
        for i,fall_log in enumerate(fall_logs):
            list[i]=fall_log.__str__()
        return jsonRes("success", 200,list)
    except Exception as e:
        print(e)
        return jsonRes("fail",400)

def interactpage(request):
    return render(request,"interact.html")

@csrf_exempt
def interactinit(request):
    try:
        interaction_logs = models.interaction_log.objects.all().order_by('id').reverse()
        list={}
        for i,interaction_log in enumerate(interaction_logs):
            list[i]=interaction_log.__str__()
        return jsonRes("success", 200,list)
    except Exception as e:
        print(e)
        return jsonRes("fail",400)

def invadepage(request):
    return render(request,"invade.html")

@csrf_exempt
def invadeinit(request):
    try:
        area_logs = models.area_log.objects.all().order_by('id').reverse()
        list={}
        for i,area_log in enumerate(area_logs):
            list[i]=area_log.__str__()
        return jsonRes("success", 200,list)
    except Exception as e:
        print(e)
        return jsonRes("fail",400)

def strangerpage(request):
    return render(request,"stranger.html")

@csrf_exempt
def strangerinit(request):
    try:
        stranger_logs = models.stranger_log.objects.all().order_by('id').reverse()
        list={}
        for i,stranger_log in enumerate(stranger_logs):
            list[i]=stranger_log.__str__()
        return jsonRes("success", 200,list)
    except Exception as e:
        print(e)
        return jsonRes("fail",400)