"""
homeapp/urls.py
"""
from django.urls import path
from .views import my_QA_page,add_QA_page

urlpatterns = [
    path('', my_QA_page),
    path('addQA/', add_QA_page),
]
