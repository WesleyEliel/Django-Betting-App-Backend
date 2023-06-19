from django.contrib.auth import login
from django.db import transaction
from knox.views import LoginView as KnoxLoginView, LogoutView as KnoxLogoutView, LogoutAllView as KnoxLogoutAllView
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError, APIException
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response

from apps.users.serializers import AuthTokenSerializer, ChangePasswordSerializer, UserSerializer, UpdateUserSerializer, \
    TransactionSerializer, InheritanceTransactionSerializer, WithdrawTransactionSerializer, DepositTransactionSerializer
from apps.users.models import Transaction, DepositTransaction, WithdrawTransaction
from commons.mixings import BaseModelMixin
from commons.views import BaseGenericViewSet


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


class TransactionViewSet(CreateModelMixin, BaseModelMixin, BaseGenericViewSet):
    pk = 'uuid'
    object_class = Transaction
    serializer_default_class = TransactionSerializer

    permission_classes_by_action = {
        'create': [permissions.IsAuthenticated],
        'list_by_user': [permissions.IsAuthenticated]
    }

    serializer_classes_by_action = {
        'create': TransactionSerializer,
        'list_by_user': InheritanceTransactionSerializer,
    }

    def get_queryset(self):
        return self.object_class.objects.all()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer_class = None
        transaction_type = None
        try:
            transaction_type = str.upper(request.data.pop('type'))
        except Exception as exc:
            raise ValidationError(
                {'message': "Veuillez renseigner le type de la transaction."})
        data = request.data | {
            'user': request.user.pk, 'type': transaction_type}
        if transaction_type == Transaction.WITHDRAW:
            serializer_class = WithdrawTransactionSerializer
        elif transaction_type == Transaction.DEPOSIT:
            serializer_class = DepositTransactionSerializer
        else:
            raise ValidationError({'message': "Type de transaction invalide."})
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        _transaction = serializer.save()
        try:
            process_response = _transaction.process()
        except Exception as exc:
            print(exc.__str__())
            raise APIException()

        if not process_response.get('success', True):
            raise APIException(
                {'message': 'Erreur du processus'})
        else:
            try:
                serialized_created_object = serializer_class(_transaction)
                headers = self.get_success_headers(
                    serialized_created_object.data)
                return Response(serialized_created_object.data, status=status.HTTP_201_CREATED, headers=headers)
            except Exception as exc:
                print(exc.__str__())
                raise APIException()

    @action(methods=["GET"], detail=False, url_path='by-me')
    def list_by_user(self, request, *args, **kwargs):
        user = request.user
        queryset = self.filter_queryset(self.get_queryset().filter(user=user))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
