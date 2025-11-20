from django.shortcuts import render
from django.http import *
from . models import *

# Create your views here.
def home(request):
    if request.method =='POST':
        uname = request.POST['uname']
        pas = request.POST['password']
        print(uname)
        try:
            res= Login.objects.get(username=uname,password=pas)
            if res and res.userType == 'faculty':
                data=Faculty.objects.get(login_id=res.login_id)
                return render(request,'./Faculty/index.html',{'name':data.name})
            elif res and res.userType == 'admin':
                admin_details=Admin.objects.get(login_id=res.login_id)
                total_students=Student.objects.filter(department_id=admin_details.department_id).count()
                total_mentors=Faculty.objects.filter(department_id=admin_details.department_id).count()
                # debugging
                print(f"Total Students: {total_students}")
                print(f"Total Mentors: {total_mentors}")
                print(f"Login:{res.login_id}")
                data={'total_students':total_students,'total_mentors':total_mentors,'login':res.login_id}
                return render(request,'./Admin/admin.html',data)
            else:
                return HttpResponse("<script>alert('Invalid Login Credentials!');</script>")

        except Exception as e:
            print(f"{e}")
            return HttpResponse("<script>alert('Invalid Login Credentials!');</script>")
            
    return render(request,'Login.html',) 


def admin_dashboard(request):
    return render(request,'./Admin/admin_dashboard.html')

#StudentList
def students_List(request,login):
    try:
        admin_det=Admin.objects.get(login_id=login)
        print(f"admin_dept:{admin_det.department_id}")
        students = Student.objects.select_related("department","course").filter(department_id=admin_det.department_id)

        content={'students':students}
        print(students)
    except Exception as e:
        print(f"Error: {e}")
    return render(request,'./Admin/view_students.html',content)