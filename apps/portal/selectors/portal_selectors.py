from apps.portal.models import Banner, SiteIdentity

def get_site_identity():
    """Selalu kembalikan instance pertama atau buat baru jika kosong"""
    obj, created = SiteIdentity.objects.get_or_create(id=1)
    return obj

def get_active_banners():
    return Banner.objects.filter(is_active=True)
