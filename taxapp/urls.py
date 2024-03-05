from django.urls import path
from .views import corporate_page, personal_page
from .views import cal_corporate
from .views import cal_personal, emi_page, calculate_emi, fd_page, calculate_fd
from .views import rd_page, calculate_rd

urlpatterns = [
    path('corporate/', corporate_page),
    path('personal/',personal_page),
    path('corporate_tax/', cal_corporate),
    path('personal_tax/', cal_personal),
    path('emi_page/', emi_page),
    path('calculate_emi/', calculate_emi),
    path('fd_page/', fd_page),
    path('calculate_fd/', calculate_fd),
    path('rd_page/', rd_page),
    path('calculate_rd/', calculate_rd)
]