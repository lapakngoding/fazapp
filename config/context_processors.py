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

    current_url = resolve(request.path_info).url_name
    output = []

    for item in SIDEBAR_MENU:
        item_copy = item.copy()

        # ===== CHECK PERMISSION PARENT =====
        if not has_permission(request.user, item_copy):
            continue

        # ===== TANPA CHILD =====
        if "children" not in item_copy:
            item_copy["active"] = (
                current_url == item_copy["url"].split(":")[-1]
            )
            output.append(item_copy)
            continue

        # ===== DENGAN CHILD =====
        filtered_children = []
        active_child = False

        for child in item_copy["children"]:
            if not has_permission(request.user, child):
                continue

            if current_url == child["url"].split(":")[-1]:
                active_child = True

            filtered_children.append(child)

        if not filtered_children:
            continue

        item_copy["children"] = filtered_children
        item_copy["active"] = active_child
        output.append(item_copy)

    return {
        "SIDEBAR_MENU": output
    }

