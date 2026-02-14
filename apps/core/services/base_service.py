from apps.core.models import AuditLog
from django.contrib.auth.models import Group, Permission
from django.apps import apps
from core.rbac import SYSTEM_ROLES

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

        if not actor:
            return

        AuditLog.objects.create(
            actor=actor,
            action=action,
            target_model=instance._meta.model_name,
            target_id=instance.pk,
            description=description,
            
        )


class RBACService:

    @staticmethod
    def seed_roles():
        for role_name, config in SYSTEM_ROLES.items():
            group, created = Group.objects.get_or_create(name=role_name)

            if config["permissions"] == "__all__":
                permissions = Permission.objects.all()
            else:
                permissions = []
                for perm_code in config["permissions"]:
                    app_label, codename = perm_code.split(".")
                    permissions.append(
                        Permission.objects.get(
                            content_type__app_label=app_label,
                            codename=codename
                        )
                    )

            group.permissions.set(permissions)

