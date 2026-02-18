from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import logout, get_user_model
from django.shortcuts import redirect
from apps.core.decorators import role_required
import json
from django.db.models.functions import TruncMonth
from django.db.models import Q, Count
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, TemplateView
from apps.core.models import AuditLog
from django.contrib.auth.models import Group
from django.conf import settings
from apps.users.selectors import get_dashboard_stats, get_user_growth_data


User = get_user_model()

class CustomLoginView(LoginView):
    template_name = "themes/default/auth/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("core:dashboard")

def logout_view(request):
    logout(request)
    return redirect('core:login')

class DashboardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        theme = getattr(settings, 'THEME', 'default')
        return [f"themes/{theme}/dashboard.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Mapping Permissions
        can_view_stats = user.is_superuser or user.has_perm('core.view_user_stats')
        can_view_charts = user.is_superuser or user.has_perm('core.view_charts')
        can_view_logs = user.is_superuser or user.has_perm('core.view_logs')
        
        context.update({
            'can_view_user_stats': can_view_stats,
            'can_view_charts': can_view_charts,
            'can_view_logs': can_view_logs,
            'now': timezone.now(), # Untuk <small>Login time: {{ now }}</small>
        })

        if can_view_stats or can_view_logs:
            # Ambil data dari selector
            stats = get_dashboard_stats()
            context.update(stats)
        
        if can_view_charts:
            growth_data = get_user_growth_data()
            context["page_title"] = "Dashboard"
            context['chart_labels'] = growth_data['labels']
            context['chart_data'] = growth_data['data']

        return context

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

    def get_target_url(self):
        from django.urls import reverse

        model_url_map = {
            "User": "users:edit",
            "Group": "users:group_edit",
        }

        model_name = self.target_model.split(".")[-1]  # aman kalau ada app label

        url_name = model_url_map.get(model_name)

        if url_name:
            try:
                return reverse(url_name, kwargs={"pk": self.target_id})
            except:
                return "#"

        return "#"


