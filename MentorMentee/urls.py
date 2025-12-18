from django.urls import path
from . import views

urlpatterns = [

    # LOGIN
    path('', views.home, name='home'),
    path('logout/', views.logout, name='logout'),

    # SUPER ADMIN DASHBOARD
    path('superadmin_dashboard/', views.superadmin_dashboard, name='superadmin_dashboard'),

    # DEPARTMENT MANAGEMENT
    path('manage_departments/', views.manage_departments, name='manage_departments'),
    path('add_department/', views.add_department, name='add_department'),
    path('delete_department/<int:id>/', views.delete_department, name='delete_department'),

    # COURSE MANAGEMENT
    path('manage_courses/', views.manage_courses, name='manage_courses'),
    path('add_course/', views.add_course, name='add_course'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),

    # BATCHES
    path("superAdmin_batches/", views.superAdmin_batches, name="superAdmin_batches"),
    path("superAdmin_add_batch/", views.superAdmin_add_batch, name="superAdmin_add_batch"),
    path("superAdmin_delete_batch/<int:id>/", views.superAdmin_delete_batch, name="superAdmin_delete_batch"),

    # FACULTY MANAGEMENT
    path('manage_faculty/', views.manage_faculty, name='manage_faculty'),
    path('add_faculty/', views.add_faculty, name='add_faculty'),
    path('delete_faculty/<int:faculty_id>/', views.delete_faculty, name='delete_faculty'),

    # FACULTY ADMIN
    path('view_faculty/<int:faculty_id>/', views.view_faculty, name='view_faculty'),
    path('make_faculty_admin/<int:faculty_id>/', views.make_faculty_admin, name='make_faculty_admin'),
    path('remove_faculty_admin/<int:faculty_id>/', views.remove_faculty_admin, name='remove_faculty_admin'),
]
