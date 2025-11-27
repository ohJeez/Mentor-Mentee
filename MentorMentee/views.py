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
            application = request.FILES['application_form']
            assessment = request.FILES['assessment_file']

            photo_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'static',
                'student_images'
            )

            fs = FileSystemStorage(location=photo_path, base_url='../static/student_images/')
            image = fs.save(photo.name, photo)
            
            #Application form
            application_path = os.path.join(BASE_DIR, 'static', 'student_applications')
            fs_app = FileSystemStorage(location=application_path, base_url='../static/student_applications/')
            saved_application_name = fs_app.save(application.name, application)
            #Assessment 
            assessment_path = os.path.join(BASE_DIR, 'static', 'student_assessment')
            fs_assessment = FileSystemStorage(location=assessment_path, base_url='../static/student_assessment/')
            saved_assessment_name = fs_assessment.save(assessment.name, assessment)


            res=Student(
                name=name,
                email=email,
                reg_no=roll,
                phone=phone,
                department_id=admin_det.department_id,
                batch_id=batch,
                course_id=course,
                student_image=image,
                year=1,
                application_form=saved_application_name,
                assessment_form = saved_assessment_name,
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
        courses=Courses.objects.filter(department_id=adm_dept.department_id)
        #all students
        students=Student.objects.filter(department_id=adm_dept.department_id)
        contents={'batches':batches,'students':students,'admin':adm_dept,'courses':courses}
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
                admin_imag = request.POST['admin_image']
                photo_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'static',
                'faculty_images'
            )
            fs = FileSystemStorage(location=photo_path, base_url='../static/faculty_images/')
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

def admin_Reports(request):
    contents={}
    try:
        login_id = request.session.get("login_id")
        if not login_id:
            return redirect("/")
        admin=Admin.objects.get(login_id=login_id)
        faculty = Faculty.objects.filter(department_id=admin.department_id)
        students = Student.objects.filter(department_id=admin.department_id)
        batches = Batches.objects.filter(course__department_id=admin.department_id)

        contents = {
            "admin": admin,
            "faculty": faculty,
            "students": students,
            "batches": batches
        }
    except Exception as e:
        print(f"Error! {e}")
    return render(request,'./Admin/admin_reports.html',contents)

def filter_sessions(request):
    report_type = request.GET.get("type")
    record_id = request.GET.get("id")
    time_range = request.GET.get("range")
    start = request.GET.get("start")
    end = request.GET.get("end")

    sessions = MentoringSession.objects.all()

    # FILTER: TYPE
    if report_type == "student":
        sessions = sessions.filter(student_id=record_id)

    elif report_type == "faculty":
        sessions = sessions.filter(faculty_id=record_id)

    elif report_type == "batch":
        sessions = sessions.filter(student__batch_id=record_id)

    # FILTER: TIME RANGE
    today = date.today()

    if time_range == "daily":
        sessions = sessions.filter(session_date=today)

    elif time_range == "weekly":
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)
        sessions = sessions.filter(session_date__range=[start_week, end_week])

    elif time_range == "monthly":
        sessions = sessions.filter(session_date__month=today.month)

    elif time_range == "custom" and start and end:
        sessions = sessions.filter(session_date__range=[start, end])

    # RETURN JSON FOR TABLE
    data = [
        {
            "date": str(s.session_date),
            "student": s.student.name,
            "faculty": s.faculty.name,
            "batch": s.student.batch.batch_name,
            "topics": s.topics_discussed,
            "remarks": s.remarks or "",
        }
        for s in sessions
    ]

    return JsonResponse({"sessions": data})

def generate_report_pdf(request):
    report_type = request.GET.get("type")
    record_id = request.GET.get("id")
    time_range = request.GET.get("range")
    start = request.GET.get("start")
    end = request.GET.get("end")

    # Fetch JSON data from filter function
    filtered = filter_sessions(request)
    response_data = json.loads(filtered.content)
    sessions = response_data.get("sessions", [])

    # Create PDF Response
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename=Mentoring_Report.pdf"

    pdf = SimpleDocTemplate(response, pagesize=A4,
                            rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)

    styles = getSampleStyleSheet()
    elements = []

    # -------------------- HEADER --------------------
    logo_path = os.path.join(settings.BASE_DIR, "static", "Assets", "logo.png")
    if os.path.exists(logo_path):
        elements.append(Image(logo_path, width=60, height=60))
        elements.append(Spacer(1, 10))

    title = Paragraph("<b>MENTORING SESSION REPORT</b>", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 10))

    # Get Display Label
    detail_label = ""
    if report_type == "student" and record_id:
        from MentorMentee.models import Student
        detail_label = f"Student: {Student.objects.get(student_id=record_id).name}"
    elif report_type == "faculty" and record_id:
        from MentorMentee.models import Faculty
        detail_label = f"Faculty: {Faculty.objects.get(faculty_id=record_id).name}"
    elif report_type == "batch" and record_id:
        from MentorMentee.models import Batches
        detail_label = f"Batch: {Batches.objects.get(batch_id=record_id).batch_name}"

    header_details = f"""
        <b>Report Type:</b> {report_type.capitalize()}<br/>
        <b>{detail_label}</b><br/>
        <b>Date Range:</b> {time_range.capitalize()}
    """

    elements.append(Paragraph(header_details, styles["Normal"]))
    elements.append(Spacer(1, 20))

    # -------------------- TABLE --------------------

    # Wrap each cell value to avoid overflow
    def wrap(text):
        return Paragraph(str(text), styles["BodyText"])

    table_data = [
        [
            wrap("Date"),
            wrap("Student"),
            wrap("Faculty"),
            wrap("Batch"),
            wrap("Topics Discussed"),
            wrap("Remarks")
        ]
    ]

    for s in sessions:
        table_data.append([
            wrap(s["date"]),
            wrap(s["student"]),
            wrap(s["faculty"]),
            wrap(s["batch"]),
            wrap(s["topics"]),
            wrap(s["remarks"]),
        ])

    # Better column widths
    col_widths = [70, 80, 80, 60, 150, 120]

    table = Table(table_data, colWidths=col_widths)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#28a745")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.7, colors.grey),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    footer = Paragraph("<i>Generated by Mentor Mentee System</i>", styles["Italic"])
    elements.append(footer)

    pdf.build(elements)

    return response