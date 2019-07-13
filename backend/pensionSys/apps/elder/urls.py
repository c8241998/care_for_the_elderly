from django.conf.urls import url
from .views import *
urlpatterns=[
    url(r'^uploadPhoto', upload_photo),

    url(r'^add', add),
    url(r'^remove', remove),
    url(r'^update', update),
    url(r'^request', request),
    url(r'^page', page),
    url(r'^init',init),
]