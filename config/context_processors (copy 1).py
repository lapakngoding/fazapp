from django.conf import settings
from apps.core.menu import SIDEBAR_MENU
from django.urls import resolve

def global_settings(request):
    return {
        'THEME': settings.THEME,
    }


def sidebar_menu(request):
    if not request.user.is_authenticated:
        return {}

    current_url = resolve(request.path_info).url_name
    output = []

    for item in SIDEBAR_MENU:

        # 🔥 FILTER STAFF ONLY
        if item.get("staff_only") and not request.user.is_staff:
            continue

        item = item.copy()

        # ===== MENU TANPA CHILDREN =====
        if "children" not in item:
            item["active"] = (current_url == item["url"].split(":")[-1])
            output.append(item)
            continue

        # ===== MENU DENGAN CHILDREN =====
        active_child = False
        filtered_children = []

        for child in item["children"]:
            # kalau nanti mau tambah permission di child level
            if child.get("staff_only") and not request.user.is_staff:
                continue

            if current_url == child["url"].split(":")[-1]:
                active_child = True

            filtered_children.append(child)

        # kalau semua child ke-filter, jangan tampilkan parent
        if not filtered_children:
            continue

        item["children"] = filtered_children
        item["active"] = active_child
        output.append(item)

    return {
        "SIDEBAR_MENU": output
    }



