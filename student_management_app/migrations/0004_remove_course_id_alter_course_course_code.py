# Generated by Django 5.2.4 on 2025-07-16 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0003_course_days'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='id',
        ),
        migrations.AlterField(
            model_name='course',
            name='course_code',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, unique=True),
        ),
    ]
