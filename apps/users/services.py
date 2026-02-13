from django.contrib.auth import get_user_model
from apps.core.core_services import AuditService, BaseService
from django.contrib.auth.models import Group, Permission
from apps.core.services.audit_service import AuditService


User = get_user_model()


class UserService:

    @staticmethod
    def create_user(form, actor=None):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password1"])
        user.save()

        AuditService.log(
            actor=actor,
            target=user,
            action="CREATE",
            description=f"Created user {user.email}"
        )

        return user

    @staticmethod
    def toggle_active(target_user, actor=None):
        target_user.is_active = not target_user.is_active
        target_user.save()

        status = "activated" if target_user.is_active else "disabled"

        AuditService.log(
            actor=actor,
            target=user,
            action="TOGGLE",
            description=f"Toggle user {user.email}"
        )

        return status


    @staticmethod
    def update_user(form, actor=None):
        user = form.save()

        AuditService.log(
            actor=actor,
            target=user,
            action="UPDATE",
            description=f"Update user {user.email}"
        )

        return user

class GroupService:

    @staticmethod
    def create_group(cleaned_data, actor=None):
        group = Group.objects.create(
            name=cleaned_data["name"]
        )

        permissions = cleaned_data.get("permissions")
        if permissions:
            group.permissions.set(permissions)

        return group


    @staticmethod
    def update_group(instance, cleaned_data, actor=None):
        instance.name = cleaned_data["name"]
        instance.save()

        permissions = cleaned_data.get("permissions")
        if permissions is not None:
            instance.permissions.set(permissions)

        return instance


    @staticmethod
    def delete_group(group, actor=None):
        # simpan dulu nama untuk log
        group_name = group.name

        # log dulu sebelum dihapus
        BaseService.log_action(
            actor=actor,
            action="DELETE",
            instance=group,
            description=f"Deleted group {group_name}"
        )

        # baru hapus
        group.delete()

        return group_name

