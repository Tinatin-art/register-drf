from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.authtoken.models import Token
from .serializers import UserSerializer

User = get_user_model()

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = get_object_or_404(User, username=username)
    
    if not user.check_password(password):
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    
    return Response({"token": token.key, 'user': serializer.data})

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        password = request.data.get('password')
        user.set_password(password)
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("Passed for {}".format(request.user.email))












# from rest_framework.response import  Response
# from rest_framework.authtoken.models import Token
# from .serializers import *
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import authentication_classes, permission_classes
# from rest_framework.authentication import SessionAuthentication, TokenAuthentication
# from rest_framework.permissions import IsAuthenticated

# @api_view(['POST'])
# def login(request):
#     user = get_object_or_404(User, username=request.data['username'])
#     if not user.check_password(request.data['password']):
#         return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
#     token = Token.objects.get(user=user)
#     serializer = UserSerializer(instance=user)
#     return Response({"token": token.key, 'user': serializer.data})

# @api_view(['POST'])
# def signup(request):
#     serializer = UserSerializer(data=request.data)

#     if serializer.is_valid():
#         serializer.save()
#         user = User.objects.get(username=request.data['username'])
#         user.set_password(request.data['password'])
#         user.save()
#         token = Token.objects.create(user=user)
#         return Response({'token': token.key, 'user': serializer.data})
#     return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def test_token(request):
#     return Response("passed for {}".format(request.user.email))


