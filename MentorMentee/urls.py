from django.urls import path

from . import views

#URL's
#path('pathname',functionName)
urlpatterns = [
    path('', views.home, name='home'),

    # ✅ No login in URL
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('admin_addStudent', views.add_Student, name='admin_addStudent'),
    path('admin_ViewStudents', views.admin_ViewStudents),
    path('admin_addFaculty', views.admin_addFaculty),
    path('admin_viewFaculty', views.admin_viewFaculty),
    path('admin_FacultyDetails/<fac_id>', views.admin_FacultyDetails),
    path('admin_AddAssignment', views.admin_AddAssignment),
    
    
    
    
    
    # path('students_list/', views.students_List, name='students_list'),
]
