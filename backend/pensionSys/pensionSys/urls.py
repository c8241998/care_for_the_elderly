"""pensionSys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url,include
from apps.account import views as account_view
from apps.camera import views as camera_view
from apps.elder import views as elder_view
from django.views.static import serve
from pensionSys.settings import MEDIA_ROOT
from apps.websocket import views as websocket_view
urlpatterns = [
    url('admin/', admin.site.urls),
    url('account/', include('apps.account.urls')),
    url('elder/', include('apps.elder.urls')),
    url('volunteer/', include('apps.volunteer.urls')),
    url('worker/', include('apps.worker.urls')),
    url('camera/', include('apps.camera.urls')),
    url('report/', include('apps.report.urls')),
    url('upload1/', camera_view.upload_img_1),
    url('upload2/', camera_view.upload_img_2),
    url('websocket/', include('apps.websocket.urls')),
    url(r'^media/(?P<path>.*)$',  serve, {"document_root": MEDIA_ROOT}),

    url('landing',account_view.landing),
    url('^$',account_view.home),
    url('home',account_view.home),
    url('mainpage',account_view.mainpage),
    url('delete',account_view.delete),

    url('test2/',elder_view.test_uploadPhoto),
]
