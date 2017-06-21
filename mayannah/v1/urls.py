from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from v1.views import RemittanceList, RemittanceDetail, RemittancePay

urlpatterns = [
        url(r'^remittance/$', RemittanceList.as_view()),
        url(r'^remittance/(?P<slug>[-\w]+)/$', RemittanceDetail.as_view()),
        url(r'^remittance/(?P<slug>[-\w]+)/pay/$',
                    RemittancePay.as_view()),
        ]

urlpatterns = format_suffix_patterns(urlpatterns)
