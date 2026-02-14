from django.urls import path
from . import views
from .views import CustomLoginView, dashboard, AuditLogListView

app_name = "core"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path("login/", CustomLoginView.as_view(), name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("audit-logs/", AuditLogListView.as_view(), name="audit_logs"),
]

