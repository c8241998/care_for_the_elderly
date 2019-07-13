from django.http import JsonResponse

def jsonRes(status,code,content=""):
    return JsonResponse({
        "status":str(status),
        "code":code,
        "content":content
    }
    )