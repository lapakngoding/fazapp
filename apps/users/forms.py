from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from apps.core.models import User
from django.contrib.auth.models import Group, Permission

User = get_user_model()

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "avatar"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

class BootstrapPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Password Lama",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password lama",
            "id": "id_old_password"
        })
    )

    new_password1 = forms.CharField(
        label="Password Baru",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password baru",
            "id": "id_new_password1"
        })
    )

    new_password2 = forms.CharField(
        label="Konfirmasi Password Baru",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Ulangi password baru",
            "id": "id_new_password2"
        })
    )


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password"
        })
    )

    password2 = forms.CharField(
        label="Ulangi Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password harus sama"
        })
    )

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            "class": "form-control"
        })
    )

    class Meta:
        model = User
        fields = ("email", "is_staff", "groups")
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "contoh: nama@email.com"
            }),
            "is_staff": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            })
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Password tidak sama")

        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
            self.save_m2m()   # 🔥 penting untuk groups

        return user

class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password Baru (opsional)",
        required=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Kosongkan jika tidak ingin mengubah password"
        })
    )

    password2 = forms.CharField(
        label="Ulangi Password",
        required=False,
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            "class": "form-control"
        })
    )

    class Meta:
        model = User
        fields = ("email", "is_staff", "groups")
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),
            "is_staff": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            })
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")

        if p1 or p2:
            if p1 != p2:
                raise forms.ValidationError("Password tidak sama")

        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)

        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)

        if commit:
            user.save()
            self.save_m2m()

        return user

def form_valid(self, form):
    self.object = UserService.create_user(form)
    messages.success(self.request, "User berhasil ditambahkan")
    return super().form_valid(form)

class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # 🔥 penting
        required=False
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]

