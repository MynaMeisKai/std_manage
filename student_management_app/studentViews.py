from datetime import time
from django.shortcuts import redirect, render
from django.contrib import messages
from student_management_app.forms import RegistrationForm
from student_management_app.models import *
from django.contrib.auth.decorators import login_required



@login_required(login_url='/student_management_app/login_requireds/')
def student_home(request):
    student_obj = Students.objects.get(admin=request.user.id)
    return render(request, "student_template/student_home_template.html",{"student":student_obj})



@login_required(login_url='/student_management_app/login_requireds/')
def studentapplyleave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    context = {
        "leave_data": leave_data,
        'student' :student_obj
    }
    return render(request, 'student_template/student_apply_leave.html', context)


@login_required(login_url='/student_management_app/login_requireds/')
def studentapplyleavesave(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_apply_leave')
    else:
        leavetype= request.POST['leave_type']
        fromleave_date = request.POST['fromleave_date']
        toleave_date = request.POST['toleave_date']
        leave_message = request.POST['leave_message']

        student_obj = Students.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(student_id=student_obj, leave_types=leavetype, from_leave_date=fromleave_date,to_leave_date=toleave_date,leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('student_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('student_apply_leave')

@login_required(login_url='/student_management_app/login_requireds/')        
def cancelleave(request): 
    student_obj = Students.objects.get(admin=request.user.id)
    leave_deletes=LeaveReportStudent.objects.filter(student_id=student_obj)
    leave_deletes.delete()
    return redirect('student_apply_leave')



def std_course_page(request):
    courses = Course.objects.all()
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    # form = RegistrationForm()
    student_obj = Students.objects.get(admin=request.user.id)
  
    db_days = Course.objects.values_list('days', flat=True).distinct()
    ordered_days = [day for day in days_of_week if day in db_days]
    print(ordered_days)
    time_slots = [
        {'start': time(9, 0), 'end': time(9, 45)},  # 09:00 - 09:45
        {'start': time(9, 45), 'end': time(10, 30)}, 
        {'start': time(10, 30), 'end': time(11, 15)}, 
        {'start': time(11, 45), 'end': time(12, 30)},
        {'start': time(1, 30), 'end': time(2,15)},
        {'start': time(2, 15), 'end': time(3, 0)},
    ]
 
    days_of_week = Course.objects.values_list('days', flat=True).distinct()
    
    context = {
        'days_of_week': ordered_days,
        'time_slots': time_slots,
        'student': student_obj,
        'form': RegistrationForm(),
        'courses': courses,
    }
    

    return render(request, 'student_template/course_field.html', context)


def std_course_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            courses = form.cleaned_data['courses']
            
            # Create or update student
            student, created = Students.objects.get_or_create(
                student_id=student_id,
                defaults={'name': name, 'email': email}
            )
            if not created:
                student.name = name
                student.email = email
                student.save()
            
            # Register for courses
            for course in courses:
                student.registered_courses.add(course)
                course.enrolled += 1
                course.save()
            
            return render(request, 'student_template/register_success.html', {
                'student': student,
                'courses': courses
            })
    else:
        form = RegistrationForm()
    
    return render(request, 'student_template/course_filed.html', {
        'form': form,
        'courses': Course.objects.all()
    })