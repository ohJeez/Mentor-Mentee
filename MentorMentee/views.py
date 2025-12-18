from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .models import *


# =====================================================
# SESSION CHECK
# =====================================================
def _require_superadmin_session(request):
    login_id = request.session.get("login_id")
    user_type = request.session.get("userType")

    if not login_id or user_type != "superadmin":
        return None
    return login_id


# =====================================================
# HOME / LOGIN
# =====================================================
def home(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pas = request.POST.get('password')

        try:
            user = Login.objects.get(username=uname, password=pas)
            request.session['login_id'] = user.login_id
            request.session['userType'] = user.userType

            if user.userType == 'superadmin':
                return redirect('superadmin_dashboard')
            return HttpResponse("Only Super Admin module implemented")

        except Login.DoesNotExist:
            return HttpResponse("<script>alert('Invalid Login');location.href='/'</script>")

    return render(request, 'Login.html')


# =====================================================
# SUPER ADMIN DASHBOARD
# =====================================================
def superadmin_dashboard(request):
    if not _require_superadmin_session(request):
        return redirect('/')

    context = {
        'total_departments': Department.objects.count(),
        'total_courses': Courses.objects.count(),
        'total_batches': Batches.objects.count(),
        'total_faculty': Faculty.objects.count(),
        'current_admin': Faculty.objects.filter(is_admin=True).first()
    }
    return render(request, 'SuperAdmin/dashboard.html', context)


# =====================================================
# DEPARTMENT MANAGEMENT
# =====================================================
def manage_departments(request):
    if not _require_superadmin_session(request):
        return redirect('/')

    departments = Department.objects.all().order_by('name')
    return render(request, 'SuperAdmin/manage_departments.html', {'departments': departments})


def add_department(request):
    if not _require_superadmin_session(request):
        return redirect('/')

    if request.method == 'POST':
        Department.objects.create(
            name=request.POST['name'],
            code=request.POST['code'],
            hod_name=request.POST['hod'],
            email=request.POST['email']
        )
        return redirect('manage_departments')

    return render(request, 'SuperAdmin/add_department.html')


def delete_department(request, id):
    if not _require_superadmin_session(request):
        return redirect('/')

    get_object_or_404(Department, dept_id=id).delete()
    return redirect('manage_departments')


# =====================================================
# COURSE MANAGEMENT
# =====================================================
def manage_courses(request):
    if not _require_superadmin_session(request):
        return redirect('/')

    return render(request, 'SuperAdmin/manage_courses.html', {
        'courses': Courses.objects.select_related('department').all(),
        'departments': Department.objects.all()
    })


def add_course(request):
    if not _require_superadmin_session(request):
        return redirect('/')

    if request.method == 'POST':
        Courses.objects.create(
            course_name=request.POST.get('course_name'),
            department_id=request.POST.get('department')
        )
        return redirect('manage_courses')
    # GET: show add course form
    return render(request, 'SuperAdmin/add_course.html', {
        'departments': Department.objects.all()
    })


def delete_course(request, course_id):
    if not _require_superadmin_session(request):
        return redirect('/')

    get_object_or_404(Courses, course_id=course_id).delete()
    return redirect('manage_courses')
def add_course(request):
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course_name")
        department_id = request.POST.get("department_id")

        department = Department.objects.get(dept_id=department_id)

        if course_id:
            # EDIT
            course = Courses.objects.get(course_id=course_id)
            course.course_name = course_name
            course.department = department
            course.save()
        else:
            # ADD
            Courses.objects.create(
                course_name=course_name,
                department=department
            )

        return redirect("manage_courses")


# =========================
# SUPER ADMIN - BATCHES
# =========================
from .models import Batches, Department, Courses


def _superadmin_batches_context():
    """Shared context for the batches page."""
    return {
        'batches': Batches.objects.select_related('course').all(),
        'departments': Department.objects.all(),
        'courses': Courses.objects.all(),
        'batches_count': Batches.objects.count(),
    }


def superAdmin_batches(request):
    if not _require_superadmin_session(request):
        return redirect('/')

    return render(request, 'SuperAdmin/superAdmin_batches.html', _superadmin_batches_context())


def superAdmin_add_batch(request):
    if not _require_superadmin_session(request):
        return redirect('/')

    if request.method == 'POST':
        batch_name = request.POST.get('batch_name')
        course_id = request.POST.get('course_id')

        if batch_name and course_id:
            Batches.objects.create(batch_name=batch_name, course_id=course_id)
            return redirect('superAdmin_batches')
        
        return HttpResponse("<script>alert('Batch name and course are required.'); window.location.href='/superAdmin_batches'</script>")

    # Fallback GET renders the batches page with full context
    return render(request, 'SuperAdmin/superAdmin_batches.html', _superadmin_batches_context())



def superAdmin_delete_batch(request, id):
    if 'login_id' not in request.session:
        return redirect('/')

    Batches.objects.filter(batch_id=id).delete()
    return redirect('superAdmin_batches')



# =====================================================
# ADMIN MANAGEMENT
# =====================================================
def superAdmin_admins(request):
    if not _require_superadmin_session(request):
        return redirect('/')

    return render(request, "SuperAdmin/superAdmin_admins.html", {
        "admins": Admin.objects.select_related("department").all(),
        "departments": Department.objects.all()
    })


def superAdmin_add_admin(request):
    if not _require_superadmin_session(request):
        return redirect('/')

    if request.method == "POST":
        department = Department.objects.get(dept_id=request.POST.get("department_id"))

        login = Login.objects.create(
            username=request.POST.get("email"),
            password="admin123",
            userType="admin"
        )

        Admin.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            department=department,
            login_id=login.login_id
        )

    return redirect("superAdmin_admins")


def superAdmin_delete_admin(request, id):
    if not _require_superadmin_session(request):
        return redirect('/')

    Admin.objects.filter(admin_id=id).delete()
    return redirect("superAdmin_admins")


# =====================================================
# FACULTY MANAGEMENT
# =====================================================
def manage_faculty(request):
    if not _require_superadmin_session(request):
        return redirect('/')

    faculties = Faculty.objects.select_related('department').all()
    departments = Department.objects.all()

    search = request.GET.get('search')
    dept = request.GET.get('department')
    role = request.GET.get('admin')

    if search:
        faculties = faculties.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(department__name__icontains=search)
        )

    if dept:
        faculties = faculties.filter(department_id=dept)

    if role == "admin":
        faculties = faculties.filter(is_admin=True)
    elif role == "faculty":
        faculties = faculties.filter(is_admin=False)

    return render(request, 'SuperAdmin/manage_faculty.html', {
        'faculty_list': faculties,
        'departments': departments
    })



def add_faculty(request):
    if not _require_superadmin_session(request):
        return redirect('/')

    departments = Department.objects.all()

    if request.method == 'POST':
        login = Login.objects.create(
            username=request.POST['username'],
            password=request.POST['password'],
            userType='faculty'
        )

        image = request.FILES.get('faculty_image')
        img_path = None

        if image:
            fs = FileSystemStorage(location=f"{settings.MEDIA_ROOT}/faculty_images/")
            filename = fs.save(image.name, image)
            img_path = f"faculty_images/{filename}"

        Faculty.objects.create(
            login=login,
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            designation=request.POST['designation'],
            department_id=request.POST['department'],
            faculty_image=img_path
        )
        return redirect('manage_faculty')

    return render(request, 'SuperAdmin/add_faculty.html', {'departments': departments})


def delete_faculty(request, faculty_id):
    if not _require_superadmin_session(request):
        return redirect('/')

    faculty = get_object_or_404(Faculty, faculty_id=faculty_id)
    Login.objects.filter(login_id=faculty.login.login_id).delete()
    faculty.delete()
    return redirect('manage_faculty')


# =====================================================
# FACULTY PROFILE
# =====================================================
def view_faculty(request, faculty_id):
    if not _require_superadmin_session(request):
        return redirect('/')

    faculty = get_object_or_404(Faculty, faculty_id=faculty_id)
    students = Student.objects.filter(faculty=faculty)

    return render(request, 'SuperAdmin/view_faculty.html', {
        'faculty': faculty,
        'students': students
    })


# =====================================================
# ADMIN ASSIGNMENT
# =====================================================
def make_faculty_admin(request, faculty_id):
    Faculty.objects.update(is_admin=False)
    faculty = get_object_or_404(Faculty, faculty_id=faculty_id)
    faculty.is_admin = True
    faculty.save()
    return redirect('manage_faculty')


def remove_faculty_admin(request, faculty_id):
    faculty = get_object_or_404(Faculty, faculty_id=faculty_id)
    faculty.is_admin = False
    faculty.save()
    return redirect('manage_faculty')


# =====================================================
# LOGOUT
# =====================================================
def logout(request):
    request.session.flush()
    return redirect('/')
