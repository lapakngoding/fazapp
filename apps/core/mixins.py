from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect

class BasePermissionMixin(PermissionRequiredMixin):
    """
    Mixin kustom untuk menghandle permission dengan feedback pesan.
    """
    raise_exception = False  # Set False agar bisa diredirect
    
    def handle_no_permission(self):
        messages.error(self.request, "Anda tidak memiliki akses untuk melakukan aksi tersebut.")
        if self.request.user.is_authenticated:
            return redirect('core:dashboard')
        return redirect('users:login')
