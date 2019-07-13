import torch
import torchvision
from torchvision import transforms
from PIL import Image, ImageDraw
import PIL
import math
import numpy as np


class Pose_estimation:

    model = None
    transform = None
    device = "cuda" if torch.cuda.is_available() else "cpu"
    COCO_INSTANCE_CATEGORY_NAMES = [
        '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
        'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
        'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
        'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
        'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
        'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
        'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
        'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
        'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
        'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
    ]
    @classmethod
    def manul_load(cls):
        print('Loading local pose detection model ...')
        if cls.model == None:
            cls.model = torchvision.models.detection.keypointrcnn_resnet50_fpn(
                            pretrained=True).to(cls.device)
            
            cls.model.eval()
            
    @classmethod
    def inference(cls, img):
        # assert type(img) == PIL.Image.Image
        if cls.model == None:
            cls.model = torchvision.models.detection.keypointrcnn_resnet50_fpn(
                pretrained=True).to(cls.device)
            
            cls.model.eval()

        if cls.transform == None:
            cls.transform = transforms.Compose([
                transforms.ToTensor(),
            ])

        return cls.model([cls.transform(img).to(cls.device)])[0]

    @classmethod
    def parse(cls, res, threshold=0.85):
        scores = res['scores'].detach().cpu().numpy()
        boxes = res['boxes'].detach().cpu().numpy()
        labels = res['labels'].detach().cpu().numpy()
        keypoints = res['keypoints'].detach().cpu().numpy()
        res = []
        for score, box, label, keypoint in zip(scores, boxes, labels, keypoints):
            if score < threshold:
                continue
            if label != 1.:
                continue
            tmp = []
            for item in box:
                tmp.append(item)
            tmp.append(score)
            tmp.append(label)
            tmp.append(keypoint)
            res.append(tmp)
        return res

    @classmethod
    def nms(cls, dets, thresh=0.35):
        # x1、y1、x2、y2、以及score赋值
        x1 = dets[:, 0]
        y1 = dets[:, 1]
        x2 = dets[:, 2]
        y2 = dets[:, 3]
        scores = dets[:, 4]

        # 每一个候选框的面积
        areas = (x2 - x1 + 1) * (y2 - y1 + 1)
        # order是按照score降序排序的
        order = scores.argsort()[::-1]

        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)
            # 计算当前概率最大矩形框与其他矩形框的相交框的坐标，会用到numpy的broadcast机制，得到的是向量
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])

            # 计算相交框的面积,注意矩形框不相交时w或h算出来会是负数，用0代替
            w = np.maximum(0.0, xx2 - xx1 + 1)
            h = np.maximum(0.0, yy2 - yy1 + 1)
            inter = w * h
            # 计算重叠度IOU：重叠面积/（面积1+面积2-重叠面积）
            ovr = inter / (areas[i] + areas[order[1:]] - inter)

            # 找到重叠度不高于阈值的矩形框索引
            inds = np.where(ovr <= thresh)[0]
            # 将order序列更新，由于前面得到的矩形框索引要比矩形框在原order序列中的索引小1，所以要把这个1加回来
            order = order[inds + 1]
        return keep

    @classmethod
    def translate_label(cls, id):
        return cls.COCO_INSTANCE_CATEGORY_NAMES[int(id)]

    @classmethod
    def process(cls, img_path, degree):
        # assert type(img_path) == str
        img = Image.open(img_path).convert('RGB')
        res = cls.inference(img)
        parsed = cls.parse(res)
        if len(parsed) == 0:
            print('No body detected!')
            return None
        partial = []
        for line in parsed:
            tmp = []
            for item in line[:5]:
                tmp.append(item)
            partial.append(tmp)
        partial = np.array(partial)
        chosen = cls.nms(partial)
        final_parsed = []
        for i in chosen:
            final_parsed.append(parsed[i])
        # finl = parsed[nmsed]
        
        # return (img, final_parsed)
        return cls.fall_judge(final_parsed[0], degree)

    @classmethod
    def fall_judge(cls, data, degree):
        samples = data[-1]
        nose = samples[0][:2]
        right_ankle = samples[-1][:2]
        tan = abs(right_ankle[-1]-nose[-1]) / abs(right_ankle[0]-nose[0])
        print('Body detected, degree is ', math.degrees(math.atan(tan)))
        if math.degrees(math.atan(tan)) < degree:
            return True
        else :
            return False


