from django.contrib.auth import login
from django.db import transaction
from knox.views import LoginView as KnoxLoginView, LogoutView as KnoxLogoutView, LogoutAllView as KnoxLogoutAllView
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response

from apps.users.serializers import AuthTokenSerializer, ChangePasswordSerializer, UserSerializer, UpdateUserSerializer


class RegisterView(GenericAPIView, CreateModelMixin):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        serialized_new_user = self.get_serializer(user)
        return Response(serialized_new_user.data, status=status.HTTP_201_CREATED)


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        print(request.data)
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class LogoutView(KnoxLogoutView):
    permission_classes = (permissions.IsAuthenticated,)


class LogoutAllView(KnoxLogoutAllView):
    permission_classes = (permissions.IsAuthenticated,)


class RetrieveUserView(GenericAPIView, RetrieveModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UpdateUserInfosView(GenericAPIView, UpdateModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdateUserSerializer

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ChangePasswordView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')
        if not user.check_password(old_password):
            raise PermissionDenied("INCORRECT_CURRENT_PASSWORD_NOT")
        user.set_password(new_password)
        user.save()
        return Response({'message': "Votre mot de passe à été changé avec succès."}, status=status.HTTP_200_OK)
