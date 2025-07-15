from django.urls import path
from student_management_app import hodViews, studentViews
from student_management_app.loginRequired import login_requireds
from student_management_app.views import *

urlpatterns = [
    path('login_requireds/',login_requireds,name='login_requireds'),
    path('',ShowLoginPage,name="show_login"),
    path('doLogin',doLogin,name="doLogin"),
    path('logout_user', logout_user,name="logout_user"),

    path('admin_home',hodViews.admin_home,name="admin_home"),

    path('add_student', hodViews.add_student,name="add_student"),
    path('add_student_save', hodViews.add_student_save,name="add_student_save"),
    path('manage_student', hodViews.managestudent,name="manage_student"),

    path('edit_student/<str:student_id>', hodViews.edit_student,name="edit_student"),
    path('edit_student_save', hodViews.edit_student_save,name="edit_student_save"),

     path('student_leave_view/', hodViews.studentleaveview, name="student_leave_view"),
    path('student_leave_approve/<leave_id>/', hodViews.studentleaveapprove, name="student_leave_approve"),
    path('student_leave_reject/<leave_id>/', hodViews.studentleavereject, name="student_leave_reject"),
    

    path('student_home', studentViews.student_home, name="student_home"),
    path('student_apply_leave/', studentViews.studentapplyleave, name="student_apply_leave"),
    path('student_apply_leave_save/', studentViews.studentapplyleavesave, name="student_apply_leave_save"),
    path('cancel_leave',studentViews.cancelleave,name="cancel_leave"),

    path('std_course_page/', studentViews.std_course_page, name='std_course_page'),
    path('std_course_register/', studentViews.std_course_register, name='std_course_register'),
    path('view_table_time/', studentViews.view_table_time, name='view_table_time'),
    
    ]