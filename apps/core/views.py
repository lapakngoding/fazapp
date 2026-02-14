from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout, get_user_model
from django.shortcuts import redirect
from django.utils import timezone
from apps.core.decorators import role_required
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView
from apps.core.models import AuditLog

User = get_user_model()

class CustomLoginView(LoginView):
    template_name = "themes/default/auth/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("core:dashboard")

def logout_view(request):
    logout(request)
    return redirect('core:login')

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html', {
        "page_title": "Dashboard",
        "total_users": User.objects.count(),
        "last_login": request.user.last_login,
        "now": timezone.now(),
    })

def permission_denied_view(request, exception):
    return render(request, "themes/default/errors/403.html", status=403)


def page_not_found_view(request, exception):
    return render(request, "themes/default/errors/404.html", status=404)


class AuditLogListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AuditLog
    template_name = "core/audit_log_list.html"
    context_object_name = "logs"
    paginate_by = 5
    permission_required = "core.view_auditlog"

    def get_queryset(self):
        queryset = super().get_queryset().select_related("actor")

        q = self.request.GET.get("q")
        actor = self.request.GET.get("actor")
        date = self.request.GET.get("date")

        if q:
            queryset = queryset.filter(
                Q(description__icontains=q) |
                Q(target_model__icontains=q)
            )

        if actor:
            queryset = queryset.filter(actor__id=actor)

        if date:
            parsed_date = parse_date(date)
            if parsed_date:
                queryset = queryset.filter(created_at__date=parsed_date)

        return queryset.order_by("-created_at")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Audit Logs"
        return context



