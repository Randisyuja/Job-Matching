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
        choices=StatusLamaran,
        default=StatusLamaran.PENDING,
        max_length=50,
        blank=False
    )
    catatan = models.TextField(
        "Catatan"
    )
    created_at = models.DateField(
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
    updated_at = models.DateField(
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
