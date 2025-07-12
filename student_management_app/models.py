from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class CustomUser(AbstractUser):
    user_type_data=((1,"HOD"),(2,"Student"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)

class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True)
    course_name = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    enrolled = models.PositiveIntegerField(default=0)
    classroom = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()

    days_choice=(
        ("Monday","Monday"),
        ("Tuesday","Tuesday"),
        ("Wednesday","Wednesday"),
        ("Thursday","Thursday"),
        ("Friday","Friday")
    )
    days = models.CharField(default = "Monday",max_length=10,choices=days_choice)  # e.g., "MWF" or "TTh"

    def __str__(self):
        return f"{self.classroom} - {self.course_code} - {self.course_name} - {self.days} {self.start_time}"

    def is_full(self):
        return self.enrolled >= self.capacity

    def has_time_conflict(self, other_course):
        if self.days != other_course.days:
            return False
        return (self.start_time < other_course.end_time and 
                self.end_time > other_course.start_time)


class Students(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    gender=models.CharField(max_length=255)
    rollnumber=models.CharField(max_length=255)
    address=models.TextField()
    registered_courses = models.ManyToManyField(Course, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class LeaveReportStudent(models.Model):
    LEAVE_CHOICES= [
    ('Leave', 'Leave'),
    ('Emergency Leave', 'Emergency Leave'),
    ('OD', 'OD'),
    ('Study Leave', 'Study Leave'),
    ]
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_types=models.CharField(choices=LEAVE_CHOICES, default='Leave',max_length=100)
    from_leave_date = models.CharField(max_length=255)
    to_leave_date = models.CharField(max_length=255)   
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
            return f"{self.student.username} - {self.leave_types} ({self.leave_status})"



@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Students.objects.create(admin=instance,address="",gender="")

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.students.save()
