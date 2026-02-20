from django.views.generic import TemplateView, DetailView
from apps.portal.selectors.portal_selectors import get_site_identity, get_active_banners, get_latest_posts
from apps.portal.models import Post

class LandingPageView(TemplateView):
    template_name = "portal/public/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Sekolah ku"
        context["banners"] = get_active_banners() 
        context["latest_posts"] = get_latest_posts(3)
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = "portal/public/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Update jumlah view setiap kali berita dibuka
        self.object.views += 1
        self.object.save()
        return context
