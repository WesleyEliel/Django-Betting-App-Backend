from django.db import models
from uuid import uuid4

from django.utils import timezone

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

    def delete(self, *args, **kwargs):
        related_models_dataset = [
            (rel.on_delete == models.CASCADE, rel.get_accessor_name(), rel.related_model._meta.verbose_name)
            for rel in self._meta.related_objects
        ]
        # Propose to user to delete all linked objects by foreign key or many to many before trying to delete the
        # current objects

        for on_delete_is_cascade, accessor, verbose_name in related_models_dataset:
            if on_delete_is_cascade:
                objects = getattr(self, accessor).all()
                objects.update(is_deleted=True, deleted_at=timezone.now())
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
        return super(AbstractCommonBaseModel, self).delete()
