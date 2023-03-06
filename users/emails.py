from django.core.mail import send_mail
import random
from django.conf import settings
from .models import NewUser

def mail(email):
    otp = random.randint(100000,999999)
    send_mail("Tester",
              f"Here is verificaion code : {otp}",
              "kyleaby1@gmail.com",
              [email],
              fail_silently=False)
    user_obj = NewUser.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()
