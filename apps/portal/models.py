from django.db import models

class SiteIdentity(models.Model):
    # Basic Info
    name = models.CharField(max_length=100, default="FazApp Portal")
    tagline = models.CharField(max_length=255, blank=True)
    logo = models.ImageField(upload_to='portal/logos/', blank=True, null=True)
    favicon = models.ImageField(upload_to='portal/favicons/', blank=True, null=True)
    
    # Metadata SEO
    meta_description = models.TextField(blank=True, help_text="Untuk SEO Google")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="Pisahkan dengan koma")

    # Footer/Contact
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "Site Identity"
        verbose_name_plural = "Site Identities"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Memastikan hanya ada satu baris data (Singleton Pattern)
        if not self.pk and SiteIdentity.objects.exists():
            return 
        super().save(*args, **kwargs)

class Banner(models.Model):
    title = models.CharField(max_length=200, verbose_name="Judul Banner")
    description = models.TextField(blank=True, verbose_name="Deskripsi")
    image = models.ImageField(upload_to='portal/banners/', verbose_name="Foto Banner")
    url = models.CharField(max_length=255, blank=True, verbose_name="Link URL (CTA)")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    order = models.PositiveIntegerField(default=0, verbose_name="Urutan")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def __str__(self):
        return self.title
