from django.db import models
from django.utils import timezone


# =================================================
# LOGIN (AUTH ONLY)
# =================================================
class Login(models.Model):
    login_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=8)
    userType = models.CharField(
        max_length=20,
        default='faculty'
    )

    def __str__(self):
        return self.username


# =================================================
# DEPARTMENT (TENANT)
# =================================================
class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    hod_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =================================================
# COURSES
# =================================================
class Courses(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.course_name


# =================================================
# BATCHES
# =================================================
class Batches(models.Model):
    batch_id = models.AutoField(primary_key=True)
    batch_name = models.CharField(max_length=30, blank=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):
        return self.batch_name


# =================================================
# ADMIN (LEGACY – DO NOT USE FOR NEW LOGIC)
# =================================================
class Admin(models.Model):
    """
    ⚠ LEGACY TABLE
    Kept only for DB compatibility with teammates.
    DO NOT use this for role checks.
    """
    admin_id = models.AutoField(primary_key=True)
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    admin_image = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name


# =================================================
# FACULTY (REAL USER + ROLE HOLDER)
# =================================================
class Faculty(models.Model):
    faculty_id = models.AutoField(primary_key=True)
    login = models.ForeignKey(Login, on_delete=models.CASCADE)

    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="faculties"
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length=15, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    faculty_image = models.ImageField(
        upload_to='faculty_images/', null=True, blank=True
    )

    # ✅ REAL ROLE FLAGS (USE THESE)
    is_superadmin = models.BooleanField(default=False)  # HOD
    is_admin = models.BooleanField(default=False)       # Admin

    def __str__(self):
        return self.name


# =================================================
# STUDENT
# =================================================
class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    reg_no = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="students"
    )

    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batches, on_delete=models.CASCADE)
    year = models.IntegerField()

    faculty = models.ForeignKey(
        Faculty, on_delete=models.SET_NULL, null=True, related_name="students"
    )

    dob = models.DateField(null=True, blank=True)

    application_form = models.FileField(
        upload_to='application_forms/', null=True, blank=True
    )
    assessment_file = models.FileField(
        upload_to='assessments/', null=True, blank=True
    )

    def __str__(self):
        return self.name


# =================================================
# MENTORING SESSION (KEEP `date` – SHARED DB SAFE)
# =================================================
class MentoringSession(models.Model):
    session_id = models.AutoField(primary_key=True)

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='sessions'
    )
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, related_name='sessions'
    )

    # ⚠ KEEP NAME AS `date` (DO NOT RENAME)
    date = models.DateTimeField(default=timezone.now)

    title = models.TextField(blank=True, null=True)
    academic_details = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Session {self.session_id}"


# =================================================
# MENTOR ASSIGNMENT LOG (SAFE)
# =================================================
class MentorAssignmentLog(models.Model):
    log_id = models.AutoField(primary_key=True)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    old_faculty = models.ForeignKey(
        Faculty, on_delete=models.SET_NULL,
        null=True, related_name="old_assignments"
    )
    new_faculty = models.ForeignKey(
        Faculty, on_delete=models.SET_NULL,
        null=True, related_name="new_assignments"
    )

    # ⚠ Do NOT depend on Admin table long-term
    changed_by = models.ForeignKey(
        Faculty, on_delete=models.SET_NULL,
        null=True
    )

    timestamp = models.DateTimeField(auto_now_add=True)
