from django.shortcuts import redirect, render
from django.contrib import messages
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

