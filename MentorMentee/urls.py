from django.urls import path

from . import views

#URL's
#path('pathname',functionName)
urlpatterns = [
    path('', views.home, name='home'),

    # ✅ No login in URL
    path('logout', views.logout, name='logout'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('admin_addStudent', views.add_Student, name='admin_addStudent'),
    path('admin_ViewStudents', views.admin_ViewStudents),
    path('admin_addFaculty', views.admin_addFaculty),
    path('admin_viewFaculty', views.admin_viewFaculty),
    path('admin_FacultyDetails/<fac_id>', views.admin_FacultyDetails),
    path('admin_AddAssignment/', views.admin_AddAssignment, name='admin_AddAssignment'),
    path('get_batch_students/<int:batch_id>/<int:faculty_id>', views.get_batch_students, name='get_batch_students'),
    path('save_assignments', views.save_assignments, name='save_assignments'),
    path("admin_ViewAssignments", views.admin_ViewAssignments),
    path("get_assigned_students", views.get_assigned_students, name="get_assigned_students"),

    
    
    
    
    
    
    # path('students_list/', views.students_List, name='students_list'),
]
