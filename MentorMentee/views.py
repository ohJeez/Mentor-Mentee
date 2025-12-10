from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import Department, Courses, Login, Faculty


# HOME / LOGIN
def home(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pas = request.POST.get('password')

        try:
            user = Login.objects.get(username=uname, password=pas)
            request.session['login_id'] = user.login_id

            if user.userType == 'superadmin':
                return redirect('superadmin_dashboard')
            elif user.userType == 'admin':
                return HttpResponse("Admin Dashboard coming soon!")
            elif user.userType == 'faculty':
                return HttpResponse("Faculty Dashboard coming soon!")

        except Login.DoesNotExist:
            return HttpResponse("<script>alert('Invalid Login!');window.location.href='/'</script>")

    return render(request, 'Login.html')


# SUPER ADMIN DASHBOARD
def superadmin_dashboard(request):
    if 'login_id' not in request.session:
        return redirect('/')

    context = {
        'total_departments': Department.objects.count(),
        'total_courses': Courses.objects.count(),
        'total_faculty': Faculty.objects.count()
    }
    return render(request, 'SuperAdmin/dashboard.html', context)


# DEPARTMENT MANAGEMENT
def manage_departments(request):
    if 'login_id' not in request.session:
        return redirect('/')

    departments = Department.objects.all().order_by('name')
    return render(request, 'SuperAdmin/manage_departments.html', {'departments': departments})


def add_department(request):
    if 'login_id' not in request.session:
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
    if 'login_id' not in request.session:
        return redirect('/')

    get_object_or_404(Department, dept_id=id).delete()
    return redirect('manage_departments')


# COURSE MANAGEMENT
def manage_courses(request):
    if 'login_id' not in request.session:
        return redirect('/')

    courses = Courses.objects.select_related('department').all()
    departments = Department.objects.all()

    return render(request, 'SuperAdmin/manage_courses.html', {
        'courses': courses,
        'departments': departments
    })


def add_course(request):
    if 'login_id' not in request.session:
        return redirect('/')

    if request.method == 'POST':
        Courses.objects.create(
            course_name=request.POST['course_name'],
            department_id=request.POST['department']
        )
    return redirect('manage_courses')


def delete_course(request, course_id):
    if 'login_id' not in request.session:
        return redirect('/')

    get_object_or_404(Courses, course_id=course_id).delete()
    return redirect('manage_courses')


# FACULTY MANAGEMENT
def manage_faculty(request):
    if 'login_id' not in request.session:
        return redirect('/')

    faculty = Faculty.objects.select_related('department').all()
    return render(request, 'SuperAdmin/manage_faculty.html', {'faculty_list': faculty})


def add_faculty(request):
    if 'login_id' not in request.session:
        return redirect('/')

    departments = Department.objects.all()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        designation = request.POST.get('designation')
        department = request.POST.get('department')
        image = request.FILES.get('faculty_image')

        # Create Login record
        login = Login.objects.create(
            username=username,
            password=password,
            userType='faculty'
        )

        # Save Image inside media/faculty_images/
        img_path = None
        if image:
            fs = FileSystemStorage(location=f"{settings.MEDIA_ROOT}/faculty_images/")
            img_filename = fs.save(image.name, image)
            img_path = f"faculty_images/{img_filename}"

        # Create Faculty record
        Faculty.objects.create(
            login=login,
            name=name,
            email=email,
            phone=phone,
            designation=designation,
            department_id=department,
            faculty_image=img_path
        )

        return redirect('manage_faculty')

    return render(request, 'SuperAdmin/add_faculty.html', {
        'departments': departments
    })


def delete_faculty(request, faculty_id):
    if 'login_id' not in request.session:
        return redirect('/')

    faculty = get_object_or_404(Faculty, faculty_id=faculty_id)
    Login.objects.filter(login_id=faculty.login.login_id).delete()
    faculty.delete()
    return redirect('manage_faculty')


# LOGOUT
def logout(request):
    request.session.flush()
    return redirect('/')
