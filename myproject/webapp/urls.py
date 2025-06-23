from django.urls import path
from .models import Employees
from . import views


urlpatterns=[
    path('emp_list/',views.employeeview),
    path('emp_detail/<int:pk>/',views.employeedetailview),
    ]
