from django.db import models
from uuid import uuid4

from .managers import DeletedManager, SoftDeleteManager, DefaultManager

# Create your models here.


class AbstractCommonBaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(
        verbose_name="Date d'ajout", auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(
        verbose_name='Date de modification', auto_now_add=False, auto_now=True)
    deleted_at = models.DateTimeField(
        verbose_name='Date de suppression', blank=True, null=True)
    active = models.BooleanField(
        verbose_name="Désigne si l'instance est active", default=True)
    is_deleted = models.BooleanField(
        verbose_name="Désigne si l'instance est supprimée", default=False)
    objects = SoftDeleteManager()
    default_objects = DefaultManager()
    deleted_objects = DeletedManager()

    class Meta:
        abstract = True
