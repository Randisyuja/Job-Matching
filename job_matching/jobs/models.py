from django.db import models
from accounts.models import User
from datetime import date


ACCEPTED_APPLICATION_STATUSES = (
    "Goukaku",
    "Diterima",
)


class JenisPekerjaan(models.Model):
    nama_pekerjaan = models.CharField(
        "Nama Pekerjaan",
        max_length=100,
        blank=False,
        null=False
    )
    file_path = models.FileField(
        "Icon/Image",
        upload_to="pekerjaan/tipe/",
        blank=True,
        null=False
    )

    class Meta:
        db_table = "jenis_pekerjaan"
        verbose_name = "Jenis Pekerjaan"
        verbose_name_plural = "Jenis Pekerjaan"

    def __str__(self):
        return self.nama_pekerjaan


class Lowongan(models.Model):
    nama_perusahaan = models.CharField(
        "Nama Perusahaan",
        max_length=100,
        blank=False,
        null=False
    )
    jenis_pekerjaan = models.ForeignKey(
        JenisPekerjaan,
        on_delete=models.PROTECT,
        related_name="lowongan",
        verbose_name="Jenis Pekerjaan"
    )
    kuota = models.IntegerField(
        "Kuota",
        blank=False,
        null=False
    )
    batas_bawah_usia = models.IntegerField(
        "Batas Bawah Usia",
        blank=False,
        null=False
    )
    batas_atas_usia = models.IntegerField(
        "Batas Atas Usia",
        blank=False,
        null=False,
    )
    lokasi_kerja = models.CharField(
        "Lokasi Kerja",
        max_length=50,
        blank=False,
        null=False
    )
    deskripsi_pekerjaan = models.TextField(
        "Deskripsi Pekerjaan",
        blank=True,
        null=True
    )
    batas_lamar = models.DateField(
        "Batas Lamar",
        blank=False,
        null=False
    )
    is_active = models.BooleanField(
        "Aktif",
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(
        "Tanggal Dibuat",
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        "Tanggal Diupdate",
        auto_now=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="dibuat_oleh",
        verbose_name="Dibuat oleh",
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="diupdate_oleh",
        verbose_name="Diupdate oleh",
        null=True,
        blank=True
    )

    class Meta:
        db_table = "lowongan"
        verbose_name = "Lowongan"
        verbose_name_plural = "Lowongan"

    def __str__(self):
        return (
            f"{self.nama_perusahaan} - "
            f"{self.jenis_pekerjaan.nama_pekerjaan}"
        )

    def save(self, *args, **kwargs):
        # Pastikan lowongan otomatis non aktif saat sudah terlaksana.
        if self.is_completed:
            self.is_active = False
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        if not self.batas_lamar:
            return False
        return date.today() > self.batas_lamar

    @property
    def sisa_kuota(self):
        """Calculate remaining quota"""
        if not self.pk:
            return max(0, self.kuota)

        approved_count = self.lamaran.filter(
            status_lamaran__in=ACCEPTED_APPLICATION_STATUSES
        ).count()
        return max(0, self.kuota - approved_count)

    @property
    def is_completed(self):
        return self.is_expired or self.sisa_kuota <= 0

    @property
    def status_label(self):
        if self.is_completed:
            return "Sudah Terlaksana"
        if self.is_active:
            return "Aktif"
        return "Tutup"

    def apply_completion_rules(self):
        if self.is_completed and self.is_active:
            type(self).objects.filter(pk=self.pk).update(is_active=False)
            self.is_active = False


class Persyaratan(models.Model):
    lowongan = models.ForeignKey(
        Lowongan,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="persyaratan",
        verbose_name="Lowongan"
    )
    name = models.CharField(
        "Persyaratan",
        max_length=50,
        blank=False,
        null=False
    )

    class Meta:
        db_table = "persyaratan"
        verbose_name = "Persyaratan"
        verbose_name_plural = "Persyaratan"

    def __str__(self):
        return f"{self.name}"
