from django.urls import path
from .views import (
    UserListView,
    UserCreateView,
    UserDisableView,
    ProfileView,
    UserUpdateView,
    ChangePasswordView,
    GroupListView,
    GroupCreateView,
    GroupUpdateView,
    GroupDeleteView,
)

app_name = "users"

urlpatterns = [
    path("", UserListView.as_view(), name="list"),
    path("add/", UserCreateView.as_view(), name="add"),
    path("<int:pk>/disable/", UserDisableView.as_view(), name="disable"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("groups/", GroupListView.as_view(), name="group_list"),
    path("groups/add/", GroupCreateView.as_view(), name="group_add"),
    path("groups/<int:pk>/edit/", GroupUpdateView.as_view(), name="group_edit"),
    path("groups/<int:pk>/delete/", GroupDeleteView.as_view(), name="group_delete"),
    path("<int:pk>/edit/", UserUpdateView.as_view(), name="edit"),
]

