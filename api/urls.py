from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from api.views import *

urlpatterns = [
    path('logins/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('apply_leave/', ApplyLeaveView.as_view(), name='apply_leave'),
]















# from api.views import UserList,SnippetDetail

# urlpatterns = [
#     path('users/', UserList.as_view(), name='user-list'),
#     path('users/<int:pk>/', SnippetDetail.as_view())
# ]