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
                return render(request,'Faculty/home.html',{'name':data.name})
            else:
                return HttpResponse("<script>alert('Invalid Login Credentials!');</script>")

        except Exception as e:
            print(f"{e}")
            return HttpResponse("<script>alert('Invalid Login Credentials!');</script>")
            
    return render(request,'Login.html',) 