from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid
from django.contrib.auth import get_user_model

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name,last_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name,last_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, last_name,password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name,last_name =last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified=models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    last_name = models.CharField(max_length=200,null=True)
    password = models.CharField(max_length=200,null=True)
    registrationDate = models.DateField(auto_now_add=True,null=True)
    documentId = models.UUIDField(default=uuid.uuid4(), editable=False, unique=True,null=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name','first_name','last_name']

    def __str__(self):
        return self.user_name
    
#Creating the use profile
User = get_user_model()
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=200,null=True)
    gender = models.CharField(max_length=200,null=True)
    photo = models.ImageField(upload_to="images/", blank=True, null=True)
    phoneNumber = models.CharField(max_length=200,null=True)
    level =models.CharField(max_length=10,null=True)


    
    def __str__(self):
        return f"{self.user.user_name}'s Profile"