from django.conf.urls import url
from .views import *
from .log_view import *
urlpatterns=[
    url(r'^page', page),
    url(r'^emotionpage', emotionpage),
    url(r'^fallpage', fallpage),
    url(r'^interactpage', interactpage),
    url(r'^invadepage', invadepage),
    url(r'^strangerpage', strangerpage),
    url(r'^emotioninit', emotioninit),
    url(r'^fallinit', fallinit),
    url(r'^interactinit', interactinit),
    url(r'^invadeinit', invadeinit),
    url(r'^strangerinit', strangerinit),
]