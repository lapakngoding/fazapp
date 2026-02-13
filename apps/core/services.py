from apps.core.models import AuditLog
from django.contrib.auth.models import Group, Permission
from django.apps import apps
from .rbac import SYSTEM_ROLES

class AuditService:

    @staticmethod
    def log(user, action, object_repr=""):
        AuditLog.objects.create(
            user=user,
            action=action,
            object_repr=object_repr,
        )

class BaseService:

    @staticmethod
    def log_action(actor, action, instance, description=""):
        """
        Log activity ke AuditLog.
        actor      : user yang melakukan aksi
        action     : string, misal 'CREATE', 'UPDATE', 'DELETE'
        instance   : object model yang diubah/dihapus
        description: optional text
        changes    : optional dict
        """

        if not actor or not instance:
            return

        AuditLog.objects.create(
            actor=actor,
            action=action,
            target_model=instance._meta.model_name,
            target_id=instance.pk,
            description=description,
        )

