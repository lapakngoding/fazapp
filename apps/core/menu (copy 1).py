from django.urls import reverse_lazy

SIDEBAR_MENU = [
    {
        "label": "Dashboard",
        "icon": "fas fa-tachometer-alt",
        "url": "core:dashboard",
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
        "children": [
            {
                "label": "User List",
                "url": "users:list",
            },
            {
                "label": "Tambah User",
                "url": "users:add",
            },
        ],
        "staff_only": True,
    },

]


