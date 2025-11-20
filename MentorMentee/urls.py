from django.urls import path

from . import views

#URL's
#path('pathname',functionName)
urlpatterns=[
    path('',views.home,name='home'),
    
    #ADMIN
    path('admin_dashboard',views.admin_dashboard),
    path('students_list/<login>',views.students_List), 
]