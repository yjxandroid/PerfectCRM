# PerfectCRM/urls.py

from django.conf.urls import url,include
from django.contrib import admin
from PerfectCRM import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^crm/', include('crm.urls')),
    url(r'^login/', views.acc_login,name='login'),
    url(r'^logout/', views.acc_logout,name='logout'),
]
