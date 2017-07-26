from django.conf.urls import url
from . import views

app_name = 'health'

urlpatterns = [
        url(r'^staging/$', views.staging, name='staging'),
        url(r'^production/$', views.production, name='production'),
        ]
