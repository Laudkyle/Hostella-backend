from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('verify/', VerifiyOTP.as_view()),
    path('changepassword/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(), name='blacklist'),
    path('profile/<str:document_id>/', userProfle),
]