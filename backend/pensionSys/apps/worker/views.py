from django.shortcuts import render
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from apps.worker import models
from util.json import jsonRes
from django.views.decorators.csrf import csrf_exempt
import shutil
import os
# Create your views here.
# 上传头像
@csrf_exempt
def upload_photo(request):
    try:
        id = request.POST.get('id')
        worker = models.worker.objects.get(id=id)

        dir = 'media/worker_photo/' + worker.id.__str__() + '.jpg'
        if os.path.exists(dir):
            os.remove(dir)

        file = request.FILES.get('file')
        worker.photo = file
        worker.save()

        return jsonRes("success", 200)
    except Exception:
        return jsonRes("fail",400)

def test_uploadPhoto(request):
    return render(request,"uploadPhoto.html")

@csrf_exempt
def add(request):
    try:
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        birthday = request.POST.get('birthday')
        gender = request.POST.get('gender')
        id_card = request.POST.get('id_card')
        worker = models.worker(name=name,phone=phone,birthday=birthday, gender=gender, id_card=id_card)
        worker.save()
        shutil.copy('media/common/default.jpg', 'media/worker_photo/' + worker.id.__str__() + '.jpg')
        return jsonRes("success", 200)
    except Exception:
        return jsonRes("fail",400)

@csrf_exempt
def remove(request):
    try:
        id = request.POST.get('id')
        worker = models.worker.objects.get(id=id)
        try:
            os.remove('media/worker_photo/'+id+'.jpg')
        except RuntimeError as e:
            print(e)
            pass
        worker.delete()
        return jsonRes("success", 200)
    except Exception:
        return jsonRes("fail",400)

@csrf_exempt
def update(request):
    try:
        id = request.POST.get('id')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        birthday = request.POST.get('birthday')
        gender = request.POST.get('gender')
        id_card = request.POST.get('id_card')
        worker = models.worker.objects.get(id=id)
        worker.name = name if name!='' else worker.name
        worker.phone = phone if phone != '' else worker.phone
        worker.birthday = birthday if birthday != '' else worker.birthday
        worker.gender = gender if gender != '' else worker.gender
        worker.id_card = id_card if id_card != '' else worker.id_card
        worker.save()
        return jsonRes("success", 200)
    except Exception:
        return jsonRes("fail",400)

@csrf_exempt
def request(request):
    try:
        id = request.POST.get('id')
        worker = models.worker.objects.get(id=id)
        content = worker.__str__()
        return jsonRes("success", 200, content)
    except Exception:
        return jsonRes("fail",400)

@csrf_exempt
def init(request):
    try:
        workers = models.worker.objects.all()
        list={}
        for i,worker in enumerate(workers):
            list[i]=worker.__str__()
        return jsonRes("success", 200,list)
    except Exception as e:
        print(e)
        return jsonRes("fail",400)

def page(request):
    return render(request,"worker.html")