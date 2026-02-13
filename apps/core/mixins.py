from django.contrib.auth.mixins import PermissionRequiredMixin


class BasePermissionMixin(PermissionRequiredMixin):
    raise_exception = True
