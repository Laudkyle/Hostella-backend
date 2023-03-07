from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.core.mail import send_mail
import random
from .emails import *
from rest_framework.decorators import api_view
import jwt

class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            mail(serializer.data['email'])
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):

    queryset = NewUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

#verification view
class VerifiyOTP(APIView):
    def post(self,request):
        try:
            data =request.data
            serializer =VerifyAccountSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user =NewUser.objects.filter(email=email)
                if not user.exists():
                    return Response({
                        'status': 400,
                        'message': "Something went wrong!!!",
                        'data': "Invalid Email, Please enter a valid mail"
                    })
                if user[0].otp != otp:
                    return Response({
                        'status': 400,
                        'message': "Something went wrong!!!",
                        'data': "Wrong OTP"
                    })
                user = user.first()
                user.is_verified = True
                user.save()
                return Response({
                    'status':200,
                    'message': "Account successfully verfied !!!",
                    'data':{}
                })
            return Response({
                'status': 400,
                'message': "Something went wrong!!!",
                'data': serializer.errors
            })

        except Exception as e:
            print(e)

# User profile view
@api_view(['GET','PUT'])
def userProfle(request,document_id,format=None):
    try:
        auth = get_authorization_header(request).split()
        token=auth[1]
        print(token)
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        if document_id==payload['user_id']:
            user= UserProfile.objects.get(documentId=document_id)
        else:
            return Response('Validation failed', status=status.HTTP_403_FORBIDDEN)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method =='GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

