from django.contrib.auth import get_user_model
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group
from django.db.models.functions import TruncMonth
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def get_all_users():
    # Hapus .select_related('profile')
    return User.objects.prefetch_related('groups').all().order_by('-date_joined')

def get_dashboard_stats():
    return {
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'staff_users': User.objects.filter(is_staff=True).count(),
        'superusers': User.objects.filter(is_superuser=True).count(),
        'total_groups': Group.objects.count(),
        'total_logs': LogEntry.objects.count(),
        'recent_logs': LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:10],
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

def search_users(query=None):
    """Selector untuk mencari user"""
    queryset = User.objects.all()
    if query:
        queryset = queryset.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )
    return queryset
