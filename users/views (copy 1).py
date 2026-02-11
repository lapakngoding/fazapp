from django.shortcuts import get_object_or_404, render, redirect
from apps.core.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import ProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import BootstrapPasswordChangeForm
from .forms import UserCreateForm
from django.contrib.auth import get_user_model

User = get_user_model()

def staff_required(user):
    return user.is_staff

@login_required
@user_passes_test(staff_required)
def user_list(request):
    users = User.objects.all().order_by("-date_joined")
    return render(request, "users/list.html", {
        "page_title": "Users Management",
        "users": users
    })

@login_required
@user_passes_test(staff_required)
def user_disable(request, pk):
    target_user = get_object_or_404(User, pk=pk)

    # optional safety: jangan disable diri sendiri
    if target_user == request.user:
        messages.error(request, "You cannot disable your own account.")
        return redirect("users:list")

    if request.method == "POST":
        target_user.is_active = not target_user.is_active
        target_user.save()

        status = "activated" if target_user.is_active else "disabled"
        messages.success(
            request,
            f"User '{target_user.email}' successfully {status}."
        )
        return redirect("users:list")

    return render(request, "users/confirm_disable.html", {
        "target_user": target_user,
        "page_title": "Disable User" if target_user.is_active else "Activate User"
    })

@login_required
def profile(request):
    user = request.user

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("users:profile")
    else:
        form = ProfileForm(instance=user)

    return render(request, "users/profile.html", {
        "page_title": "Users Profile",
        "form": form
    })

@login_required
def change_password(request):
    if request.method == "POST":
        form = BootstrapPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(request, "Password berhasil diubah.")
            return redirect("users:change_password")

        else:
            messages.error(request, 'Gagal mengubah password. Periksa kembali input Anda.')

    else:
        form = BootstrapPasswordChangeForm(request.user)

    return render(request, "users/change_password.html", {
        "page_title": "Profile Ubah Password",
        "form": form
    })

@login_required
@user_passes_test(staff_required)
def user_create(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()

            messages.success(request, "User berhasil ditambahkan")
            return redirect("users:list")
    else:
        form = UserCreateForm()

    return render(request, "users/create.html", {
        "form": form,
        "page_title": "Add User"
    })
