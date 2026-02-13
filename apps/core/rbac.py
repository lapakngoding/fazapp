SYSTEM_ROLES = {
    "SUPERADMIN": {
        "description": "Full system access",
        "permissions": "__all__",
    },
    "ADMIN": {
        "description": "Manage users and groups",
        "permissions": [
            "core.view_user",
            "core.add_user",
            "core.change_user",
            "core.delete_user",
            "auth.view_group",
            "auth.add_group",
            "auth.change_group",
            "auth.delete_group",
            "core.view_auditlog",
        ],
    },
    "STAFF": {
        "description": "Basic access",
        "permissions": [
            "core.view_user",
        ],
    },
}

