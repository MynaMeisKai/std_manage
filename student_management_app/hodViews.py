from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import AddStudentForm, EditStudentForm
from student_management_app.models import *
from django.contrib.auth.decorators import login_required



@login_required(login_url='/login_requireds/') 
def admin_home(request):

    all_student_count = Students.objects.all().count()
    # all_student_leaves=LeaveReportStudent.objects.all().count()
    context={
        "all_student_count": all_student_count,  
        # "all_student_leaves" : all_student_leaves
    }
    return render(request,"hod_template/home_content.html",context)


@login_required(login_url='/login_requireds/') 
def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")

@login_required(login_url='/login_requireds/') 
def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,
                                                last_name=last_name,first_name=first_name,user_type=2)
            user.staffs.address=address
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))


@login_required(login_url='/login_requireds/') 
def add_student(request):
    form=AddStudentForm()
    return render(request,"hod_template/add_student_template.html",{"form":form})

@login_required(login_url='/login_requireds/') 
def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddStudentForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            gender = form.cleaned_data['gender']
            rollno=form.cleaned_data['rollnumber']
            address=form.cleaned_data["address"]
            print(form.is_valid())
            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                      first_name=first_name,last_name=last_name, user_type=2)
                print('---------------',gender,rollno,address)
                user.students.gender = gender
                user.students.rollnumber = rollno
                user.students.address = address
                    
                user.save()
                messages.success(request,"Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request,"Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form=AddStudentForm(request.POST)
            return render(request, "hod_template/add_student_template.html", {"form": form})

@login_required(login_url='/login_requireds/') 
def managestudent(request):
    students = Students.objects.all()
    context = {
        "students": students
    }
    return render(request, 'hod_template/manage_student_template.html', context)

@login_required(login_url='/login_requireds/') 
def edit_student(request,student_id):
    request.session['student_id']=student_id
    student=Students.objects.get(admin=student_id)
    form=EditStudentForm()
    form.fields['email'].initial=student.admin.email
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    form.fields['address'].initial=student.address
    form.fields['rollnumber'].initial=student.rollnumber
    form.fields['gender'].initial=student.gender
    return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,
                                                                    "username":student.admin.username})

@login_required(login_url='/login_requireds/') 
def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.session.get("student_id")
        if student_id==None:
            return HttpResponseRedirect(reverse("manage_student"))

        form=EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            gender = form.cleaned_data["gender"]

            try:
                user=CustomUser.objects.get(id=student_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                student=Students.objects.get(admin=student_id)
                student.address=address
                student.gender=gender
                student.save()
                del request.session['student_id']
                messages.success(request,"Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
            except:
                messages.error(request,"Failed to Edit Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
        else:
            form=EditStudentForm(request.POST)
            student=Students.objects.get(admin=student_id)
            return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,
                                                                            "username":student.admin.username})


@login_required(login_url='/login_requireds/') 
def studentleaveview(request):
    leaves = LeaveReportStudent.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/student_leave_view.html', context)

@login_required(login_url='/login_requireds/') 
def studentleaveapprove(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('student_leave_view')


@login_required(login_url='/login_requireds/') 
def studentleavereject(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('student_leave_view')