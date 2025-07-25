# serializers.py
from rest_framework import serializers
from student_management_app.models import CustomUser, AdminHOD, Students, LeaveReportStudent
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken




class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'


def update_student_profile(user, roll_number, gender, address):
    try:
        student = Students.objects.get(admin=user)
        
        student.rollnumber = roll_number
        student.gender = gender
        student.address = address
        
        student.save()
        
    except ObjectDoesNotExist:
        pass

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'user_type']


class RegisterSerializer(serializers.ModelSerializer):
    GENDER = [
        ('Male', 'MALE'),
        ('Female', 'FEMALE')
    ]

    roll_number = serializers.CharField(max_length=20, write_only=True)
    gender = serializers.ChoiceField(choices=GENDER, write_only=True)
    address = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'username', 'password', 'roll_number', 'gender', 'address']
        extra_kwargs = {'password': {'write_only': True}}



    def create(self, validated_data):
        roll_number = validated_data.pop('roll_number')
        gender = validated_data.pop('gender')
        address = validated_data.pop('address')

       
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=make_password(validated_data['password']),
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user_type=2  # Assuming 2 represents a student
        )
    
        update_student_profile(user, roll_number, gender, address) # type: ignore
        context = {"message": "Registered Successfully !!"}
        
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        aser = get_user_model()
        username = data.get('username')
        password = data.get('password')
        if username and password:
            # user = authenticate(username=username, password=password)
            user = aser.objects.get(username=username)
            if user and user.is_active:
                data['user'] = user
                return data
            else:
                raise serializers.ValidationError("Invalid credentials or User is not active.")
        else:
            raise serializers.ValidationError("Must provide username and password.")

    def create(self, validated_data):
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)
        st=user.students
        return {
            'username': user.username,
            'token': str(refresh.access_token),
            # 'user_type': user.get_user_type_display(),
            'user':StudentsSerializer(st).data
        }

class LeaveReportStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveReportStudent
        fields = ['leave_types', 'from_leave_date', 'to_leave_date', 'leave_message', 'leave_status']
        extra_kwargs = {
            'student': {'read_only': True},  # student will be set in the view, not provided by the user
            'leave_status': {'read_only': True},  # leave_status will be managed by the system
        }