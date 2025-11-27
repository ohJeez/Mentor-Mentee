from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
    path("admin_profile", views.admin_profile, name="admin_profile"),
    path('admin_StudentDetails/<int:s_id>', views.admin_StudentDetails, name="admin_StudentDetails"),
    path("admin_uploadStudents", views.admin_uploadStudents, name="admin_uploadStudents"),
    path("admin_reports", views.admin_Reports, name="admin_reports"),
    path("admin_reports_data", views.filter_sessions, name="admin_reports_data"),
    path("admin_reports_pdf", views.generate_report_pdf, name="admin_reports_pdf"),
    
    ##Faculty URL's
    path('faculty/', views.faculty_dashboard, name='faculty_dashboard'),
    path('students/', views.students_content, name='students-content'),
    path('student/<int:student_id>/', views.student_profile, name='student_profile'),
    path('student/<int:id>/sessions/', views.student_session, name="student_session"),
    path('student/<int:id>/upload-application/', views.upload_application, name='upload_application'),
    path('student/<int:id>/upload-assessment/', views.upload_assessment, name='upload_assessment'),
    path('student/<int:id>/new-session/', views.new_session, name='new_session'),
    path('session/<int:id>/details/', views.session_details, name='session_details'),
    path('profile/', views.profile_content, name='profile_content'),
    path('filter-students/', views.filter_students, name='filter_students'),
    path('session/<int:session_id>/', views.view_session, name='view_session'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
    
    
    
    

