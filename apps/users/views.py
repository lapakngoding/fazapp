from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, FormView, RedirectView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import update_session_auth_hash
from django import forms
from django.urls import reverse
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from .services import UserService, GroupService
from apps.core.mixins import BasePermissionMixin

from .forms import ProfileForm, BootstrapPasswordChangeForm, UserCreateForm, UserUpdateForm, GroupForm

User = get_user_model()


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Users Profile"
        return context

class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = "users/change_password.html"
    form_class = BootstrapPasswordChangeForm
    success_url = reverse_lazy("users:change_password")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, "Password berhasil diubah.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Gagal mengubah password.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Profile Ubah Password"
        return context

class UserListView(BasePermissionMixin, ListView):
    model = User
    template_name = "users/list.html"
    context_object_name = "users"
    permission_required = "core.view_user"
    raise_exception = True
    ordering = ["-date_joined"]
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q")

        if q:
            queryset = queryset.filter(
                Q(email__icontains=q) |
                Q(username__icontains=q)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Users Management"
        return context

class UserCreateView(LoginRequiredMixin, BasePermissionMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "users/create.html"
    success_url = reverse_lazy("users:list")
    permission_required = "core.add_user"

    def form_valid(self, form):
        self.object = UserService.create_user(
            form,
            actor=self.request.user
        )
        messages.success(self.request, "User berhasil ditambahkan")
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add User"
        return context

class UserDisableView(LoginRequiredMixin, PermissionRequiredMixin, RedirectView):
    permission_required = "core.change_user"

    def get(self, request, *args, **kwargs):
        target_user = get_object_or_404(User, pk=kwargs["pk"])

        if target_user == request.user:
            messages.error(request, "You cannot disable your own account.")
            return redirect("users:list")

        status = UserService.toggle_active(
            target_user,
            actor=request.user
        )

        messages.success(
            request,
            f"User '{target_user.email}' successfully {status}."
        )

        return redirect("users:list")

class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/edit.html"
    success_url = reverse_lazy("users:list")
    permission_required = "core.change_user"

    def form_valid(self, form):
        self.object = UserService.update_user(
            form,
            actor=self.request.user
        )
        messages.success(self.request, "User berhasil diperbarui.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Edit User"
        return context

class GroupListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Group
    template_name = "users/group_list.html"
    context_object_name = "groups"
    permission_required = "core.view_group"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Group Management"
        return context

class GroupCreateView(LoginRequiredMixin, BasePermissionMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = "users/group_form.html"
    success_url = reverse_lazy("users:group_list")
    permission_required = "core.add_group"

    def form_valid(self, form):
        GroupService.create_group(
            cleaned_data=form.cleaned_data,
            actor=self.request.user
        )

        messages.success(self.request, "Group berhasil dibuat.")
        return redirect(self.success_url)

class GroupUpdateView(LoginRequiredMixin, BasePermissionMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = "users/group_form.html"
    success_url = reverse_lazy("users:group_list")
    permission_required = "core.change_group"

    def form_valid(self, form):
        self.object = self.get_object()

        GroupService.update_group(
            instance=self.object,
            cleaned_data=form.cleaned_data,
            actor=self.request.user
        )

        messages.success(self.request, "Group berhasil diupdate.")
        return redirect(self.success_url)

class GroupDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Group
    template_name = "users/group_confirm_delete.html"
    success_url = reverse_lazy("users:group_list")
    permission_required = "core.delete_group"

    def form_valid(self, form):
        group = self.get_object()
        group_name = GroupService.delete_group(
            group,
            actor=self.request.user
        )

        messages.success(
            self.request,
            f"Group '{group_name}' berhasil dihapus."
        )

        return redirect(self.success_url)



