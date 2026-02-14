from django.contrib.auth import get_user_model
from apps.core.services.base_service import AuditService, BaseService
from django.contrib.auth.models import Permission
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
            target=target_user,
            action="TOGGLE",
            description=f"Toggled user {target_user.email}"
        )

        return status



    @staticmethod
    def update_user(form, actor=None):
        instance = form.save()

        AuditService.log(
            actor=actor,
            target=instance,
            action="UPDATE",
            description=f"Updated user {instance.email}"
        )

        return instance
