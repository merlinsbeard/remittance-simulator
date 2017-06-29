from django.conf.urls import url
from . import views

app_name = 'person'

urlpatterns = [
        url(r'^$', views.ProfileDetail.as_view(), name='self'),
        ]
