from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nip = models.CharField(max_length=20, unique=True, verbose_name="NIP/NUPTK")
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    specialization = models.CharField(max_length=100, help_text="Mata Pelajaran Utama")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.nip})"

# apps/akademik/models.py

class Classroom(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nama Kelas")
    # OneToOneField memastikan satu guru hanya bisa jadi wali di satu kelas
    teacher = models.OneToOneField(
        Teacher, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='homeroom',
        verbose_name="Wali Kelas"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kelas"
        verbose_name_plural = "Kelas"
