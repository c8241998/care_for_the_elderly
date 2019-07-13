import urllib,urllib.request
import json
# face host
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=YfzCmMvgP4KEBfF2hKGXBTEp&client_secret=zK0Y3ncch42QP8RfpXtbBoagVA4jjKoA'
request = urllib.request.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')
response = urllib.request.urlopen(request)
content = response.read()
content = json.loads(bytes.decode(content).strip())
access_token = content['access_token']

print(access_token)