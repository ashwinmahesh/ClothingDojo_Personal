from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index),
    url(r'^processLogin/$', views.processLogin),
    url(r'^register/$', views.register),
    url(r'^processRegister/$', views.processRegister)
]