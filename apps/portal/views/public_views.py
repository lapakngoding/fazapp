from django.views.generic import TemplateView
from apps.portal.selectors.portal_selectors import get_site_identity, get_active_banners

class LandingPageView(TemplateView):
    template_name = "portal/public/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Data portal sudah ada dari Context Processor, 
        # tapi kita bisa tambah data spesifik di sini
        context["page_title"] = "Sekolah ku"
        context["banners"] = get_active_banners() 
        return context
