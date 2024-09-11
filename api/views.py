from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.serializers import *
from student_management_app.models import *

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.create(serializer.validated_data), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class ApplyLeaveView(generics.CreateAPIView):
    queryset = LeaveReportStudent.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = LeaveReportStudentSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == 2:
            return Response({"error": "Only students can apply for leave."}, status=status.HTTP_403_FORBIDDEN)
        return super().post(request, *args, **kwargs)
