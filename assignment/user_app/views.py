from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import requests
import jwt
import datetime
import ssl
from .serializers import UserCreateSerializer, UserSerializer
from .password_validcheck import password_validcheck
from .models import User

JWT_SECRET_KEY = getattr(settings, 'SIMPLE_JWT', None)['SIGNING_KEY']

@api_view(['POST'])
@permission_classes([AllowAny])
def createUser(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        if password_validcheck(serializer.validated_data['password']) == False:
            return Response({"message": "check your password valid"}, status=status.HTTP_409_CONFLICT)
        if User.objects.filter(email=serializer.validated_data['email']).first() is None:
            serializer.save()
            return Response({"message": "Good email for use"}, status=status.HTTP_201_CREATED)
        return Response({"message": "duplicate email"}, status=status.HTTP_409_CONFLICT)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        search_email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=search_email).first()

        if user is None:
            raise AuthenticationFailed('User not found!') 
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!') 
        
        data = {'email': search_email, 'password': password}
        response_token = requests.post("http://127.0.0.1:8000/users/api-jwt-auth/", data=data)
        response_token = response_token.json()
        # payload= {
        #     'email' : user.email,
        #     'exp' : datetime.datetime.now() + datetime.timedelta(minutes=60), # 유효 시간
        #     'iat' : datetime.datetime.now() # 발급 시각
        # }
        # token = jwt.encode(payload, JWT_SECRET_KEY, algorithm = 'HS256').decode('utf-8')

        response = JsonResponse({
            'message' : 'ok',
            'jwt':response_token["access"]
        })

        response.set_cookie(key ='jwt', value= response_token, httponly=True) 

        return response

@csrf_exempt
def logout(request) :
    if request.method == 'POST' :
        response = JsonResponse({
            "message" : "success"
        })
        response.delete_cookie('jwt')
        return response

@csrf_exempt
def userValid(request):
    token = request.COOKIES.get('jwt')

    if not token :
        return HttpResponse("User doesn't have token", status=status.HTTP_200_OK)

    try :
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])

    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('UnAuthenticated!')

    try:
        user = User.objects.filter(email=payload['email']).first()
    except:
        return HttpResponse("User not Found", status=status.HTTP_200_OK)
    return HttpResponse("User still valid", status=status.HTTP_404_NOT_FOUND)