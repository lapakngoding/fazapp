from apps.core.models import AuditLog
from django.contrib.auth.models import Group, Permission
from django.apps import apps
from core.rbac import SYSTEM_ROLES

class AuditService:

    @staticmethod
    def log(actor, action, target=None, description=""):

        target_model = None
        target_id = None

        if target:
            target_model = target.__class__.__name__
            target_id = target.pk

        AuditLog.objects.create(
            actor=actor,
            target_model=target_model,
            target_id=target_id,
            action=action,
            description=description,
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

