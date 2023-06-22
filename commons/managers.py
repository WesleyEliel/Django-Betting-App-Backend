from django.conf import settings
from django.db import models
from django.utils import timezone


def get_settings():
    default_settings = dict(
        cascade=True,
    )
    return getattr(settings, 'SOFT_DELETE_SETTINGS', default_settings)


class SoftDeleteQuerySet(models.query.QuerySet):

    def delete(self, *args, **kwargs):
        cascade = get_settings()['cascade']
        if cascade:  # delete one by one if cascade
            for obj in self.all():
                obj.delete(cascade=cascade)
        return self.update(is_deleted=True, deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)


class DeletedQuerySet(models.query.QuerySet):
    def restore(self, *args, **kwargs):
        qs = self.filter(*args, **kwargs)
        qs.update(is_deleted=False, deleted_at=None)


class DeletedManager(models.Manager):
    def get_queryset(self):
        return DeletedQuerySet(self.model, using=self._db).filter(is_deleted=True)


class DefaultManager(models.Manager):
    pass
