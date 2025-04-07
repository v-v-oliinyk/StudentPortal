from django.db import models

class Auditing(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

class User(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='student')
    email = models.EmailField(unique=True, default='example@gmail.com')
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='users_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.surname} {self.name}"

class Cohort(Auditing):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Subject(Auditing):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey("Teacher", on_delete=models.SET_NULL, null=True, related_name="subjects")
    cohorts = models.ManyToManyField(Cohort, related_name="subjects")

    def __str__(self):
        return self.name

class LessonData(Auditing):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="lessons")
    location = models.CharField(max_length=255)
    start_at = models.DateTimeField()

    def __str__(self):
        return f"{self.subject.name} at {self.location} on {self.start_at}"

class Teacher(Auditing):
    pass
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#
#     def __str__(self):
#         return f"Teacher: {self.user.surname} {self.user.name}"

class Student(Auditing):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cohort = models.ForeignKey(Cohort, on_delete=models.SET_NULL, null=True, related_name="students")
    subjects = models.ManyToManyField(Subject, related_name="students")

    def __str__(self):
        return f"Student: {self.user.surname} {self.user.name}"


class Grade(Auditing):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="grades")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="grades")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name="given_grades")
    value = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.surname} - {self.subject.name}: {self.value}"