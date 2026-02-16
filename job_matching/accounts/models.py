from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    email = models.EmailField("Email Address", unique=True, blank=False, null=False)
    is_active = models.BooleanField("Aktif", default=True)
    created_at = models.DateTimeField("Tanggal Dibuat", auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.email}"


class Staff(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='staff_profile'
    )
    nama = models.CharField(
        "Nama",
        max_length=50,
        blank=False
    )
    jabatan = models.CharField(
        "Jabatan",
        max_length=50,
        blank=False
    )
    unit_kerja = models.CharField(
        "Unit Kerja",
        max_length=100,
        blank=False
    )
    nomor_hp = models.CharField(
        "Nomor HP",
        max_length=50,
        blank=False
    )
    is_active = models.BooleanField(
        "Aktif",
        max_length=50,
        blank=False
    )

    class Meta:
        db_table = "staff"
        verbose_name = "Staff"
        verbose_name_plural = "Staff"

    def __str__(self):
        return f"{self.name} - {self.jabatan}"
