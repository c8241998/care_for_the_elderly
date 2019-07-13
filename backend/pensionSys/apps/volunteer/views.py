from django.shortcuts import render
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from apps.volunteer import models
from util.json import jsonRes
from django.views.decorators.csrf import csrf_exempt
import shutil
import os
# Create your views here.

def page(request):
    return render(request,"volunteer.html")

# 上传头像
@csrf_exempt
def upload_photo(request):
    try:
        id = request.POST.get('id')
        volunteer = models.volunteer.objects.get(id=id)

        dir = 'media/volunteer_photo/' + volunteer.id.__str__() + '.jpg'
        if os.path.exists(dir):
            os.remove(dir)

        file = request.FILES.get('file')
        volunteer.photo = file
        volunteer.save()
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
        visitdate = request.POST.get('visitdate')
        volunteer = models.volunteer(name=name, phone=phone, birthday=birthday, gender=gender, id_card=id_card,
                                     visitdate=visitdate )

        volunteer.save()
        shutil.copy('media/common/default.jpg','media/volunteer_photo/'+volunteer.id.__str__()+'.jpg')
        return jsonRes("success", 200)
    except Exception:
        return jsonRes("fail",400)

@csrf_exempt
def remove(request):
    try:
        id = request.POST.get('id')
        volunteer = models.volunteer.objects.get(id=id)
        try:
            os.remove('media/volunteer_photo/'+id+'.jpg')
        except RuntimeError as e:
            print(e)
            pass
        volunteer.delete()
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
        visitdate = request.POST.get('visitdate')
        volunteer = models.volunteer.objects.get(id=id)
        volunteer.name = name if name != '' else volunteer.name
        volunteer.phone = phone if phone != '' else volunteer.phone
        volunteer.birthday = birthday if birthday != '' else volunteer.birthday
        volunteer.gender = gender if gender != '' else volunteer.gender
        volunteer.id_card = id_card if id_card != '' else volunteer.id_card
        volunteer.visitdate = visitdate if visitdate != '' else volunteer.visitdate
        volunteer.save()
        return jsonRes("success", 200)
    except Exception:
        return jsonRes("fail",400)

@csrf_exempt
def request(request):
    try:
        id = request.POST.get('id')
        volunteer = models.volunteer.objects.get(id=id)
        content = volunteer.__str__()
        return jsonRes("success", 200, content)
    except Exception:
        return jsonRes("fail",400)

@csrf_exempt
def init(request):
    try:
        volunteers = models.volunteer.objects.all()
        list={}
        for i,volunteer in enumerate(volunteers):
            list[i]=volunteer.__str__()
        return jsonRes("success", 200,list)
    except Exception as e:
        print(e)
        return jsonRes("fail",400)

def page(request):
    return render(request,"volunteer.html")