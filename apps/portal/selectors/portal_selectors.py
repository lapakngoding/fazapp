from apps.portal.models import Banner, SiteIdentity, Post

def get_site_identity():
    """Selalu kembalikan instance pertama atau buat baru jika kosong"""
    obj, created = SiteIdentity.objects.get_or_create(id=1)
    return obj

def get_active_banners():
    return Banner.objects.filter(is_active=True)

def get_latest_posts(limit=3):
    """Ambil berita terbaru yang dipublish"""
    return Post.objects.filter(is_published=True).order_by('-created_at')[:limit]
