from django.contrib.auth.models import Group, Permission
from apps.core.rbac import SYSTEM_ROLES

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

