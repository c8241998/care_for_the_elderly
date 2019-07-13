from django.conf.urls import url
from .views import *
urlpatterns=[
    url(r'^msg', msg),
    url(r'^data', data),
]