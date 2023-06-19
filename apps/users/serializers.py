# -*- coding: utf-8 -*-
"""
Created on June 6, 2023

@author:
    Wesley Eliel MONTCHO, alias DevBackend7
"""

import logging

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from commons.messages import Messages
from apps.users.models import User, Transaction, DepositTransaction, WithdrawTransaction
from apps.utils.models import Country

logger = logging.getLogger(__name__)
logger.setLevel('INFO')


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label="Email",
        write_only=True
    )
    password = serializers.CharField(
        label="Mot de passe",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label="Token",
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = "Impossible de se connecter avec les identifiants renseignés"
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Vous devez inclure "email" et "password.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'conf_num', 'email', 'birthday', 'country',
                  'sex', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'read_only': True},
            'last_name': {'read_only': True},
            'conf_num': {'read_only': True},
            'profile_image': {'read_only': True},
        }

    def validate(self, data):
        password = data.get('password', '')
        email = data.get('email', None)

        if password == "":
            raise ValidationError({"password": 'PASSWORD_NEEDED'})

        if email is not None:
            if User.objects.filter(email=email).exists():
                raise ValidationError(
                    {'email': 'EMAIL_ALREADY_USED'})

        return super().validate(attrs=data)

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.ask_verification()
        instance.save()
        financial_account = instance.related_financial_account
        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'sex', 'birthday',
                  )


class UserSerializerLight(serializers.ModelSerializer):
    class Meta:
        ref_name = "UserSerializerLightForUserModule"
        model = User
        fields = ('pk', 'first_name', 'last_name', 'email', 'sex')


class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Transaction
        fields = (
            'pk', 'type', 'user', 'local_id', 'amount',
        )

        read_only_fiels = ('local_id', 'type')


class DepositTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositTransaction
        fields = TransactionSerializer.Meta.fields + ('url', 'status')


class WithdrawTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawTransaction
        fields = TransactionSerializer.Meta.fields + ('way', 'status')
        read_only_fiels = ('local_id', 'type')

        extra_kwargs = {
            'amount': {'required': True},
        }


class InheritanceTransactionSerializer(serializers.ModelSerializer):
    def to_representation(self, instance, *args, **kwargs):
        if instance is not None:
            child = Transaction.objects.get_subclass(id=instance.id)

            if isinstance(child, DepositTransaction):
                serializer = DepositTransactionSerializer(
                    instance=child, context=self.context)

            elif isinstance(child, WithdrawTransaction):
                serializer = WithdrawTransactionSerializer(
                    instance=child, context=self.context)

            else:
                print(type(child))
                raise Exception('Unexpected type of tagged object')

            return serializer.data

        return None

    class Meta:
        model = Transaction
        fields = (
            'pk', 'description', 'type', 'local_id', 'user', 'amount'
        )

        read_only_fiels = ('local_id',)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, required=True)
    new_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, required=True)

    def validate(self, attrs):
        old_password = attrs.get('old_password', '')
        new_password = attrs.get('new_password', '')
        if old_password == '':
            raise ValidationError(
                {'old_password': Messages.THIS_FIELD_MUST_NOT_BE_EMPTY})
        if new_password == '':
            raise ValidationError(
                {'new_password': Messages.THIS_FIELD_MUST_NOT_BE_EMPTY})

        return super().validate(attrs)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
