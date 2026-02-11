from django.urls import path
from . import views
from .views import CustomLoginView, dashboard

app_name = "core"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path("login/", CustomLoginView.as_view(), name="login"),
    path('logout/', views.logout_view, name='logout'),
]

