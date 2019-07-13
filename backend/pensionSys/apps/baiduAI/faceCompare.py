# encoding:utf-8
import urllib,urllib.parse,urllib.request
import base64
import json
from .access_token import token

def compare_face(img1,img2):
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match" #请求地址
    with open(img1,"rb") as f1:
        base64_data1 = base64.b64encode(f1.read())
        with open(img2,"rb") as f2:
            base64_data2 = base64.b64encode(f2.read())

            params = json.dumps(
                [{"image": str(base64_data1,encoding='UTF8'), "image_type": "BASE64"},
                 {"image": str(base64_data2,encoding='UTF8'), "image_type": "BASE64"}])
            params = params.encode('utf-8')

            request_url = request_url + "?access_token=" + token._token_
            request = urllib.request.Request(url=request_url, data=params)
            request.add_header('Content-Type', 'application/json')
            response = urllib.request.urlopen(request)
            content = response.read()
            content = json.loads(str(content, encoding='UTF8'))

            return(content)