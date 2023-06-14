from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet
from knox.auth import TokenAuthentication

from commons.mixings import BaseModelMixin

class BaseModelsViewSet(BaseModelMixin, viewsets.ModelViewSet):
    object_class = None
    serializer_default_class = None
    authentication_classes = [TokenAuthentication]

    serializer_classes_by_action = {}

    permission_classes_by_action = {}


class BaseGenericViewSet(GenericViewSet):
    object_class = None
    serializer_default_class = None
    authentication_classes = [TokenAuthentication]

    serializer_classes_by_action = {}

    permission_classes_by_action = {}

    def get_queryset(self):
        if not self.object_class:
            raise NotImplementedError
        return self.object_class.objects.all()

    def get_permissions(self):
        def get_permission_function(instance):
            try:
                return instance()
            except TypeError:
                return instance

        try:
            # return permission_classes depending on `action`
            return [get_permission_function(permission) for permission in
                    self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [get_permission_function(permission) for permission in self.permission_classes]

    def get_serializer_class(self):
        if not hasattr(self, 'serializer_classes_by_action'):
            return self.serializer_default_class
        try:
            # return serializer_class depending on `action`
            return self.serializer_classes_by_action[self.action]
        except KeyError:
            # action is not set return default serializer_class
            return self.serializer_default_class