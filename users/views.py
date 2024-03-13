from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


from .models import User
from .serializers import UserListSerializer, UserDetailSerializer, UserCreateSerializer
from api.mixins import UserPermissionMixin, AdminPermissionMixin


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data.get('access')
        refresh_token = response.data.get('refresh')
        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,
        })
        

# Login
class Login(CustomTokenObtainPairView):
    permission_classes = [permissions.AllowAny]


# Register
class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'response': 'User created successfully',
            'username': user.username,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


# Logout
class Logout(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
    

# Users
class UserList(AdminPermissionMixin, generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    

class UserDetail(UserPermissionMixin, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer