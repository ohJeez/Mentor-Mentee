from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models import Q

from .models import (
    Department,
    Courses,
    Login,
    Faculty,
    Student,
    Assignment   # <-- IMPORTANT
)

# =========================================================
# LOGIN (UNCHANGED LOGIC, TENANT-AWARE)
# =========================================================
def home(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pas = request.POST.get('password')

        try:
            login = Login.objects.get(username=uname, password=pas)
            faculty = Faculty.objects.select_related('department').get(login=login)

            request.session['login_id'] = login.login_id
            request.session['faculty_id'] = faculty.faculty_id
            request.session['department_id'] = faculty.department.dept_id
            request.session['is_superadmin'] = faculty.is_superadmin
            request.session['is_admin'] = faculty.is_admin

            if faculty.is_superadmin:
                return redirect('superadmin_dashboard')
            else:
                return HttpResponse("Only SuperAdmin module implemented")

        except (Login.DoesNotExist, Faculty.DoesNotExist):
            return HttpResponse(
                "<script>alert('Invalid Login!');window.location.href='/'</script>"
            )

    return render(request, 'Login.html')


# =========================================================
# SUPERADMIN DASHBOARD
# =========================================================
def superadmin_dashboard(request):
    if not request.session.get('is_superadmin'):
        return redirect('/')

    dept_id = request.session['department_id']

    context = {
        'total_faculty': Faculty.objects.filter(department_id=dept_id).count(),
        'pending_assignments': Assignment.objects.filter(
            status='pending',
            faculty__department_id=dept_id
        ).count()
    }

    return render(request, 'SuperAdmin/dashboard.html', context)


# =========================================================
# SUPERADMIN — VIEW PENDING ASSIGNMENTS
# =========================================================
def pending_assignments(request):
    if not request.session.get('is_superadmin'):
        return redirect('/')

    dept_id = request.session['department_id']

    assignments = Assignment.objects.select_related(
        'student', 'faculty'
    ).filter(
        status='pending',
        faculty__department_id=dept_id
    )

    return render(
        request,
        'SuperAdmin/pending_assignments.html',
        {'assignments': assignments}
    )


# =========================================================
# SUPERADMIN — APPROVE ASSIGNMENT
# =========================================================
def approve_assignment(request, assignment_id):
    if not request.session.get('is_superadmin'):
        return redirect('/')

    dept_id = request.session['department_id']

    assignment = get_object_or_404(
        Assignment,
        assignment_id=assignment_id,
        status='pending',
        faculty__department_id=dept_id
    )

    # 1. Approve assignment
    assignment.status = 'approved'
    assignment.save()

    # 2. Update student table ONLY NOW
    student = assignment.student
    student.faculty = assignment.faculty
    student.save()

    # 3. Email hook (already exists in your project)
    # send_assignment_approval_mail(student.email)

    return redirect('pending_assignments')


# =========================================================
# SUPERADMIN — REJECT ASSIGNMENT
# =========================================================
def reject_assignment(request, assignment_id):
    if not request.session.get('is_superadmin'):
        return redirect('/')

    dept_id = request.session['department_id']

    assignment = get_object_or_404(
        Assignment,
        assignment_id=assignment_id,
        status='pending',
        faculty__department_id=dept_id
    )

    assignment.status = 'rejected'
    assignment.save()

    return redirect('pending_assignments')


# =========================================================
# LOGOUT
# =========================================================
def logout(request):
    request.session.flush()
    return redirect('/')
