"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^remittance/', include('partner.urls', namespace='partner')),
    # Rest Framework Browsable API
    url(r'^api-auth/', include('rest_framework.urls',
                       namespace='rest_framework')),
    url(r'^v1/', include('v1.urls', namespace='v1')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^profile/', include('person.urls', namespace='profile')),
    url(r'^health/', include('health.urls', namespace='health')),
    url('^$', RedirectView.as_view(pattern_name='profile:self'), name='home'),
    # JWT
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
]
