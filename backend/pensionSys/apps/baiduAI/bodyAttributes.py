# encoding:utf-8
import urllib,urllib.parse,urllib.request
import base64
import json
from .access_token import token

def get_body_attributes(img):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_attr"

    with open(img,"rb") as f:
        base64_data = base64.b64encode(f.read())
        params = {
            "image":str(base64_data,encoding='UTF8'),
        }
        params = urllib.parse.urlencode(params).encode(encoding='UTF8')
        request_url = request_url + "?access_token=" + token._token_
        request = urllib.request.Request(url=request_url, data=params)
        request.add_header('Content-Type', 'application/json')
        response = urllib.request.urlopen(request)
        content = response.read()
        content = json.loads(str(content,encoding='UTF8'))
        return(content)