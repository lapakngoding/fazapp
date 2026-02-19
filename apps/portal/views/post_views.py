from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from apps.core.mixins import BasePermissionMixin
from apps.portal.models import Post
from apps.portal.forms import PostForm

class PostListView(BasePermissionMixin, ListView):
    model = Post
    template_name = "portal/posts/list.html"
    context_object_name = "posts"
    permission_required = "portal.view_post"

class PostCreateView(BasePermissionMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "portal/posts/form.html"
    success_url = reverse_lazy('portal:post_list')
    permission_required = "portal.add_post"

    def form_valid(self, form):
        messages.success(self.request, "Berita berhasil diterbitkan!")
        return super().form_valid(form)

class PostUpdateView(BasePermissionMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "portal/posts/form.html"
    success_url = reverse_lazy('portal:post_list')
    permission_required = "portal.change_post"

    def form_valid(self, form):
        messages.success(self.request, "Berita berhasil diperbarui!")
        return super().form_valid(form)
