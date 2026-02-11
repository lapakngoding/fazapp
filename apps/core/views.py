from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout, get_user_model
from django.shortcuts import redirect
from django.utils import timezone
from apps.core.decorators import role_required

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

