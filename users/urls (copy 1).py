from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.user_list, name="list"),
    path("add/", views.user_create, name="add"),
    path("<int:pk>/disable/", views.user_disable, name="disable"),
    #path("create/", views.user_create, name="create"),
    path("profile/", views.profile, name="profile"),
    path("change-password/", views.change_password, name="change_password"),
]

