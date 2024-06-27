from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework import status
from api.auth.serializers import LoginSerializer, ReadUserSerializer, CreatUserSerializer
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def register_api_view(request):
    serializer = CreatUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token, created = Token.objects.get_or_create(user=user)
    read_serializer = ReadUserSerializer(user, context={'request': request})
    data = {**read_serializer.data, 'token': token.key}
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_api_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        token, created = Token.objects.get_or_create(user=user) # (token, False)
        read_serializer = ReadUserSerializer(user, context={'request': request})
        data = {**read_serializer.data, 'token': token.key}
        return Response(data)

    return Response(    
        {'detail': 'Не существует пользователя или неверный пароль.'}, status=status.HTTP_401_UNAUTHORIZED)