from django.db import models
from accounts.models import User
from participants.models import Peserta
from jobs.models import Lowongan
from .choices import StatusLamaran


class Lamaran(models.Model):
    peserta = models.ForeignKey(
        Peserta,
        on_delete=models.CASCADE,
        related_name="lamaran",
        verbose_name="Peserta"
    )
    lowongan = models.ForeignKey(
        Lowongan,
        on_delete=models.CASCADE,
        related_name="lamaran",
        verbose_name="Lowongan"
    )
    status_lamaran = models.CharField(
        "Status Lamaran",
        choices=StatusLamaran.choices,
        default=StatusLamaran.PENDING,
        max_length=50,
        blank=False
    )
    catatan = models.TextField(
        "Catatan"
    )
    created_at = models.DateTimeField(
        "Tanggal Dibuat",
        auto_now_add=True
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='lamaran_created',
        verbose_name='Dibuat Oleh',
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(
        "Tanggal Diupdate",
        auto_now=True
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='lamaran_updated',
        verbose_name='Diupdate Oleh',
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.pk and not self.peserta.can_apply_jobs:
            raise ValueError(
                "Peserta belum approved. Profil harus disetujui sebelum "
                "melamar."
            )

        if not self.lowongan.is_active and not self.pk:
            raise ValueError('Lowongan sudah tidak aktif')

        if self.lowongan.is_expired and not self.pk:
            raise ValueError(
                'Tidak dapat melamar ke lowongan yang sudah ditutup'
            )

        if self.lowongan.sisa_kuota <= 0 and not self.pk:
            raise ValueError('Kuota lowongan sudah penuh')

        super().save(*args, **kwargs)
        self.lowongan.apply_completion_rules()
