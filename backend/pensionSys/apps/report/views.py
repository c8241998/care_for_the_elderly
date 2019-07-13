from django.shortcuts import render
from apps.camera import models as camera_models
from apps.elder import models as elder_models
from util.json import jsonRes
# Create your views here.
def init(request):
    try:
        list={
            'stranger':camera_models.stranger_log.objects.count(),
            'area':camera_models.area_log.objects.count(),
            'interact':[],
            'emotion_pie':{
                'angry':camera_models.emotion_log.objects.filter(label='angry').__len__(),
                'disgust':camera_models.emotion_log.objects.filter(label='disgust').__len__(),
                'fear':camera_models.emotion_log.objects.filter(label='fear').__len__(),
                'happy':camera_models.emotion_log.objects.filter(label='happy').__len__(),
                'sad':camera_models.emotion_log.objects.filter(label='sad').__len__(),
                'surprise':camera_models.emotion_log.objects.filter(label='surprise').__len__()
            }
        }
        elders = elder_models.elder.objects.all()
        for elder in elders:
            name = elder.name
            times = camera_models.interaction_log.objects.filter(elder=name)
            list['interact'].append({
                'name':name,
                'times':times.__len__()
            })
        return jsonRes("success", 200, list)

    except Exception as e:
        print(e)
        return jsonRes("fail",400)