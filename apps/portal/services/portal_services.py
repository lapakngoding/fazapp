from apps.portal.models import SiteIdentity
from apps.core.services.audit_service import AuditService

class PortalService:
    @staticmethod
    def update_identity(instance, data, actor=None):
        for attr, value in data.items():
            setattr(instance, attr, value)
        
        instance.full_clean()
        instance.save()

        AuditService.log(
            actor=actor,
            target=instance,
            action="UPDATE",
            description=f"Updated site identity: {instance.name}"
        )
        return instance
