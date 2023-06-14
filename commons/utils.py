import os
import time

from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import NotFound


def custom_get_object_or_404(klass, *args, **kwargs):
    try:
        return get_object_or_404(klass, *args, **kwargs)
    except Http404:
        queryset = klass._default_manager.all() if hasattr(
            klass, '_default_manager') else klass
        raise NotFound(
            f'INSTANCE_{queryset.model._meta.object_name}_WITH_THIS_IDENTIFIERS_DOES_NOT_EXISTS'.upper())
    except Exception as exc:
        print(type(exc))
        raise exc


def model_instances_exist(model: models.Model):
    return len(model.objects.all()) != 0


def _upload_to(instance, filename):
    epoch_time = round(time.time())
    name, extension = os.path.splitext(filename)
    file = "{}_{}{}".format(name, epoch_time, extension)
    return "{}/{}".format(instance.__class__.__name__, file)
