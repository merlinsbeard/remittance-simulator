from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='list'),
    url(r'^(?P<slug>[-\w]+)/$',
        views.RemittanceDetailView.as_view(), name='detail')
]
