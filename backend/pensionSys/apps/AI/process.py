import torch
import torchvision
import time
import os
import numpy as np
from apps.AI.object_detection.detect_object import Detect_object
from apps.AI.face_detection.face_detect import get_faces, crop
from apps.AI.emotion_classification.inference import Emotion_classification
from apps.AI.pose_estimation.pose_estimation import Pose_estimation
from apps.baiduAI.bodyAttributes import get_body_attributes
from apps.baiduAI.faceDetection import get_face
from apps.baiduAI.bodyCoordinate import get_body_coordinate
from PIL import Image
import math

def manul_load():
    Detect_object.manul_load()
    Emotion_classification.manul_load()
    Pose_estimation.manul_load()

def is_stacking(rec1, rec2):
    """
    计算两个矩形框的交并比。
    :param rec1: (x0,y0,x1,y1)      (x0,y0)代表矩形左上的顶点，（x1,y1）代表矩形右下的顶点。下同。
    :param rec2: (x0,y0,x1,y1)
    :return: 交并比IOU.
    """
    left_column_max  = max(rec1[0],rec2[0])
    right_column_min = min(rec1[2],rec2[2])
    up_row_max       = max(rec1[1],rec2[1])
    down_row_min     = min(rec1[3],rec2[3])
    #两矩形无相交区域的情况
    if left_column_max>=right_column_min or down_row_min<=up_row_max:
        return False
    # 两矩形有相交区域的情况
    else:
        return True

def detect_bodies(file, storage='photos/bodies', way="network"):
    """
    This has to be the first step of everything.
    """
    if not os.path.exists(storage):
        os.mkdir(storage)
    assert type(file) == str
    assert way in ['network', 'local']
    bodies = []
    cords = []
    if way == 'local':
        imgs, res = Detect_object.process(file)
        for k, v in res.items():
            if k == 1:
                for line in v:
                    cords.append(line[:4].tolist())
        for img in imgs:
            name = str(time.time())+'.jpg'
            img.save(os.path.join(storage, name))
            bodies.append(name)
    elif way == 'network':
        res = get_body_attributes(file)
        num = res["person_num"]
        info = res['person_info']
        img = Image.open(file).convert('RGB')
        for i in range(num):
            loc = info[i]['location']
            height = loc['height']
            width = loc['width']
            top = loc['top']
            left = loc['left']
            img_ = img.crop([left, top, left+width, top+height])
            name = str(time.time())+'.jpg'
            img_.save(os.path.join(storage, name))
            bodies.append(name)
            cords.append([left, top, left+width, top+height])
    return (bodies, cords)

def detect_faces(file, storage='photos/faces', way='network'):
    if not os.path.exists(storage):
        os.mkdir(storage)
    assert type(file) == str
    assert way in ['network', 'local']
    faces = []
    img = Image.open(file).convert('RGB')

    if way == 'local':
        res_faces, ldmrks = get_faces(img)
        faces = crop(img, res_faces, storage)
    elif way == 'network':
        try:
            res = get_face(file)['result']
            num = res['face_num']
            face_list = res['face_list']
            for i in range(num):
                face_ = face_list[i]
                loc = face_['location']
                height = loc['height']
                width = loc['width']
                top = loc['top']
                left = loc['left']
                img_ = img.crop([left, top, left + width, top + height])
                name = str(time.time()) + '.jpg'
                img_.save(os.path.join(storage, name))
                faces.append(name)
        except Exception as e:
            return []

    return faces

def detect_emotion(file, way='network'):
    assert type(file) == str
    assert way in ['network', 'local']
    img = Image.open(file).convert('RGB')
    if way == 'local':
        label = Emotion_classification.inference(img)
    elif way == 'network':
        res = get_face(file)['result']
        if res == None:
            return 'neutral'
        num = res['face_num']
        face_list = res['face_list']
        label = 'neutral'
        if num > 0:
            face_ = face_list[0]
            label = face_['emotion']['type']
    return label

def detect_pose(file, degree=30, storage='photos/fall', way='network'):
    if not os.path.exists(storage):
        os.mkdir(storage)
    assert type(file) == str
    assert way in ['network', 'local']
    img = Image.open(file).convert('RGB')
    if way == 'local':
        res = Pose_estimation.process(file, degree)
        if res == None:
            return False
        else:   
            return res
    elif way == 'network':
        res = get_body_coordinate(file)
        try:
            if res['person_num'] > 0:
                print('detected {} body(s)'.format(res['person_num']))
                info = res['person_info'][0]['body_parts']
                neck = info['neck']
                right_ankle = info['right_ankle']
                tan = abs(right_ankle['y'] - neck['y']) / (abs(right_ankle['x'] - neck['x']) + 1e-6)
                if math.degrees(math.atan(tan)) < degree:
                    return True
                else:
                    return False
            else:
                print('no body detected!')
                return False
        except Exception as e:
            return False





















