from django.core.management.base import BaseCommand
from apps.core.services.rbac_service import RBACService


class Command(BaseCommand):
    help = "Seed RBAC roles and permissions"

    def handle(self, *args, **kwargs):
        RBACService.seed_roles()
        self.stdout.write(self.style.SUCCESS("RBAC seeded successfully"))

