from django.urls import reverse_lazy

SIDEBAR_MENU = [
    {
        "label": "Home",
        "icon": "fas fa-home",
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
    # Tambahkan entri ini ke dalam list SIDEBAR_MENU
    {
        "label": "Portal Management",
        "icon": "fas fa-desktop",
        "permissions": ["portal.change_siteidentity"],
        "children": [
            {
                "label": "Site Configuration",
                "url": "portal:settings",
                "permissions": ["portal.change_siteidentity"],
            },
            {
                "label": "Banner Slider",
                "url": "portal:banner_list",
                "permissions": ["portal.view_banner"],
            },
            {
                "label": "Berita & Artikel",
                "url": "portal:post_list",
                "permissions": ["portal.view_post"],
            },
        ],
    },
    # MENU SIM Akademik
    {
        'label': 'SIM Akademik',
        'icon': 'fas fa-fw fa-graduation-cap', # Icon FontAwesome
        "permissions": ["core.view_user"],
        'children': [
            {
                "label": "Dashboard",
                "url": "akademik:dashboard_akademik",
                "permissions": ["core.view_user"],
            },
            {
                "label": "Daftar Guru",
                "url": "akademik:teacher_list",
            },
            {
                "label": "Daftar Kelas",
                "url": "akademik:classroom_list",
            },
        ]
    },

]

