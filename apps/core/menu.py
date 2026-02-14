from django.urls import reverse_lazy

SIDEBAR_MENU = [
    {
        "label": "Dashboard",
        "icon": "fas fa-tachometer-alt",
        "url": "core:dashboard",
    },
    {
        "label": "Hsitories",
        "icon": "fas fa-history",
        "permissions": ["core.view_user"],
        "url": "core:audit_logs",
    },
    {
        "label": "Settings",
        "icon": "fas fa-cog",
        "children": [
            {
                "label": "Profile",
                "url": "users:profile",
            },
        ],
    },
    {
        "label": "Users",
        "icon": "fas fa-users",
        "permissions": ["core.view_user"],  # 🔥 pakai permission
        "children": [
            {
                "label": "User List",
                "url": "users:list",
                "permissions": ["core.view_user"],
            },
            {
                "label": "Tambah User",
                "url": "users:add",
                "permissions": ["core.add_user"],
            },
        ],
    },
    {
    "label": "Roles & Groups",
    "icon": "fas fa-user-shield",
    "children": [
        {
            "label": "Group List",
            "url": "users:group_list",
        },
        {
            "label": "Add Group",
            "url": "users:group_add",
        },
    ],
    "permission": "auth.view_group",
    },

]

