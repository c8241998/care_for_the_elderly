# views.py
from django.shortcuts import render
from django.http import StreamingHttpResponse,HttpResponse
import socket
from django.views.decorators.csrf import csrf_exempt
from apps.baiduAI import faceDetection,faceCompare,bodyAttributes,bodyCoordinate
import json
from PIL import Image
from apps.elder import models as elder_model
from apps.worker import models as worker_model
from apps.volunteer import models as volunteer_model
import _thread
import time
from .models import stranger_log,emotion_log,fall_log,interaction_log,area_log
import shutil
from apps.AI import process
from util import conf
import _thread
def index(request):
    #此处的模板请自行创建 例如:<html><body>< img src='http://your_ip:port/camera/video_feed/' >
    return render(request,'camera.html')

def broadcast_thread(thread,msg,port):
    s = socket.socket()  # 创建 socket 对象
    host = socket.gethostname()  # 获取本地主机名
    addr = (host, port)
    s.connect(addr)  # 绑定端口号
    s.send(msg.encode('utf-8'))
    s.close()  # 关闭连接

def broadcast(msg,port=9000):
    _thread.start_new_thread(broadcast_thread,("thread",msg,port))



def strange(body,face):

    is_strange = True
    threshold = 30

    result={
        'strange':True,
        'elder':None,
        'volunteer':None
    }

    # 对比elder库
    if is_strange:
        elders = elder_model.elder.objects.all()
        for i, elder in enumerate(elders):
            id = elder.id
            elder_photo_dir = 'media/elder_photo/' + str(id) + '.jpg'
            try:
                compare_result = faceCompare.compare_face(elder_photo_dir, face)
                score = compare_result['result']['score']
                if score > threshold:
                    is_strange = False
                    result['elder'] = id
                    break
                time.sleep(0.5)
            except Exception as e:
                continue

    # 对比worker库
    if is_strange:
        workers = worker_model.worker.objects.all()
        for i, worker in enumerate(workers):
            id = worker.id
            worker_photo_dir = 'media/worker_photo/' + str(id) + '.jpg'
            try:
                compare_result = faceCompare.compare_face(worker_photo_dir, face)
                score = compare_result['result']['score']
                if score > threshold:
                    is_strange = False
                    break
                time.sleep(0.5)
            except Exception as e:
                continue

    # 对比volunteer库
    if is_strange:
        volunteers = volunteer_model.volunteer.objects.all()
        for i, volunteer in enumerate(volunteers):
            id = volunteer.id
            volunteer_photo_dir = 'media/volunteer_photo/' + str(id) + '.jpg'
            try:
                compare_result = faceCompare.compare_face(volunteer_photo_dir, face)
                score = compare_result['result']['score']
                if score > threshold:
                    is_strange = False
                    result['volunteer'] = id
                    break
                time.sleep(0.5)
            except Exception as e:
                continue

    if is_strange is True:
        try:
            body_attr = bodyAttributes.get_body_attributes(body)

            attr = body_attr['person_info'][0]['attributes']
            new_log = stranger_log(
                gender=attr['gender']['name'],
                upper_wear_fg=attr['upper_wear_fg']['name'],
                cellphone=attr['cellphone']['name'],
                orientation=attr['orientation']['name'],
                headwear=attr['headwear']['name'],
                age=attr['age']['name'],
                glasses=attr['glasses']['name'],
                bag=attr['bag']['name'],
                upper_wear_texture=attr['upper_wear_texture']['name'],
                lower_wear=attr['lower_wear']['name'],
                upper_color=attr['upper_color']['name'],
            )
            new_log.save()
            new_pic_dir = 'media/stranger_log/' + new_log.id.__str__() + '.jpg'
            shutil.copy(body, new_pic_dir)
            new_log.picture = new_pic_dir
            new_log.save()

            broadcast(str({
                "msg": "有陌生人进入！",
                "dir": "../" + new_pic_dir
            }))

        except KeyError as e:
            print(e)
            pass

    result['strange'] = is_strange
    print('strange: '+is_strange.__str__())

    return result

def emotion(face,elder,way):

    emotion_label = process.detect_emotion(face, way=way)
    broadcast(str({
        "type": "emotion_pie",
        "label": emotion_label
    }),port=9001)
    new_log = emotion_log(elder=elder,label=emotion_label)
    new_log.save()
    shutil.copy(face,'media/emotion_log/'+new_log.id.__str__()+'.jpg')
    print('emotion:'+emotion_label.__str__())

def fall(body,degree=30,way='local'):

    is_fall = False

    try:
        result = process.detect_pose(body,degree=degree,way=way)
        is_fall = result
    except RuntimeError as e:
        print(e)
        pass

    if is_fall:
        new_log = fall_log()
        new_log.save()
        new_pic_dir = 'media/fall_log/'+new_log.id.__str__()+'.jpg'
        shutil.copy(body,new_pic_dir)
        broadcast(str({
            "msg": "有摔倒行为发生！",
            "dir": "../" + new_pic_dir
        }))

    print('fall: '+is_fall.__str__())

def interaction(record,img):
    for volunteer in record['volunteer']:
        for elder in record['elder']:
            new_log = interaction_log()
            new_log.elder = elder_model.elder.objects.get(id=elder).name
            new_log.volunteer = volunteer_model.volunteer.objects.get(id=volunteer).name
            new_log.save()
            shutil.copy(img,'media/interaction_log/'+new_log.id.__str__()+'.jpg')

    print('interaction finish')

def analysis1(threadName,dir,way):

    detection = process.detect_bodies(dir,way=way)
    body_list = detection[0]
    print('body:'+body_list.__len__().__str__())
    # 交互记录
    interaction_record={
        'volunteer':[],
        'elder':[]
    }

    for body in body_list:

        body_dir = 'photos/bodies/' + body
        faces = process.detect_faces(body_dir,way=way)
        for face in faces:
            face_dir = 'photos/faces/' + face

            # 陌生人
            detection_result = strange(body_dir,face_dir)

            elder_id = detection_result['elder']
            volunteer_id = detection_result['volunteer']
            if not elder_id is None:
                # emotion
                emotion(face_dir,elder_id,way=way)
                interaction_record['elder'].append(elder_id)

            if not volunteer_id is None:
                interaction_record['volunteer'].append(volunteer_id)

            break

        # 摔倒
        degree = conf.conf()['degree']
        fall(body_dir,degree=degree,way='network')


    # 交互
    interaction(interaction_record,dir)

    print('finish a img')

def analysis2(threadName,dir,way,area):
    detection = process.detect_bodies(dir)
    body_list = detection[0]
    boxes = detection[1]
    for i,box in enumerate(boxes):
        if process.is_stacking(box,area):
            body = 'photos/bodies/' + body_list[i]
            try:

                body_attr = bodyAttributes.get_body_attributes(body)

                attr = body_attr['person_info'][0]['attributes']
                new_log = area_log(
                    gender=attr['gender']['name'],
                    upper_wear_fg=attr['upper_wear_fg']['name'],
                    cellphone=attr['cellphone']['name'],
                    orientation=attr['orientation']['name'],
                    headwear=attr['headwear']['name'],
                    age=attr['age']['name'],
                    glasses=attr['glasses']['name'],
                    bag=attr['bag']['name'],
                    upper_wear_texture=attr['upper_wear_texture']['name'],
                    lower_wear=attr['lower_wear']['name'],
                    upper_color=attr['upper_color']['name'],
                )
                new_log.save()
                new_pic_dir = 'media/area_log/' + new_log.id.__str__() + '.jpg'
                shutil.copy(body, new_pic_dir)
                new_log.picture = new_pic_dir
                new_log.save()

                broadcast(str({
                    "msg":"禁止区域有入侵行为！",
                    "dir":"../"+new_pic_dir
                }))

                broadcast(str({
                    "type": "area"
                }),port=9001)

            except KeyError as e:
                print(e)
                pass


@csrf_exempt
def upload_img_1(request):
    dir = 'photos/camera1/'+request.FILES['img'].name

    with open(dir , 'wb') as f:
        f.write(request.FILES['img'].read())

    conf_json = conf.conf()
    way = conf_json['way']
    print('receive a img')
    _thread.start_new_thread(analysis1,("thread1",dir,way))

    return HttpResponse('File received!')

@csrf_exempt
def upload_img_2(request):
    dir = 'photos/camera2/'+request.FILES['img'].name

    with open(dir , 'wb') as f:
        f.write(request.FILES['img'].read())

    conf_json = conf.conf()
    way = conf_json['way']
    area = conf_json['warn_area']

    _thread.start_new_thread(analysis2,("thread2",dir,way,area))

    return HttpResponse('File received!')

