from apps.core.models import AuditLog


class AuditService:

    @staticmethod
    def log(actor, target, action, description=""):
        AuditLog.objects.create(
            actor=actor,
            target_model=target.__class__.__name__,
            target_id=target.pk,
            action=action,
            description=description
        )

