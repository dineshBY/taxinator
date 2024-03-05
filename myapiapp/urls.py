"""
myapiapp/urls.py
"""
from django.urls import path
from .views import MyAPIClass, MyAPIClass_EMI, MyAPIClass_FD, MyAPIClass_RD

urlpatterns = [
    path('calc_tax/', MyAPIClass.as_view()),
    path('calc_emi/', MyAPIClass_EMI.as_view()),
    path('calc_fd/', MyAPIClass_FD.as_view()),
    path('calc_rd/', MyAPIClass_RD.as_view())
]
