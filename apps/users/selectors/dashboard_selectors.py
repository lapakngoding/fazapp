from django.contrib.auth import get_user_model
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def get_dashboard_stats():
    # Mengambil user terakhir yang login (selain user saat ini jika ingin)
    last_user_login = User.objects.exclude(last_login__isnull=True).order_by('-last_login').first()
    
    return {
        'total_users': User.objects.count(),
        'staff_users': User.objects.filter(is_staff=True).count(),
        'superusers': User.objects.filter(is_superuser=True).count(),
        'total_groups': Group.objects.count(),
        'total_logs': LogEntry.objects.count(),
        'last_login': last_user_login.last_login if last_user_login else None,
        # Kita map LogEntry agar sesuai dengan template (actor, action, target_model, created_at)
        'recent_logs': [
            {
                'actor': log.user.email or log.user.username,
                'action': log.get_action_flag_display(),
                'target_model': log.content_type.model,
                'created_at': log.action_time
            } for log in LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:10]
        ],
    }

def get_user_growth_data():
    six_months_ago = timezone.now() - timedelta(days=180)
    growth = (
        User.objects.filter(date_joined__gte=six_months_ago)
        .annotate(month=TruncMonth('date_joined'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    return {
        'labels': [item['month'].strftime('%b %Y') for item in growth],
        'data': [item['count'] for item in growth],
    }
