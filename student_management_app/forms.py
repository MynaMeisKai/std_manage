from django import forms
from student_management_app.models import Course

class DateInput(forms.DateInput):
    input_type = "date"

class AddStudentForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    rollnumber=forms.CharField(label="Roll No",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )
    gender=forms.ChoiceField(label="Gender",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))

class EditStudentForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    rollnumber=forms.CharField(label="Roll No",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))

    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    gender=forms.ChoiceField(label="Gender",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))


class RegistrationForm(forms.Form):
    student_id = forms.CharField(label='Student ID', max_length=20)
    name = forms.CharField(label='Full Name', max_length=100)
    email = forms.EmailField(label='Email')
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        courses = cleaned_data.get('courses', [])
        
        # Check for time conflicts
        course_list = list(courses)
        for i in range(len(course_list)):
            for j in range(i + 1, len(course_list)):
                if course_list[i].has_time_conflict(course_list[j]):
                    raise forms.ValidationError(
                        f"Time conflict between {course_list[i].course_code} and {course_list[j].course_code}"
                    )
        
        # Check for full courses
        for course in courses:
            if course.is_full():
                raise forms.ValidationError(
                    f"Course {course.course_code} is already full"
                )
        
        return cleaned_data