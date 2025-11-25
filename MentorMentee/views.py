from django.shortcuts import render
from django.http import *
from . models import *
from django.core.files.storage import FileSystemStorage
import os
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import F
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from functools import wraps

# Create your views here.
def home(request):
    if request.method =='POST':
        uname = request.POST.get('uname')
        pas = request.POST.get('password')
        print(uname)
        try:
            res= Login.objects.get(username=uname,password=pas)
            
            if res and res.userType == 'admin':
                admin_details=Admin.objects.get(login_id=res.login_id)
                request.session['login_id']=admin_details.login_id
                
                total_students=Student.objects.filter(department_id=admin_details.department_id).count()
                total_mentors=Faculty.objects.filter(department_id=admin_details.department_id).count()
                print(admin_details.name)
                data={'total_students':total_students,'total_mentors':total_mentors,'login':request.session.get('login_id'),'admin':admin_details}
                return render(request,'./Admin/admin_dashboard.html',data)
            
            elif res and res.userType == 'faculty':
                data = Faculty.objects.get(login_id=res.login_id)
                # Student model has no 'faculty' FK — use department or all students
                students = Student.objects.filter(faculty_id=data.faculty_id)  # or Student.objects.all()
                return render(request, 'Faculty/index.html', {'name': data.name, 'students': students, 'faculty': data})
            
            else:
                return HttpResponse("<script>alert('Invalid Login Credentials!');</script>")

        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse("<script>alert('Invalid Login Credentials!');</script>")
            
    return render(request,'Login.html') 


def admin_dashboard(request):
    session_login = request.session.get('login_id')
    if not session_login:
        return HttpResponse("<script>alert('Session expired!'); window.location.href='/'</script>")

    return render(request, './Admin/admin_dashboard.html')



#Logout
def logout(request):
    request.session.flush()   # clears session completely
    return redirect('/')  

#Admin add student
def add_Student(request):
    # ✅ Check session
    session_login = request.session.get('login_id')
    if not session_login:
        return HttpResponse(
            "<script>alert('Session expired! Please login again.'); window.location.href='/'</script>"
        )
    try:
        admin_det = Admin.objects.get(login_id=session_login)
        courses = Courses.objects.filter(department_id=admin_det.department_id).order_by('course_name')
        batches = Batches.objects.filter(course__department_id=admin_det.department_id)
        contents = {'courses': courses,'batch': batches,'admin':admin_det}

        if request.method == 'POST':
            name = request.POST['name']
            roll = request.POST['roll']
            course = request.POST['department']
            email = request.POST['email']
            phone = request.POST['phone']
            dob = request.POST['dob']
            batch = request.POST['batch']
            photo = request.FILES['photo']

            photo_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'static',
                'student_images'
            )

            fs = FileSystemStorage(location=photo_path, base_url='../static/student_images/')
            image = fs.save(photo.name, photo)

            res=Student(
                name=name,
                email=email,
                reg_no=roll,
                phone=phone,
                department_id=admin_det.department_id,
                batch_id=batch,
                course_id=course,
                student_image=image,
                year=1
            )
            res.save()
            return HttpResponse(
                "<script>alert('Student Added Successfully!'); window.location.href='/admin_addStudent'</script>")

    except Exception as e:
        print("Error:", e)

    return render(request, './Admin/admin_addStudent.html', contents)

#View Students
def admin_ViewStudents(request):
    login_id=request.session.get('login_id')
    if not login_id:
        return HttpResponse(
            "<script>alert('Session expired! Please login again.'); window.location.href='/'</script>"
        )
    try:
        adm_dept=Admin.objects.get(login_id=login_id)
        batches = Batches.objects.filter(course__department_id=adm_dept.department_id)
        #all students
        students=Student.objects.filter(department_id=adm_dept.department_id)
        contents={'batches':batches,'students':students,'admin':adm_dept}
    except Exception as e:
        print(f"Error! {e}")
    return render(request,'./Admin/view_students.html',contents)

#Add faculty
def admin_addFaculty(request):
    contents={}
    try:
        login_id=request.session.get('login_id')
        if not login_id:
            return HttpResponse(
            "<script>alert('Session expired! Please login again.'); window.location.href='/'</script>")
        adm_dept=Admin.objects.get(login_id=login_id)
        dept=Department.objects.filter(dept_id=adm_dept.department_id)
        contents={'department':dept,'admin':adm_dept}
    except Exception as e:
        print(f"Error! {e}")
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        department=request.POST['department']
        designation=request.POST['designation']
        username=request.POST['username']
        passwd=request.POST['password']
        faculty_image=request.FILES['faculty_image']
        photo_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'static',
                'faculty_images'
            )

        fs = FileSystemStorage(location=photo_path, base_url='../static/faculty_images/')
        image = fs.save(faculty_image.name, faculty_image)
        
        res1=Login(username=username,password=passwd,userType='faculty')
        res1.save()
        res2=Faculty(name=name,email=email,phone=phone,department_id=department,designation=designation,faculty_image=image,login_id=res1.login_id)
        res2.save()
        
        return HttpResponse(
                "<script>alert('Faculty Added Successfully!'); window.location.href='/admin_addFaculty'</script>")
    return render(request,'./Admin/admin_addFaculty.html',contents)

#View Faculties
def admin_viewFaculty(request):
    contents={}
    try:
        login_id=request.session.get('login_id')
        if not login_id:
            return HttpResponse(
            "<script>alert('Session expired! Please login again.'); window.location.href='/'</script>")
        dept=Admin.objects.get(login_id=login_id)
        faculty=Faculty.objects.filter(department_id=dept.department_id)
        contents={'faculties':faculty,'admin':dept}
    except Exception as e:
        print(f"Error! {e}")
    return render(request,'./Admin/admin_viewFaculty.html',contents)

#View faculty details
def admin_FacultyDetails(request,fac_id):
    contents={}
    try:
        login_id=request.session.get('login_id')
        if not login_id:
            return HttpResponse(
            "<script>alert('Session expired! Please login again.'); window.location.href='/'</script>")
        admin=Admin.objects.get(login_id=login_id)
        fac_details=Faculty.objects.get(faculty_id=fac_id)
        assigned_stu=Student.objects.filter(faculty_id=fac_id)
        batches=Batches.objects.filter(course__department=fac_details.department_id)
        contents={'faculty':fac_details,'students':assigned_stu,'batches':batches,'admin':admin}
    except Exception as e:
        print(f"Error! {e}")
    return render(request,'./Admin/admin_FacultyDetails.html',contents)

#Add Assignments
def admin_AddAssignment(request):
    try:
        login_id = request.session.get('login_id')
        if not login_id:
            return HttpResponse(
                "<script>alert('Session expired! Please login again.'); window.location.href='/'</script>"
            )

        admin = Admin.objects.get(login_id=login_id)
        admin_dept = admin.department_id
        faculties = Faculty.objects.filter(department_id=admin_dept)
        batches = Batches.objects.filter(course__department_id=admin_dept)
        context = {'faculties': faculties,'batches': batches,'admin':admin}
    except Exception as e:
        print(f"Error in admin_AddAssignment: {e}")
        context = {}
    return render(request, './Admin/admin_AddAssignment.html', context)

#Filter students based on batch and faculty
def get_batch_students(request, batch_id, faculty_id):
    try:
        assigned = Student.objects.filter(batch_id=batch_id, faculty_id=faculty_id)
        unassigned = Student.objects.filter(batch_id=batch_id, faculty__isnull=True)

        return JsonResponse({
            "assigned": list(assigned.values("student_id", "name", "reg_no")),
            "unassigned": list(unassigned.values("student_id", "name", "reg_no")),
        })
    except Exception as e:
        print(f"Error in get_batch_students: {e}")
        return JsonResponse({"error": "Something went wrong"}, status=500)

#Saving new assignments
@csrf_exempt
def save_assignments(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            faculty_id = data.get("faculty")
            student_ids = data.get("students", [])

            # Clear old assignments for THIS faculty (you can also limit by batch if you want)
            Student.objects.filter(faculty_id=faculty_id).update(faculty=None)

            # Assign new students
            Student.objects.filter(student_id__in=student_ids).update(faculty_id=faculty_id)

            return JsonResponse({"status": "success", "message": "Assignments saved successfully ✅"})
        except Exception as e:
            print(f"Error in save_assignments: {e}")
            return JsonResponse({"error": "Server error"}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=400)

#Admin view assignments
def admin_ViewAssignments(request):
    login_id = request.session.get('login_id')
    if not login_id:
        return redirect('/')
    admin = Admin.objects.get(login_id=login_id)
    dept = admin.department_id
    faculties = Faculty.objects.filter(department_id=dept)
    batches = Batches.objects.filter(course__department_id=dept)
    return render(request, './Admin/admin_ViewAssignments.html',
                  {"faculties": faculties, "batches": batches,"admin":admin}
    )

#Filtering students based on assignments
def get_assigned_students(request):
    faculty = request.GET.get("faculty")
    batch = request.GET.get("batch")
    students = Student.objects.filter(faculty_id=faculty)

    if batch:
        students = students.filter(batch_id=batch)
    return JsonResponse({
        "students": list(
            students.annotate(
                course_name=F("course__course_name"),
                batch_name=F("batch__batch_name")
            ).values(
                "name",
                "reg_no",
                "student_image",
                "course_name",
                "batch_name",
            )
        )
    })


##FACULTY SIDE VIEWS##

def assignment_page(request):
    faculties = Faculty.objects.all()
    departments = Department.objects.all()
    students = Student.objects.all()

    return render(request, "assignment_page.html", {
        "faculties": faculties,
        "departments": departments,
        "students": students,
    })
    
def students_partial(request):
    return render(request, 'Faculty/students-content.html')

def student_profile(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    return render(request, 'Faculty/student_profile.html', {'student': student})

def student_profile_partial(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    return render(request, 'Faculty/student_profile.html', {'student': student})   

def your_view(request):
    students = Student.objects.filter(faculty=request.user)  # adjust as needed
    departments = Department.objects.all()
    
    context = {
        'students': students,
        'departments': departments,
    }
    return render(request, 'Faculty/students-content.html', context)