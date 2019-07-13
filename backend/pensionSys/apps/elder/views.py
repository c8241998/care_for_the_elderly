from django.shortcuts import render
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from apps.elder import models
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
        elder = models.elder.objects.get(id=id)

        dir = 'media/elder_photo/' + elder.id.__str__() + '.jpg'
        if os.path.exists(dir):
            os.remove(dir)

        file = request.FILES.get('file')
        elder.photo = file
        elder.save()



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
        fam_name = request.POST.get('fam_name')
        fam_phone = request.POST.get('fam_phone')
        elder = models.elder(name=name,phone=phone,birthday=birthday,gender=gender,id_card=id_card,fam_name=fam_name,fam_phone=fam_phone)
        elder.save()
        elder.photo = 'elder_photo/' + elder.id.__str__() + '.jpg'
        shutil.copy('media/common/default.jpg', 'media/elder_photo/' + elder.id.__str__() + '.jpg')
        elder.save()
        return jsonRes("success", 200)
    except Exception as e:
        print(e)
        return jsonRes("fail",400)

@csrf_exempt
def remove(request):
    try:
        id = request.POST.get('id')
        elder = models.elder.objects.get(id=id)
        try:
            os.remove('media/elder_photo/'+id+'.jpg')
        except RuntimeError as e:
            print(e)
            pass
        elder.delete()
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
        fam_name = request.POST.get('fam_name')
        fam_phone = request.POST.get('fam_phone')
        elder = models.elder.objects.get(id=id)
        elder.name = name if name != '' else elder.name
        elder.phone = phone if phone != '' else elder.phone
        elder.birthday = birthday if birthday != '' else elder.birthday
        elder.gender = gender if gender != '' else elder.gender
        elder.id_card = id_card if id_card != '' else elder.id_card
        elder.fam_name = fam_name if fam_name != '' else elder.fam_name
        elder.fam_phone = fam_phone if fam_phone != '' else elder.fam_phone
        elder.save()
        return jsonRes("success", 200)
    except Exception:
        return jsonRes("fail",400)

@csrf_exempt
def request(request):
    try:
        id = request.POST.get('id')
        elder = models.elder.objects.get(id=id)
        content = elder.__str__()
        return jsonRes("success", 200, content)
    except Exception:
        return jsonRes("fail",400)

def page(request):
    return render(request,"elder.html")

@csrf_exempt
def init(request):
    try:
        elders = models.elder.objects.all()
        list={}
        for i,elder in enumerate(elders):
            list[i]=elder.__str__()
        return jsonRes("success", 200,list)
    except Exception as e:
        print(e)
        return jsonRes("fail",400)