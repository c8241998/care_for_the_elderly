from django.conf.urls import url
from .views import *
urlpatterns=[
    url(r'^login', login , name='login'),
    url(r'^logout', logout , name='logout'),
    url(r'^modifyPwd', modifyPwd ),
]