from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    RefreshTokenSerializer,
    LogoutSerializer,
)

class RegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

class LoginAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            refresh_token = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh_token),
                "access": str(refresh_token.access_token)
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RefreshTokenSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]
        try:
            refresh_token = RefreshToken(token)
            return Response({
                "refresh": str(refresh_token),
                "access": str(refresh_token.access_token)
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({"detail": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]
        try:
            refresh_token = RefreshToken(token)
            refresh_token.blacklist()
            return Response({"detail": "User logged out!"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as err:
            return Response({"detail": str(err)}, status=status.HTTP_400_BAD_REQUEST)