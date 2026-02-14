from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet

User = get_user_model()

def get_all_users() -> QuerySet:
    return User.objects.all()

def search_users(query: str) -> QuerySet:
    return User.objects.filter(
        Q(email__icontains=query) |
        Q(username__icontains=query)
    )

