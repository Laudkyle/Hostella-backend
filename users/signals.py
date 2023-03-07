from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import *

user= get_user_model()
@receiver(post_save,sender=user)
def createUserProfile(sender, instance, created, **kwargs):
    if created:
        userInfo= NewUser.objects.filter(user_name=instance)
        userInfo= userInfo.first()
        UserProfile.objects.create(user=instance, user_name= userInfo.user_name, first_name=userInfo.first_name, last_name=userInfo.last_name, documentId=userInfo.documentId)
        
