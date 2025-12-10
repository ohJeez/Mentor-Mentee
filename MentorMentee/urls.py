from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),

    path('superadmin_dashboard/', superadmin_dashboard, name='superadmin_dashboard'),

    path('manage_departments/', manage_departments, name='manage_departments'),
    path('add_department/', add_department, name='add_department'),
    path('delete_department/<int:id>/', delete_department, name='delete_department'),

    path('manage_courses/', manage_courses, name='manage_courses'),
    path('add_course/', add_course, name='add_course'),
    path('delete_course/<int:course_id>/', delete_course, name='delete_course'),

    path('manage_faculty/', manage_faculty, name='manage_faculty'),
    path('add_faculty/', add_faculty, name='add_faculty'),
    path('delete_faculty/<int:faculty_id>/', delete_faculty, name='delete_faculty'),

    path('logout/', logout, name='logout'),
]
