from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('logout/', logout, name='logout'),

    path('superadmin/dashboard/', superadmin_dashboard, name='superadmin_dashboard'),

    # Assignment approval (SuperAdmin only)
    path('superadmin/pending-assignments/', pending_assignments, name='pending_assignments'),
    path('superadmin/approve-assignment/<int:assignment_id>/', approve_assignment, name='approve_assignment'),
    path('superadmin/reject-assignment/<int:assignment_id>/', reject_assignment, name='reject_assignment'),
]
