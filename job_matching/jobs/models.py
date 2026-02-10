from django.db import models
from accounts.models import User


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
        blank=False,
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
        blank=False,
        null=False
    )
    updated_at = models.DateTimeField(
        "Tanggal Diupdate",
        blank=False,
        null=False
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
        return f"{self.nama_perusahaan} - {self.jenis_pekerjaan.nama_pekerjaan}"


class Persyaratan(models.Model):
    lowongan = models.ForeignKey(
        Lowongan,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
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
