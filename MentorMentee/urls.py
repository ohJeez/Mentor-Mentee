from django.urls import path
from django.contrib import admin
from django.urls import path
from MentorMentee import views

#URL's
#path('pathname',functionName)
urlpatterns=[
    path('',views.home,name='home'),
    path('students_list/<faculty_id>',views.students_list)
]