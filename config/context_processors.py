from django.conf import settings
from apps.core.menu import SIDEBAR_MENU
from django.urls import resolve

def global_settings(request):
    return {
        'THEME': settings.THEME,
    }

def has_permission(user, item):
    """
    Cek apakah user punya permission untuk item.
    Support:
    - permission (string)
    - permissions (list)
    - custom lambda
    """

    # custom lambda
    if callable(item.get("permission")):
        return item["permission"](user)

    # single permission
    if "permission" in item:
        return user.has_perm(item["permission"])

    # multiple permissions
    if "permissions" in item:
        return all(user.has_perm(p) for p in item["permissions"])

    # kalau tidak ada permission field → tampilkan
    return True


from copy import deepcopy

def sidebar_menu(request):
    if not request.user.is_authenticated:
        return {}

    # Gunakan view_name lengkap (misal: 'users:list')
    resolver = resolve(request.path_info)
    current_full_url = f"{resolver.namespace}:{resolver.url_name}" if resolver.namespace else resolver.url_name
    
    output = []
    for item in SIDEBAR_MENU:
        item_copy = item.copy()
        if not has_permission(request.user, item_copy):
            continue

        if "children" not in item_copy:
            # Bandingkan full URL name agar presisi
            item_copy["active"] = (current_full_url == item_copy["url"])
            output.append(item_copy)
            continue

        filtered_children = []
        active_child = False
        for child in item_copy["children"]:
            if not has_permission(request.user, child):
                continue
            
            # Cek jika salah satu child sedang aktif
            if current_full_url == child["url"]:
                child["active"] = True # Tambahkan flag active ke child juga
                active_child = True
            
            filtered_children.append(child)

        if filtered_children:
            item_copy["children"] = filtered_children
            item_copy["active"] = active_child
            output.append(item_copy)

    return {"SIDEBAR_MENU": output}

from portal.selectors.portal_selectors import get_site_identity

def portal_context(request):
    return {
        'portal': get_site_identity()
    }
