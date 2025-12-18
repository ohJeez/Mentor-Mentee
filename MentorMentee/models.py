from django.db import models
from django.utils import timezone

    #Login
class Login (models.Model):
    login_id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=25)
    password=models.CharField(max_length=20)
    userType=models.CharField(max_length=10,default='faculty')

    # Departments
class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    hod_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    #Courses
class Courses(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    #Batches
class Batches(models.Model):
    batch_id = models.AutoField(primary_key=True)
    batch_name = models.CharField(max_length=30,blank=True)
    course = models.ForeignKey(Courses,on_delete=models.CASCADE)
    batch_mail = models.EmailField(max_length=150,db_index=False,blank=True,null=True)
    
    
    #Admin
class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    login=models.ForeignKey(Login,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150,db_index=False)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    admin_image = models.CharField(max_length=500,blank=True)

    #Faculty
class Faculty(models.Model):
    faculty_id = models.AutoField(primary_key=True)
    login=models.ForeignKey(Login,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150,db_index=False)
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="faculties")
    designation = models.CharField(max_length=100, blank=True, null=True)
    faculty_image = models.CharField(max_length=500,blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    
    #Student
class Student(models.Model):
    login = models.ForeignKey(Login, on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150,db_index=False)
    reg_no = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="students")
    student_image = models.FileField(blank=True,null=True,upload_to='student_images/')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batches,on_delete=models.CASCADE)
    year = models.IntegerField()
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name="students")
    dob = models.DateField(null=True, blank=True)
    application_form = models.FileField(upload_to='application_forms/', null=True, blank=True)
    assessment_file = models.FileField(upload_to='assessments/', null=True, blank=True)
    
    # Mentoring Session
class MentoringSession(models.Model):
    session_id = models.AutoField(primary_key=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='sessions')
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField(default=timezone.now)  # automatically set to now
    title = models.TextField(blank=False, null=True)
    academic_details = models.TextField(blank=False, null=True)
    demography = models.TextField(blank=True, null=True)  # first session only
    personal = models.TextField(blank=True, null=True)    # first session only
    emotional_details = models.TextField(blank=True, null=True)
    other_details = models.TextField(blank=True, null=True)
    followup_actions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.name} - {self.title} ({self.date.strftime('%d-%m-%Y')})"

    #MentorAssignments
class MentorAssignmentLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    old_faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name="old_assignments")
    new_faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name="new_assignments")
    changed_by = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    #Scheduling Sessions
class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    batch = models.ForeignKey(Batches,on_delete=models.CASCADE)
    created_by = models.ForeignKey(Admin,on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=25,default="Active",choices=[
        ("active","Active"),
        ("completed","Completed"),
        ("incomplete","Incomplete"),
        ("cancelled","Cancelled")
        ])
    created_at = models.DateField(auto_now_add=True)
    
    #Session Requests
class SessionRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    request_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=25,default="Pending",choices=[
        ("pending","Pending"),
        ("accepted","Accepted"),
        ("completed","Completed"),
        ("rejected","Rejected"),
        ("cancelled","Cancelled")
        ])
    session_date = models.DateField(null=True,blank=True)
    session_time = models.TimeField(null=True,blank=True)
    comments = models.CharField(max_length=200,blank=True,null=True)
    
    #Student Uploads
class StudentUploads(models.Model):
    upload_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    file_name = models.CharField(max_length=100,blank=True,null=True)
    upload_file = models.FileField(upload_to='student_uploads/',max_length=500)
    description = models.CharField(max_length=200,blank=True,null=True)
    def file_type(self):
        ext = str(self.upload_file.name).lower()
        if ext.endswith(".pdf"):
            return "pdf"
        return "image"
    
    #Faculty Assignments
class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )