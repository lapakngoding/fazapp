from django.urls import path
from .views.dashboard import DashboardView, CustomLoginView, AuditLogListView
from django.contrib.auth.views import LogoutView


app_name = "core"

urlpatterns = [
    #path("", DashboardView.as_view(), name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page='core:login'), name='logout'),
    path("audit-logs/", AuditLogListView.as_view(), name="audit_logs"),
]

