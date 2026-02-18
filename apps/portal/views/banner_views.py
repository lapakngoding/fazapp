from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from apps.core.mixins import BasePermissionMixin
from apps.portal.models import Banner
from apps.portal.forms import BannerForm

class BannerListView(BasePermissionMixin, ListView):
    model = Banner
    template_name = "portal/banners/list.html"
    context_object_name = "banners"
    permission_required = "portal.view_banner"

class BannerCreateView(BasePermissionMixin, CreateView):
    model = Banner
    form_class = BannerForm
    template_name = "portal/banners/form.html"
    success_url = reverse_lazy('portal:banner_list')
    permission_required = "portal.add_banner"

    def form_valid(self, form):
        messages.success(self.request, "Banner berhasil ditambahkan!")
        return super().form_valid(form)

class BannerUpdateView(BasePermissionMixin, UpdateView):
    model = Banner
    form_class = BannerForm
    template_name = "portal/banners/form.html"
    success_url = reverse_lazy('portal:banner_list')
    permission_required = "portal.change_banner"

    def form_valid(self, form):
        messages.success(self.request, "Banner berhasil diperbarui!")
        return super().form_valid(form)
