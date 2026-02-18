from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from apps.portal.models import SiteIdentity
from apps.portal.services.portal_services import PortalService
from apps.portal.selectors.portal_selectors import get_site_identity
from apps.core.mixins import BasePermissionMixin

class PortalSettingUpdateView(BasePermissionMixin, UpdateView):
    model = SiteIdentity
    template_name = "portal/settings.html"
    fields = '__all__' # Atau list field spesifik
    success_url = reverse_lazy('portal:settings')
    permission_required = 'portal.change_siteidentity'

    def get_object(self, queryset=None):
        return get_site_identity()

    def form_valid(self, form):
        PortalService.update_identity(
            instance=self.get_object(),
            data=form.cleaned_data,
            actor=self.request.user
        )
        messages.success(self.request, "Konfigurasi portal berhasil diperbarui!")
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Portal"
        return context
