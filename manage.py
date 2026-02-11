#!/usr/bin/env python
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))  # ← TAMBAHKAN INI

def main():
    # 🔥 PAKSA Django pakai development settings
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'config.settings.development'
    )

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django."
        ) from exc

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

