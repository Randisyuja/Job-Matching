from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email harus diisi")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser harus memiliki is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser harus memiliki is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    username = None
    email = models.EmailField("Email Address", unique=True, blank=False, null=False)
    is_active = models.BooleanField("Aktif", default=True)
    created_at = models.DateTimeField("Tanggal Dibuat", auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

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
        default=True
    )

    class Meta:
        db_table = "staff"
        verbose_name = "Staff"
        verbose_name_plural = "Staff"

    def __str__(self):
        return f"{self.nama} - {self.jabatan}"
