# users/selectors.py
def get_active_users():
    return User.objects.filter(is_active=True)

def search_users(query):
    return User.objects.filter(username__icontains=query)

