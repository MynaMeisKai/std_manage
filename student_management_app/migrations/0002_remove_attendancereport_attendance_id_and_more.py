# Generated by Django 5.0.7 on 2024-07-31 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendancereport',
            name='attendance_id',
        ),
        migrations.RemoveField(
            model_name='attendancereport',
            name='student_id',
        ),
        migrations.RemoveField(
            model_name='students',
            name='course_id',
        ),
        migrations.RemoveField(
            model_name='subjects',
            name='course_id',
        ),
        migrations.RemoveField(
            model_name='feedbackstaffs',
            name='staff_id',
        ),
        migrations.RemoveField(
            model_name='feedbackstudent',
            name='student_id',
        ),
        migrations.RemoveField(
            model_name='leavereportstaff',
            name='staff_id',
        ),
        migrations.RemoveField(
            model_name='leavereportstudent',
            name='student_id',
        ),
        migrations.RemoveField(
            model_name='notificationstaffs',
            name='staff_id',
        ),
        migrations.RemoveField(
            model_name='notificationstudent',
            name='student_id',
        ),
        migrations.RemoveField(
            model_name='staffs',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='subjects',
            name='staff_id',
        ),
        migrations.RemoveField(
            model_name='students',
            name='session_end_year',
        ),
        migrations.RemoveField(
            model_name='students',
            name='session_start_year',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[(1, 'HOD'), (2, 'Student')], default=1, max_length=10),
        ),
        migrations.DeleteModel(
            name='Attendance',
        ),
        migrations.DeleteModel(
            name='AttendanceReport',
        ),
        migrations.DeleteModel(
            name='Courses',
        ),
        migrations.DeleteModel(
            name='FeedBackStaffs',
        ),
        migrations.DeleteModel(
            name='FeedBackStudent',
        ),
        migrations.DeleteModel(
            name='LeaveReportStaff',
        ),
        migrations.DeleteModel(
            name='LeaveReportStudent',
        ),
        migrations.DeleteModel(
            name='NotificationStaffs',
        ),
        migrations.DeleteModel(
            name='NotificationStudent',
        ),
        migrations.DeleteModel(
            name='Staffs',
        ),
        migrations.DeleteModel(
            name='Subjects',
        ),
    ]