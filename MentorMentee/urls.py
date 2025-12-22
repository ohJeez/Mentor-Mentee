from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout', views.logout, name='logout'),

#===============================================================================================

##ADMIN SIDE URLS##
    
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('admin_addStudent', views.add_Student, name='admin_addStudent'),
    path('admin_ViewStudents', views.admin_ViewStudents),
    path('login_send_otp/', views.login_send_otp, name='login_send_otp'),
    path('login_verify_otp/', views.login_verify_otp, name='login_verify_otp'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('admin_addBatch', views.admin_addBatch),
    path('admin_viewBatches', views.admin_viewBatches),
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
    path("admin_reports/", views.admin_Reports, name="admin_reports"),
    path("api/search_entities/", views.search_entities, name="search_entities"),
    path("api/report_data/", views.fetch_report_data, name="fetch_report_data"),
    path("api/report_pdf/", views.generate_report_pdf, name="generate_report_pdf"),
    path('admin_viewSessions',views.admin_viewSessions),
    path("admin_updateSession",views.admin_updateSession,name="admin_updateSession"),
    path('admin_createSession',views.admin_createSession), 
    
    
    
#===============================================================================================

##FACULTY SIDE URLS##  

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
    path('faculty/session-requests/', views.faculty_session_requests, name='faculty_session_requests'),
    path('faculty/session-requests/accept/<int:request_id>/',views.accept_session_request,name='accept_session_request'),
    path('faculty/session-requests/reject/<int:request_id>/',views.reject_session_request,name='reject_session_request'),
    path('faculty/students/',views.faculty_ViewStudents,name='students-view'),
    
    path("faculty/get_sessions/", views.faculty_api_get_sessions, name="faculty_get_sessions"),
    path("faculty/get_day_sessions/<str:day>/", views.faculty_api_get_day_sessions),

    path("api/get_sessions/", views.api_get_sessions),
    path("api/get_day_sessions/<date_str>", views.api_get_day_sessions),
    
#===============================================================================================

##STUDENT SIDE URLS##
    path('signup', views.signup, name='signup'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student_api_get_sessions',views.student_api_get_sessions),
    path("get_sessions/", views.student_api_get_sessions),
    path("get_day_sessions/<str:date_str>", views.student_api_get_day_sessions),
    path('student_RequestSession',views.student_RequestSession),
    path('student_profile',views.student_Profile),
    path('student_uploads',views.student_uploads),
    path("student_delete_upload/<int:id>/", views.student_delete_upload),
    path('student_viewSessions',views.student_viewSessions),
    path("student_update_profile", views.student_update_profile, name="student_update_profile"),
    path("verify-current-password/", views.verify_current_password, name="verify_current_password"),
    path('update_password/',views.update_password,name='update_password'),
    path('verify_otp/',views.verify_otp,name='verify_otp'),
    path('send_otp/',views.send_otp,name='send_otp'),


#===============================================================================================

##HOD SIDE URLS##
    path('hod_dashboard/', views.hod_dashboard, name='hod_dashboard'),

    path('manage_departments/', views.manage_departments, name='manage_departments'),
    path('add_department/', views.add_department, name='add_department'),
    path('delete_department/<int:id>/', views.delete_department, name='delete_department'),

    path('manage_courses/', views.manage_courses, name='manage_courses'),
    path('add_course/', views.add_course, name='add_course'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),

    path("hod_batches/", views.hod_batches, name="hod_batches"),
    path("hod_add_batch/", views.hod_add_batch, name="hod_add_batch"),
    path("hod_delete_batch/<int:id>/", views.hod_delete_batch, name="hod_delete_batch"),

    path('manage_faculty/', views.manage_faculty, name='manage_faculty'),
    path('add_faculty/', views.add_faculty, name='add_faculty'),
    path('delete_faculty/<int:faculty_id>/', views.delete_faculty, name='delete_faculty'),

    path('view_faculty/<int:faculty_id>/', views.view_faculty, name='view_faculty'),
    path('make_faculty_admin/<int:faculty_id>/', views.make_faculty_admin, name='make_faculty_admin'),
    path('remove_faculty_admin/<int:faculty_id>/', views.remove_faculty_admin, name='remove_faculty_admin'),

    path('pending_assignments/', views.pending_assignments, name='pending_assignments'),
    path('approve_assignment/<int:assignment_id>/', views.approve_assignment, name='approve_assignment'),
    path('bulk_approve_assignments/', views.bulk_approve_assignments, name='bulk_approve_assignments'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
    
    
    
    

