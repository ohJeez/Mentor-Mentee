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
import csv
from datetime import datetime,timedelta,date
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from django.utils.dateparse import parse_date
from django.core.mail import send_mail
from django.db.models import F, Value
from django.db.models.functions import Coalesce
import csv
import io


# Create your views here.
def home(request):
    if request.method =='POST':
        uname = request.POST.get('uname')
        pas = request.POST.get('password')
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
                students = Student.objects.filter(faculty_id=data.faculty_id)
                courses = students.values_list('course', flat=True).distinct()
                years = students.values_list('year', flat=True).distinct()
                departments = Department.objects.all()
                courses = Courses.objects.all()
                batches = Batches.objects.all()
                
                request.session['login_id'] = res.login_id
                request.session['faculty_name'] = data.name
                
                return render(request, 'Faculty/faculty_dashboard.html', {'name': data.name, 'students': students, 'faculty': data, 'departments': departments, 'courses': courses, 'years': years, 'courses': courses, "batches": batches,})
            
            elif res and res.userType == 'student':
                student=Student.objects.get(login_id=res.login_id)
                request.session['login_id']=student.login_id
                dept = student.department
                today = date.today()
                active_sessions = Schedule.objects.filter(
                    batch__course__department=dept,
                    start_date__lte=today,
                    end_date__gte=today,
                    status='active',
                )
                pending_sessions = Schedule.objects.filter(
                    batch__course__department=dept,
                    start_date__gt=today,
                )
                missed_sessions = Schedule.objects.filter(
                    batch__course__department=dept,
                    end_date__lt=today,
                    status='incomplete',
                )
                return render(request, "./Student/student_dashboard.html", {
                    "student": student,
                    "active_sessions": active_sessions,
                    "pending_sessions": pending_sessions,
                    "missed_sessions": missed_sessions,
                })
            
            else:
                return HttpResponse("""
                    <!DOCTYPE html>
                    <html>
                    <head>
                    <meta charset="UTF-8">
                    <title>Redirecting...</title>
                    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
                    </head>
                    <body>
                    <script>
                    Swal.fire({
                        title: "Invalid Login",
                        text: "Invalid login credentials. Please try again.",
                        icon: "error",
                        confirmButtonColor: "#28a745",
                        allowOutsideClick: false
                    }).then(() => {
                        window.location.href = "/";
                    });
                    </script>
                    </body>
                    </html>
                    """)


        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse("""
                <!DOCTYPE html>
                <html>
                <head>
                <meta charset="UTF-8">
                <title>Redirecting...</title>
                <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
                </head>
                <body>
                <script>
                Swal.fire({
                    title: "Invalid Login",
                    text: "Invalid login credentials. Please try again.",
                    icon: "error",
                    confirmButtonColor: "#28a745",
                    allowOutsideClick: false
                }).then(() => {
                    window.location.href = "/";
                });
                </script>
                </body>
                </html>
                """)

            
    return render(request,'Login.html') 


def admin_dashboard(request):
    session_login = request.session.get("login_id")
    if not session_login:
        return HttpResponse("<script>alert('Session expired!');window.location.href='/'</script>")

    admin = Admin.objects.get(login_id=session_login)

    # Today sessions
    today = date.today()
    today_list = Schedule.objects.filter(start_date__lte=today, end_date__gte=today,status='active')

    # Pending = future start dates
    pending_list = Schedule.objects.filter(start_date__gt=today)

    context = {
        "admin": admin,
        "today_list": today_list,
        "pending_list": pending_list,
    }
    return render(request, "./Admin/admin_dashboard.html", context)



# API: FULL CALENDAR EVENTS
def api_get_sessions(request):
    schedules = Schedule.objects.all()
    events = []

    colors = {
        "active": "#4f46e5",
        "completed": "#16a34a",
        "incomplete": "#ca8a04",
        "cancelled": "#dc2626",
    }

    for s in schedules:
        events.append({
            "title": s.batch.batch_name,
            "start": str(s.start_date),
            "end": (str(s.end_date + timedelta(days=1))),  # FullCalendar uses end-exclusive
            "color": colors.get(s.status, "#4f46e5")
        })

    return JsonResponse(events, safe=False)



# API: SESSIONS FOR A PARTICULAR DAY
def api_get_day_sessions(request, date_str):
    day = date.fromisoformat(date_str)

    sessions = Schedule.objects.filter(
        start_date__lte=day,
        end_date__gte=day
    )

    data = [
        {
            "batch": s.batch.batch_name,
            "status": s.status,
            "start": str(s.start_date),
            "end": str(s.end_date)
        }
        for s in sessions
    ]

    return JsonResponse(data, safe=False)

#Admin Create Session
def admin_createSession(request):
    contents={}
    login_id = request.session.get('login_id')
    if not login_id:
        return HttpResponse("""
            <html>
            <head>
                <script src='https://cdn.jsdelivr.net/npm/sweetalert2@11'></script>
            </head>
            <body>
                <script>
                    Swal.fire({
                        title: 'Session Expired!',
                        text: 'Please login again.',
                        icon: 'warning'
                    }).then(() => {
                        window.location.href = '/';
                    });
                </script>
            </body>
            </html>
        """)
    try:   
        admin = Admin.objects.get(login_id=login_id)
        batches = Batches.objects.filter(course__department_id=admin.department_id)
        contents={'admin':admin,'batches':batches}
        if request.method == 'POST':
            batch = request.POST['batch']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            status = request.POST['status']
            mail_subject = request.POST['mail_subject']
            mail_body = request.POST['mail_body']
            if start_date > end_date:
                return HttpResponse("<script>alert('Invalid Date Selection!');window.location.href='admin_createSession'</script>")
            
            res = Schedule(
                start_date=start_date,
                end_date=end_date,
                status=status,
                created_at=date.today(),
                batch_id=batch,
                created_by_id=login_id
                )
            res.save()
            
            batch=Batches.objects.get(batch_id=batch)
            
            #Mail delivery system
            send_mail(
                subject=mail_subject,
                message=mail_body,
                from_email="noreply.mentormentee@gmail.com",
                recipient_list=[batch.batch_mail],
                fail_silently=False,
            )

            return HttpResponse("<script>alert('Session Created & Mail Sent Sucessfully!');window.location.href='/admin_createSession'</script>")
    except Exception as e:
        print(f"Error! {e}")
    return render(request,'./Admin/admin_createSession.html',contents)

#Logout
def logout(request):
    request.session.flush()   # clears session completely
    return redirect('/')  

def dob_to_password(dob_str):
    """
    Convert YYYY-MM-DD → DDMMYYYY
    """
    dob = datetime.strptime(dob_str, "%Y-%m-%d")
    return dob.strftime("%d%m%Y")




#Admin add student
def add_Student(request):
    # ✅ Session check
    session_login = request.session.get('login_id')
    if not session_login:
        return HttpResponse(
            "<script>alert('Session expired! Please login again.'); window.location.href='/'</script>"
        )

    admin_det = Admin.objects.get(login_id=session_login)

    courses = Courses.objects.filter(
        department_id=admin_det.department_id
    ).order_by('course_name')

    batches = Batches.objects.filter(
        course__department_id=admin_det.department_id
    )

    contents = {
        'courses': courses,
        'batch': batches,
        'admin': admin_det
    }

    # =====================================================
    # 🔹 CSV BULK UPLOAD
    # =====================================================
    if request.method == "POST" and request.FILES.get("csv_file"):
        try:
            csv_file = request.FILES["csv_file"]

            if not csv_file.name.lower().endswith(".csv"):
                raise Exception("Invalid file type")

            decoded = csv_file.read().decode("utf-8-sig").splitlines()

            # Detect delimiter (comma / tab)
            dialect = csv.Sniffer().sniff(decoded[0])
            reader = csv.DictReader(decoded, dialect=dialect)

            # Normalize headers
            reader.fieldnames = [
                h.strip().lower().replace(" ", "_")
                for h in reader.fieldnames
            ]

            added_count = 0

            for row in reader:
                # Mandatory checks
                if not row.get("name") or not row.get("reg_no") or not row.get("dob"):
                    continue

                reg_no = row["reg_no"].strip()

                # Skip duplicates
                if Student.objects.filter(reg_no=reg_no).exists():
                    continue

                # ----------------------------
                # CREATE LOGIN
                # ----------------------------
                password = dob_to_password(row["dob"])

                login = Login(
                    username=reg_no,
                    password=password,
                    userType="student"
                )
                login.save()

                # ----------------------------
                # CREATE STUDENT
                # ----------------------------
                Student.objects.create(
                    login=login,
                    name=row["name"].strip(),
                    reg_no=reg_no,
                    email=row["email"].strip(),
                    phone=row.get("phone", "").strip(),
                    dob=row["dob"],
                    department_id=admin_det.department_id,
                    course_id=int(row["course_id"]),
                    batch_id=int(row["batch_id"]),
                    year=int(row.get("year", 1)),
                    faculty=None,
                    student_image=None,
                    application_form=None,
                    assessment_file=None
                )

                added_count += 1

            return HttpResponse(f"""
            <!DOCTYPE html>
            <html>
            <head>
              <meta charset="UTF-8">
              <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
            </head>
            <body>
            <script>
              Swal.fire({{
                title: "Upload Successful!",
                text: "{added_count} students uploaded successfully!",
                icon: "success",
                confirmButtonColor: "#28a745",
                allowOutsideClick: false,
                draggable: true
              }}).then(() => {{
                window.location.href = "/admin_addStudent";
              }});
            </script>
            </body>
            </html>
            """)

        except Exception as e:
            print("CSV Upload Error:", e)
            return HttpResponse("""
            <!DOCTYPE html>
            <html>
            <head>
              <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
            </head>
            <body>
            <script>
              Swal.fire({
                title: "Upload Failed",
                text: "Error processing CSV file.",
                icon: "error",
                confirmButtonColor: "#28a745"
              }).then(() => {
                window.history.back();
              });
            </script>
            </body>
            </html>
            """)

    # =====================================================
    # 🔹 SINGLE STUDENT ADD
    # =====================================================
    if request.method == 'POST':
        try:
            name = request.POST['name']
            roll = request.POST['roll']
            course = request.POST['department']
            email = request.POST['email']
            phone = request.POST['phone']
            dob = request.POST['dob']
            batch = request.POST['batch']

            photo = request.FILES.get('photo')
            application = request.FILES.get('application_form')
            assessment = request.FILES.get('assessment_file')
            username = request.POST['username']
            password = request.POST['password']
            
            # ---------------- PHOTO ----------------
            image = None
            if photo:
                photo_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    'static',
                    'student_images'
                )
                fs = FileSystemStorage(location=photo_path)
                image = fs.save(photo.name, photo)

            # ---------------- APPLICATION ----------------
            # saved_application_name = None
            # if application:
                # application_path = os.path.join(
                #     os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                #     'static',
                #     'student_applications'
                # )
                # fs_app = FileSystemStorage(location=application_path)
                # saved_application_name = fs_app.save(application.name, application)

            # ---------------- ASSESSMENT ----------------
            # saved_assessment_name = None
            # if assessment:
            #     assessment_path = os.path.join(
            #         os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            #         'static',
            #         'student_assessment'
            #     )
            #     fs_assessment = FileSystemStorage(location=assessment_path)
            #     saved_assessment_name = fs_assessment.save(assessment.name, assessment)
            
            login = Login(username=username,password=password,userType='student')
            login.save()

            Student.objects.create(
                name=name,
                email=email,
                reg_no=roll,
                phone=phone,
                dob=dob,
                department_id=admin_det.department_id,
                batch_id=batch,
                course_id=course,
                student_image=image,
                year=1,
                application_form=application,
                assessment_file=assessment,
                login=login
            )

            return HttpResponse(
                "<script>alert('Student Added Successfully!'); window.location.href='/admin_addStudent'</script>"
            )

        except Exception as e:
            print("Single Upload Error:", e)
            return HttpResponse(
                "<script>alert('Error adding student!');window.history.back();</script>"
            )

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
        courses=Courses.objects.filter(department_id=adm_dept.department_id)
        #all students
        students=Student.objects.filter(department_id=adm_dept.department_id)
        contents={'batches':batches,'students':students,'admin':adm_dept,'courses':courses}
    except Exception as e:
        print(f"Error! {e}")
    return render(request,'./Admin/view_students.html',contents)

#Add faculty
# def admin_addFaculty(request):
#     contents={}
#     try:
#         login_id=request.session.get('login_id')
#         if not login_id:
#             return HttpResponse(
#             "<script>alert('Session expired! Please login again.'); window.location.href='/'</script>")
#         adm_dept=Admin.objects.get(login_id=login_id)
#         dept=Department.objects.filter(dept_id=adm_dept.department_id)
#         contents={'department':dept,'admin':adm_dept}
#     except Exception as e:
#         print(f"Error! {e}")
#     if request.method=='POST':
#         name=request.POST['name']
#         email=request.POST['email']
#         phone=request.POST['phone']
#         department=request.POST['department']
#         designation=request.POST['designation']
#         username=request.POST['username']
#         passwd=request.POST['password']
#         faculty_image=request.FILES['faculty_image']
#         photo_path = os.path.join(
#                 os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
#                 'static',
#                 'faculty_images'
#             )

#         fs = FileSystemStorage(location=photo_path, base_url='../static/faculty_images/')
#         image = fs.save(faculty_image.name, faculty_image)
        
#         res1=Login(username=username,password=passwd,userType='faculty')
#         res1.save()
#         res2=Faculty(name=name,email=email,phone=phone,department_id=department,designation=designation,faculty_image=image,login_id=res1.login_id)
#         res2.save()
        
#         return HttpResponse(
#                 "<script>alert('Faculty Added Successfully!'); window.location.href='/admin_addFaculty'</script>")
#     return render(request,'./Admin/admin_addFaculty.html',contents)


#Add Batches
def admin_addBatch(request):
    contents={}
    try:
        login_id=request.session.get('login_id')
        if not login_id:
            return HttpResponse(
            "<script>alert('Session expired! Please login again.'); window.location.href='/'</script>")
        adm_dept=Admin.objects.get(login_id=login_id)
        courses=Courses.objects.filter(department_id=adm_dept.department_id)
        contents={'courses':courses,'admin':adm_dept}
    except Exception as e:
        print(f"Error! {e}")
    if request.method=='POST':
        batch_name=request.POST['batch_name']
        course=request.POST['course']
        
        res=Batches(batch_name=batch_name,course_id=course)
        res.save()
        
        return HttpResponse(
                "<script>alert('Batch Added Successfully!'); window.location.href='/admin_addBatch'</script>")
    return render(request,'./Admin/admin_addBatch.html',contents)

#View Batches
def admin_viewBatches(request):
    contents={}
    try:
        login_id=request.session.get('login_id')
        if not login_id:
            return HttpResponse(
            "<script>alert('Session expired! Please login again.'); window.location.href='/'</script>")
        adm_dept=Admin.objects.get(login_id=login_id)
        batches=Batches.objects.filter(course__department_id=adm_dept.department_id)
        contents={'batches':batches,'admin':adm_dept}
        
        #Editing batch
        if request.method == 'POST':
            batch_id=request.POST['batch_id']
            batch_name=request.POST['batch_name']
            mail=request.POST['batch_mail']
            
            batch_obj=Batches.objects.get(batch_id=batch_id)
            batch_obj.batch_name=batch_name
            batch_obj.batch_mail=mail
            batch_obj.save()
            return HttpResponse(
                "<script>alert('Batch Updated Successfully!'); window.location.href='/admin_viewBatches'</script>")
    except Exception as e:
        print(f"Error! {e}")
    return render(request,'./Admin/admin_viewBatches.html',contents)

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

# #Saving new assignments
# @csrf_exempt
# def save_assignments(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)

#             faculty_id = data.get("faculty")
#             student_ids = data.get("students", [])

#             faculty = Faculty.objects.get(faculty_id=faculty_id)

#             # STEP 1 — Fetch students originally assigned to this faculty
#             old_assigned_ids = list(
#                 Student.objects.filter(faculty_id=faculty_id).values_list("student_id", flat=True)
#             )

#             # STEP 2 — Students who were removed (unassigned)
#             removed_ids = set(old_assigned_ids) - set(student_ids)

#             # STEP 3 — Clear assignment for removed students
#             Student.objects.filter(student_id__in=removed_ids).update(faculty_id=None)

#             # STEP 4 — Assign new students
#             Student.objects.filter(student_id__in=student_ids).update(faculty_id=faculty_id)

#             # STEP 5 — Identify students who are newly assigned OR re-assigned after unassign
#             newly_assigned_ids = (set(student_ids) - set(old_assigned_ids)) | (set(student_ids) & removed_ids)

#             newly_assigned_students = Student.objects.filter(student_id__in=newly_assigned_ids)

#             # STEP 6 — Send email only to newly assigned OR re-assigned students
#             for s in newly_assigned_students:
#                 try:
#                     email_subject = "Mentor Assignment Notification"
#                     email_body = f"""
# Dear {s.name},

# Greetings!

#     You have been assigned a mentor as part of the Mentorship Programme.

#     Assigned Mentor:
#         Name: {faculty.name}
#         Department: {faculty.department.name}

# Please contact your mentor as required.

# Regards,
#     Mentor-Mentee Coordination Team
# """

#                     send_mail(
#                         subject=email_subject,
#                         message=email_body,
#                         from_email="noreply.mentormentee@gmail.com",
#                         recipient_list=[s.email],
#                         fail_silently=False,
#                     )

#                 except Exception as err:
#                     print(f"Email error for {s.name}: {err}")

#             return JsonResponse({
#                 "status": "success",
#                 "message": "Assignments updated. Emails sent only to newly assigned or re-assigned students."
#             })

#         except Exception as e:
#             print(f"Error in save_assignments: {e}")
#             return JsonResponse({"error": "Server error"}, status=500)

#     return JsonResponse({"error": "Invalid method"}, status=400)

@csrf_exempt
def save_assignments(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            faculty_id = data.get("faculty")
            student_ids = data.get("students", [])

            faculty = Faculty.objects.get(faculty_id=faculty_id)

            for sid in student_ids:
                Assignment.objects.update_or_create(
                    student_id=sid,
                    defaults={
                        "faculty": faculty,
                        "status": "pending"
                    }
                )

            return JsonResponse({
                "status": "success",
                "message": "Assignments submitted for HOD approval"
            })

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

    return render(
        request,
        "Admin/admin_ViewAssignments.html",
        {
            "faculties": faculties,
            "batches": batches,
            "admin": admin
        }
    )
    
#Filtering students based on assignments
def get_assigned_students(request):
    faculty = request.GET.get("faculty")
    batch = request.GET.get("batch")

    login_id = request.session.get("login_id")
    admin = Admin.objects.get(login_id=login_id)
    dept = admin.department_id

    # Base queryset: all department students
    students = Student.objects.filter(department_id=dept)

    # Optional filters
    if faculty:
        students = students.filter(faculty_id=faculty)

    if batch:
        students = students.filter(batch_id=batch)

    return JsonResponse({
        "students": list(
            students.annotate(
                course_name=F("course__course_name"),
                batch_name=F("batch__batch_name"),
                faculty_name=Coalesce(F("faculty__name"), Value("Unassigned"))
            ).values(
                "name",
                "reg_no",
                "student_image",
                "course_name",
                "batch_name",
                "faculty_name",
            )
        )
    })
    
    
#Admin Profile
def admin_profile(request):
    contents={}

    try:
        login_id = request.session.get('login_id')
        if not login_id:
            return redirect('/')
        admin=Admin.objects.get(login_id=login_id)
        contents={'admin':admin}
        
        #Editing data
        if request.method == 'POST':
            admin.name = request.POST['name']
            admin.email = request.POST['email']
            admin.phone = request.POST['phone']
            if "admin_image" in request.FILES:
                admin_imag = request.FILES['admin_image']
                photo_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'static',
                'admin_image'
            )
                fs = FileSystemStorage(location=photo_path, base_url='../static/admin_image/')
                admin.admin_image = fs.save(admin_imag.name, admin_imag)
            admin.save()
            return redirect ('admin_profile')
            
    except Exception as e:
        print(f"Error! {e}")
    return render(request,'./Admin/admin_profile.html',contents)

#Student Details
def admin_StudentDetails(request, s_id):
    try:
        login_id = request.session.get('login_id')
        if not login_id:
            return redirect('/')
        admin = Admin.objects.get(login_id=login_id)
        student = Student.objects.get(student_id=s_id)
        return render(request, './Admin/admin_StudentDetails.html', {
            'student': student,
            'admin': admin
        })
    except Exception as e:
        print("Error:", e)
        return redirect('/admin_ViewStudents')

#Upload students via CSV
import csv, io
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def admin_uploadStudents(request):
    try:
        login_id = request.session.get("login_id")
        if not login_id:
            return redirect("/")

        admin = Admin.objects.get(login_id=login_id)
        admin_department = admin.department  # logged-in admin dept

        if request.method == "POST" and request.FILES.get("csv_file"):
            csv_file = request.FILES["csv_file"]

            # ✅ Validate file type
            if not csv_file.name.endswith(".csv"):
                messages.error(request, "Please upload a valid CSV file!")
                return redirect("admin_addStudent")

            # ✅ Decode and read CSV
            data = csv_file.read().decode("utf-8")
            io_string = io.StringIO(data)
            reader = csv.DictReader(io_string)

            added, skipped = 0, 0

            for row in reader:
                reg_no = row.get("reg_no")

                # ✅ Prevent duplicates
                if Student.objects.filter(reg_no=reg_no).exists():
                    skipped += 1
                    continue

                # ✅ Get foreign key references
                course = Courses.objects.filter(course_name=row.get("course")).first()
                batch = Batches.objects.filter(batch_name=row.get("batch")).first()

                if not course or not batch:
                    skipped += 1
                    continue

                # ✅ Create student record
                Student.objects.create(
                    name=row.get("name"),
                    email=row.get("email"),
                    reg_no=reg_no,
                    phone=row.get("phone"),
                    dob=row.get("dob") or None,
                    year=row.get("year") or 1,
                    department=admin_department,
                    course=course,
                    batch=batch,
                    student_image="",     # optional or handle separately
                )

                added += 1

            messages.success(
                request,
                f"✅ Upload complete — {added} added, {skipped} skipped (duplicates/invalid)."
            )

            return redirect("admin_addStudent")

    except Exception as e:
        print("CSV Upload Error:", e)
        messages.error(request, "Something went wrong during CSV upload!")

    return redirect("admin_addStudent")

#Reports
from django.db.models import Count

def admin_Reports(request):
    login_id = request.session.get("login_id")
    if not login_id:
        return redirect("/")

    admin = Admin.objects.get(login_id=login_id)

    return render(request, "Admin/admin_reports.html", {
        "admin": admin
    })
    
    
def search_entities(request):
    q = request.GET.get("q", "")
    mode = request.GET.get("mode")

    if mode == "student":
        results = Student.objects.filter(name__icontains=q)[:10]
        data = [
            {"id": s.student_id, "label": f"{s.name} ({s.reg_no})"}
            for s in results
        ]

    elif mode == "faculty":
        results = Faculty.objects.filter(name__icontains=q)[:10]
        data = [
            {"id": f.faculty_id, "label": f.name}
            for f in results
        ]

    else:  # batch
        results = Batches.objects.filter(batch_name__icontains=q)[:10]
        data = [
            {"id": b.batch_id, "label": b.batch_name}
            for b in results
        ]

    return JsonResponse({"results": data})
def fetch_report_data(request):
    report_type = request.GET.get("type")
    record_id = request.GET.get("id")
    time_range = request.GET.get("range")
    
    print("TYPE:", report_type)
    print("RECORD ID (raw):", record_id, type(record_id))
    print("RANGE:", time_range)

    qs = MentoringSession.objects.all()

    # -------- ENTITY FILTER --------
    if report_type == "student":
        qs = qs.filter(student__student_id=int(record_id))

    elif report_type == "faculty":
        qs = qs.filter(faculty__faculty_id=int(record_id))

    elif report_type == "batch":
        qs = qs.filter(student__batch__batch_id=int(record_id))

    # -------- DATE FILTER --------
    today = today = timezone.localdate()

    if time_range == "daily":
        from django.utils.timezone import localdate
        qs = qs.filter(date__date=localdate())

    elif time_range == "monthly":
        qs = qs.filter(
            date__month=today.month,
            date__year=today.year
        )

    # -------- METRICS --------
    total_sessions = qs.count()
    students = qs.values("student").distinct().count()
    faculty = qs.values("faculty").distinct().count()

    # -------- CHART DATA --------
    chart_qs = (
        qs.values("date")
        .annotate(count=Count("session_id"))
        .order_by("date")
    )

    return JsonResponse({
        "total_sessions": total_sessions,
        "total_students": students,
        "total_faculty": faculty,
        "avg_sessions": round(
            total_sessions / max(students, 1), 2
        ),
        "chart": {
            "labels": [str(c["date"]) for c in chart_qs],
            "values": [c["count"] for c in chart_qs]
        }
    })
    
def generate_report_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename=Mentoring_Report.pdf"

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph("<b>MENTORING PROGRAMME REPORT</b>", styles["Title"])
    )
    elements.append(Spacer(1, 20))
    elements.append(
        Paragraph("Generated by Mentor Mentee System", styles["Normal"])
    )
    elements.append(
        Paragraph(f"Date: {date.today()}", styles["Normal"])
    )

    doc.build(elements)
    return response


#Admin View Sessions
def admin_viewSessions(request):
    try:
        login_id = request.session.get("login_id")
        if not login_id:
            return redirect('/')
        admin = Admin.objects.get(login_id=login_id)
        dept = admin.department_id
        batches = Batches.objects.filter(course__department_id=dept)
        faculties = Faculty.objects.filter(department_id=dept)
        students = Student.objects.filter(department_id=dept)
        sessions = Schedule.objects.filter(batch__course__department_id=dept)
    except Exception as e:
        print(f"Error! {e}")
    return render(request, './Admin/admin_viewSessions.html',
                  {"batches": batches, "faculties": faculties, "students": students,"admin":admin,"sessions": sessions})
    
#Admin edit session
from django.shortcuts import redirect
from django.http import HttpResponse
from datetime import date
from django.core.mail import send_mail

def admin_updateSession(request):
    if request.method == "POST":
        try:
            login_id = request.session.get("login_id")
            if not login_id:
                return redirect('/')

            schedule_id = request.POST.get("schedule_id")
            new_start = request.POST.get("start_date")
            new_end = request.POST.get("end_date")
            new_status = request.POST.get("status")

            if new_start > new_end:
                return HttpResponse(
                    "<script>alert('Invalid date range');window.location.href='/admin_viewSessions'</script>"
                )

            # 🔹 Fetch existing schedule
            schedule = Schedule.objects.select_related('batch').get(schedule_id=schedule_id)

            old_start = str(schedule.start_date)
            old_end = str(schedule.end_date)

            # 🔹 Update schedule
            Schedule.objects.filter(schedule_id=schedule_id).update(
                start_date=new_start,
                end_date=new_end,
                status=new_status
            )

            # 🔹 Send mail ONLY if dates changed
            if old_start != new_start or old_end != new_end and new_status == 'active' or new_status == 'incomplete':
                batch_email = schedule.batch.batch_mail
                batch_name = schedule.batch.batch_name

                mail_subject = "Update: Mentoring Session Schedule Changed"

                mail_body = f"""
Dear Students,

Greetings of the day!

Please note that the mentoring session schedule for your batch
({batch_name}) has been updated.

Previous Schedule:
    From: {old_start}
    To  : {old_end}

Revised Schedule:
    From: {new_start}
    To  : {new_end}

Kindly take note of the revised dates and plan accordingly.

Regards,
Mentor-Mentee Coordination Team
"""

                send_mail(
                    subject=mail_subject,
                    message=mail_body,
                    from_email="noreply.mentormentee@gmail.com",
                    recipient_list=[batch_email],
                    fail_silently=False,
                )

            return HttpResponse(
                "<script>alert('Session updated successfully!');window.location.href='/admin_viewSessions'</script>"
            )

        except Exception as e:
            print("Update session error:", e)
            return HttpResponse(
                "<script>alert('Something went wrong');window.location.href='/admin_viewSessions'</script>"
            )

    return redirect('/admin_viewSessions')


#===============================================================================================


##FACULTY SIDE VIEWS##

def faculty_dashboard(request):
    login_id = request.session.get('login_id')
    if not login_id:
        return redirect('home')

    faculty = get_object_or_404(Faculty, login_id=login_id)
    dept = faculty.department
    today = date.today()

    active_sessions = Schedule.objects.filter(
        batch__course__department=dept,
        start_date__lte=today,
        end_date__gte=today
    )

    pending_sessions = Schedule.objects.filter(
        batch__course__department=dept,
        start_date__gt=today
    )

    missed_sessions = Schedule.objects.filter(
        batch__course__department=dept,
        end_date__lt=today
    )

    return render(request, 'Faculty/faculty_dashboard.html', {
        'faculty': faculty,
        'active_sessions': active_sessions,
        'pending_sessions': pending_sessions,
        'missed_sessions': missed_sessions,
    })

def students_content(request):
    session_login = request.session.get('login_id')
    session_login_name = request.session.get('faculty_name')
    if not session_login:
        return redirect('/')  # not logged in

    try:
        faculty = Faculty.objects.get(login_id=session_login)
    except Faculty.DoesNotExist:
        return HttpResponse("<script>alert('Invalid session.'); window.location.href='/'</script>")

    students = Student.objects.filter(faculty_id=faculty.faculty_id)
    departments = Department.objects.all()
    courses = Courses.objects.all()
    batches = Batches.objects.all()
    last_session = MentoringSession.objects.filter(faculty=faculty).order_by('-date').first()
    

    context = {
        'students': students,
        'departments': departments,
        'courses': courses,
        'batches': batches,
        'faculty': faculty,
        'name': session_login_name,
        'last_session_date': last_session.date if last_session else None,
    }
    return render(request, 'Faculty/students-content.html', context)

def student_profile(request, student_id):
    login_id = request.session.get('login_id')
    if not login_id:
        return redirect('home')

    faculty = get_object_or_404(Faculty, login_id=login_id)
    student = get_object_or_404(Student, student_id=student_id)

    context = {
        'faculty': faculty,   # logged-in faculty
        'student': student,
    }

    return render(request, 'Faculty/student_profile.html', context)


from django.core.files.storage import FileSystemStorage
import os

def profile_content(request):
    login_id = request.session.get('login_id')
    if not login_id:
        return redirect('/')

    faculty = get_object_or_404(Faculty, login_id=login_id)
    students = Student.objects.filter(faculty_id=faculty.faculty_id)

    # ------- UPDATE PROFILE PART -------
    if request.method == 'POST':
        faculty.name = request.POST.get('name')
        faculty.email = request.POST.get('email')
        faculty.phone = request.POST.get('phone')
        faculty.designation = request.POST.get('designation')

        # File upload (FACULTY)
        if "faculty_image" in request.FILES:
            image_file = request.FILES["faculty_image"]

            upload_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'static',
                'faculty_images'
            )

            fs = FileSystemStorage(
                location=upload_path,
                base_url='/static/faculty_images/'
            )

            filename = fs.save(image_file.name, image_file)
            faculty.faculty_image = filename   # ✅ correct field

        faculty.save()
        return redirect('profile_content')

    # 🔵 TOTAL mentoring sessions taken by this faculty
    total_mentoring = MentoringSession.objects.filter(
        faculty=faculty
    ).count()

    return render(request, 'Faculty/profile-content.html', {
        'faculty': faculty,
        'students': students,
        'total_mentoring': total_mentoring,
    })

def filter_students(request):
    faculty_login_id = request.session.get('login_id')
    if not faculty_login_id:
        return JsonResponse({"error": "Session expired"}, status=403)

    try:
        faculty = Faculty.objects.get(login_id=faculty_login_id)
        students = Student.objects.filter(faculty_id=faculty.faculty_id)
    except Faculty.DoesNotExist:
        return JsonResponse({"error": "Invalid faculty"}, status=403)

    dept = request.GET.get('department')
    course = request.GET.get('course')
    batch = request.GET.get('batch')
    

    # Only students assigned to this faculty
    students = Student.objects.filter(faculty_id=faculty.faculty_id)

    if dept and dept.isdigit():
        students = students.filter(department_id=int(dept))
    if course and course.isdigit():
        students = students.filter(course_id=int(course))
    if batch and batch.isdigit():
        students = students.filter(batch__batch_id=batch)

    data = []
    for s in students:
        data.append({
            "student_id": s.student_id,
            "name": s.name,
            "reg_no": s.reg_no,
            "department_name": s.department.name,
            "batch_name": s.batch.batch_name,
            'course_name': s.course.course_name,
        })

    return JsonResponse({"students": data})

def student_session(request, id):
    student = Student.objects.get(student_id=id)
    sessions = MentoringSession.objects.filter(student__student_id=id).order_by('-date')
    student_uploads = StudentUploads.objects.filter(student=student)
    return render(request, 'Faculty/student_sessions.html', {
        'student': student,
        'sessions': sessions,
        'student_uploads': student_uploads,
    })

from django.contrib import messages
    
def upload_application(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST" and request.FILES.get('application_form'):
        student.application_form = request.FILES['application_form']
        student.save()
        messages.success(request, "Application Form uploaded successfully.")

    return redirect('student_session', id=id)


def upload_assessment(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST" and request.FILES.get('assessment_file'):
        student.assessment_file = request.FILES['assessment_file']
        student.save()
        messages.success(request, "Assessment File uploaded successfully.")

    return redirect('student_session', id=id)


from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

def new_session(request, id):
    student = get_object_or_404(Student, student_id=id)

    previous_sessions = MentoringSession.objects.filter(
        student=student
    ).order_by('date')

    is_first_session = not previous_sessions.exists()

    # Defaults for GET
    demography = ''
    personal = ''

    # If NOT first session → load from first session
    if not is_first_session:
        first_session = previous_sessions.first()
        demography = first_session.demography or ''
        personal = first_session.personal or ''

    if request.method == "POST":
        title = request.POST.get("title")
        academic_details = request.POST.get("academic_details")
        emotional_details = request.POST.get("emotional_details")
        other_details = request.POST.get("other_details")
        followup_actions = request.POST.get("followup_actions")

        # FIRST SESSION → read from form
        if is_first_session:
            demography = request.POST.get("demography", "")
            personal = request.POST.get("personal", "")

        MentoringSession.objects.create(
            student=student,
            faculty=student.faculty,
            title=title,
            academic_details=academic_details,
            emotional_details=emotional_details,
            other_details=other_details,
            followup_actions=followup_actions,
            demography=demography,
            personal=personal,
            date=timezone.now()
        )

        return redirect('student_session', id=id)

    return render(request, 'Faculty/new_session.html', {
        'student': student,
        'previous_sessions': previous_sessions.order_by('-date'),
        'is_first_session': is_first_session,
        'demography': demography,
        'personal': personal,
    })



def session_details(request, id):
    session = get_object_or_404(MentoringSession, id=id)

    return render(request, 'session_details.html', {
        'session': session,
        'student': session.student,
    })

def view_session(request, session_id):
    session = MentoringSession.objects.get(session_id=session_id)
    return render(request, 'Faculty/view_session.html', {'session': session})

def faculty_session_requests(request):
    login_id = request.session.get('login_id')
    if not login_id:
        return redirect('home')

    faculty = get_object_or_404(Faculty, login_id=login_id)

    # Only requests meant for THIS faculty
    requests = SessionRequest.objects.filter(
        faculty=faculty
    ).order_by('-request_date')

    return render(request, 'Faculty/session_requests.html', {
        'requests': requests,
        'faculty': faculty,
    })

from django.views.decorators.http import require_POST

@require_POST
def accept_session_request(request, request_id):
    login_id = request.session.get('login_id')
    if not login_id:
        return redirect('home')

    faculty = get_object_or_404(Faculty, login_id=login_id)

    session_request = get_object_or_404(
        SessionRequest,
        request_id=request_id,
        faculty=faculty   # SECURITY: only own requests
    )

    session_request.session_date = request.POST.get('session_date')
    session_request.session_time = request.POST.get('session_time')
    session_request.status = 'Accepted'
    session_request.save()

    return redirect('faculty_session_requests')

from django.views.decorators.http import require_POST

@require_POST
def reject_session_request(request, request_id):
    login_id = request.session.get('login_id')
    if not login_id:
        return redirect('home')

    faculty = get_object_or_404(Faculty, login_id=login_id)

    session_request = get_object_or_404(
        SessionRequest,
        request_id=request_id,
        faculty=faculty,
        status="pending"
    )

    session_request.status = "Rejected"
    session_request.save()

    return redirect('faculty_session_requests')

# Faculty - View All Students (Department-wise)
def faculty_ViewStudents(request):
    login_id = request.session.get('login_id')
    if not login_id:
        return HttpResponse(
            "<script>alert('Session expired! Please login again.'); window.location.href='/'</script>"
        )

    try:
        faculty = Faculty.objects.get(login_id=login_id)

        # Fetch department-wise data (same as Admin)
        batches = Batches.objects.filter(
            course__department=faculty.department
        )

        courses = Courses.objects.filter(
            department=faculty.department
        )

        students = Student.objects.filter(
            department=faculty.department
        )

        context = {
            'faculty': faculty,
            'students': students,
            'batches': batches,
            'courses': courses,
        }

        return render(request, 'Faculty/view_students.html', context)

    except Faculty.DoesNotExist:
        return redirect('home')

#==============================================================================================


# Student Views

def signup(request):
    contents={}
    try:
        department=Department.objects.all()
        batches=Batches.objects.all()
        courses=Courses.objects.all()
        contents={'departments':department,'courses':courses,'batches':batches}
        if request.method == 'POST':
            name = request.POST['name']
            reg_no = request.POST['reg_no']
            email = request.POST['email']
            phone = request.POST['phone']
            dob = request.POST['dob']
            department = request.POST['department']
            course = request.POST['course']
            batch = request.POST['batch']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            photo = request.FILES['photo']
            application_form = request.FILES['application_form']
            #Password and EMail Validation
            if password != confirm_password:
                 return HttpResponse("<script>alert('Passwords Unmatch!'); window.location.href='/signup'</script>")
            
            #Student Image
            photo_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'static',
                'student_images'
            )
            fs = FileSystemStorage(location=photo_path, base_url='../static/student_images/')
            st_image = fs.save(photo.name, photo)
            
            #Application Form
            # app_path = os.path.join(
            #     os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            #     'static',
            #     'Application_Forms'
            # )
            # fs = FileSystemStorage(location=app_path, base_url='../static/Application_Forms/')
            # app_form = fs.save(application_form.name, application_form)
            #Login
            res1=Login(username=reg_no,password=password,userType='student')
            res1.save()
            res2=Student(
                        login_id=res1.login_id,
                        name=name,
                        email=email,
                        reg_no=reg_no,
                        phone=phone,
                        department_id=department,
                        course_id=course,
                        batch_id=batch,
                        year=1,
                        dob=dob,
                        student_image=st_image,
                        application_form=application_form,
                        )
            res2.save()
            return HttpResponse("<script>alert('Account created successfully. Login to continue :)'); window.location.href='/'</script>")
            
    except Exception as e:
        print(f"Error! {e}")
    return render(request,'Student_SignUp.html',contents)

# Student Dashboard
def student_dashboard(request):
    session_login = request.session.get("login_id")
    
    student = Student.objects.get(login_id=session_login)
    dept = student.department

    today = date.today()

    active_sessions = Schedule.objects.filter(
        batch__course__department=dept,
        start_date__lte=today,
        end_date__gte=today
    )

    pending_sessions = Schedule.objects.filter(
        batch__course__department=dept,
        start_date__gt=today
    )

    missed_sessions = Schedule.objects.filter(
        batch__course__department=dept,
        end_date__lt=today
    )

    return render(request, "./Student/student_dashboard.html", {
        "student": student,
        "active_sessions": active_sessions,
        "pending_sessions": pending_sessions,
        "missed_sessions": missed_sessions,
    })

#Dashboard Calendar
def student_api_get_sessions(request):
    student = Student.objects.get(login_id=request.session["login_id"])
    dept = student.department
    schedules = Schedule.objects.filter(batch__course__department=dept)
    events = []
    for s in schedules:
        events.append({
            "title": s.batch.batch_name,
            "start": str(s.start_date),
            "end": str(s.end_date + timedelta(days=1))
        })
    return JsonResponse(events, safe=False)

# API: Get sessions for a specific day
def student_api_get_day_sessions(request, date_str):
    try:
        session_login = request.session.get("login_id")
        student = Student.objects.get(login_id=session_login)
        dept = student.department
        selected_date = date.fromisoformat(date_str)

        # Sessions where this date is between start and end
        sessions = Schedule.objects.filter(
            batch__course__department=dept,
            start_date__lte=selected_date,
            end_date__gte=selected_date
        )
        data = [
            {
                "batch": s.batch.batch_name,
                "status": s.status,
                "start_date": str(s.start_date),
                "end_date": str(s.end_date),
            }
            for s in sessions
        ]
        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
    #Student Request Session
def student_RequestSession(request):
    contents={}
    login_id = request.session.get('login_id')
    if not login_id:
        return HttpResponse(
            "<script>alert('Session expired! Please login again.'); window.location.href='/'</script>")
    try:
        student=Student.objects.get(login_id=login_id)
        contents={'student':student}
        
        if request.method == 'POST':
            request_date_str = request.POST['request_date']
            reason = request.POST['reason']
            status = 'Pending'
            request_date = datetime.strptime(request_date_str, "%Y-%m-%d").date()
            if request_date < date.today():
                return HttpResponse(
            "<script>alert('Invalid date selection!'); window.location.href='/student_RequestSession'</script>")
            res = SessionRequest(
                request_date=request_date_str,
                status = status,
                faculty_id = student.faculty_id,
                student_id=student.student_id,
                comments = reason
                )
            res.save()
            return HttpResponse(
            "<script>alert('Request sent successfully'); window.location.href='/student_dashboard'</script>")
    except Exception as e:
        print(f"Error! {e}")
        return HttpResponse(
            "<script>alert('Request failed! Try Again'); window.location.href='/student_dashboard'</script>")
    return render(request,'./Student/student_RequestSession.html',contents)

#Student Profile
def student_Profile(request):
    contents={}
    login=request.session.get('login_id')
    if not login:
        return HttpResponse(
            "<script>alert('Session expired! Please login again.'); window.location.href='/'</script>")
    try:
        student=Student.objects.get(login_id=login)
        contents={'student':student}
    except Exception as e:
        print(f"Error! {e}")
    return render(request,'./Student/student_profile.html',contents)

#Student Uploads
def student_uploads(request):
    contents={}
    login_id = request.session.get('login_id')
    if not login_id:
        return HttpResponse(
            "<script>alert('Session expired! Please login again.'); window.location.href='/'</script>")
    try:
        student=Student.objects.get(login_id=login_id)
        uploads=StudentUploads.objects.filter(student_id=student.student_id)
        contents={'student':student,'uploads':uploads}
        if request.method == "POST":
                file_name = request.POST.get("file_name")
                description = request.POST.get("description")
                upload_file = request.FILES.get("upload_file")
                # Save directly using FileField
                res = StudentUploads(
                    student=student,
                    file_name=file_name,
                    upload_file=upload_file,
                    description=description
                )
                res.save()
                return HttpResponse(
                    "<script>alert('File uploaded successfully!'); window.location.href='/student_uploads'</script>")
    except Exception as e:
        print(f"Error! {e}")
    return render(request,'./Student/student_uploads.html',contents)

# Student – View Sessions
def student_viewSessions(request):
    login_id = request.session.get("login_id")
    if not login_id:
        return redirect("/")

    try:
        student = Student.objects.get(login_id=login_id)

        requests = SessionRequest.objects.filter(
            student=student).select_related("faculty").order_by("request_date")

        context = {
            "student": student,
            "requests": requests
        }

        return render(
            request,
            "./Student/student_viewSessions.html",
            context
        )

    except Exception as e:
        print("Student requested sessions error:", e)
        return redirect("/")
    
#Student edit profile
def student_update_profile(request):
    try:
        login_id = request.session.get("login_id")
        if not login_id:
            return redirect("/")

        student = Student.objects.get(login_id=login_id)
        if request.method == "POST":
            student = Student.objects.get(login_id=request.session["login_id"])

            student.email = request.POST.get("email")
            student.phone = request.POST.get("phone")
            student.dob = request.POST.get("dob")

            if "student_image" in request.FILES:
                student.student_image = request.FILES["student_image"]
            student.save()
            
            return HttpResponse(
                "<script>alert('Profile updated successfully!'); window.location.href='/student_profile'</script>")
    except Exception as e:
        print(f"Error{e}")
        return HttpResponse(
            "<script>alert('Error updating profile!'); window.location.href='/student_profile'</script>")
    return redirect("/student_profile") 

def test_mail(request):
    try:
        send_mail(
            subject="Mail from Mentor-Mentee System",
            message="Gentle reminder. This is to inform you that you have not completed your 1st mentoring session yet. You are asked to meet your mentor now itself along with a apology letter. Avoidance will result in expelling you from the institution.",
            from_email="noreply.mentormentee@gmail.com",   # SAME as EMAIL_HOST_USER
            recipient_list=["mca2531@rajagiri.edu"],  # you will receive the test mail
            fail_silently=False,
        )
        return HttpResponse("Email sent successfully!")
    except Exception as e:
        return HttpResponse(f"Error sending email: {e}")
    
    