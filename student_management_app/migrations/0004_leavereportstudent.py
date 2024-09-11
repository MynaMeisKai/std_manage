# Generated by Django 5.0.7 on 2024-07-31 13:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0003_remove_students_profile_pic_students_rollnumber'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveReportStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('leave_types', models.CharField(choices=[('Leave', 'Leave'), ('Emergency Leave', 'Emergency Leave'), ('OD', 'OD'), ('Study Leave', 'Study Leave')], default='Leave', max_length=100)),
                ('from_leave_date', models.CharField(max_length=255)),
                ('to_leave_date', models.CharField(max_length=255)),
                ('leave_message', models.TextField()),
                ('leave_status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students')),
            ],
        ),
    ]