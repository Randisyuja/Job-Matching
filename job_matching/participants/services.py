from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Peserta
from .choices import StatusValidasi


@transaction.atomic
def create_peserta(
    user,
    peserta_form,
    pendidikan_formset,
    pekerjaan_formset,
    keluarga_formset,
    dokumen_formset
):
    peserta = peserta_form.save(commit=False)
    peserta.user = user
    peserta.updated_by = user
    peserta.save()

    pendidikan_formset.instance = peserta
    pendidikan_formset.save()

    pekerjaan_formset.instance = peserta
    pekerjaan_formset.save()

    keluarga_formset.instance = peserta
    keluarga_formset.save()

    dokumen_formset.instance = peserta
    dokumen_formset.save()

    return peserta


@transaction.atomic
def update_peserta(
    user,
    peserta,
    peserta_form,
    pendidikan_formset,
    pekerjaan_formset,
    keluarga_formset,
    dokumen_formset
):
    peserta = peserta_form.save(commit=False)
    peserta.updated_by = user
    peserta.save()

    pendidikan_formset.save()
    pekerjaan_formset.save()
    keluarga_formset.save()
    dokumen_formset.save()

    return peserta


def validate_level_1(peserta: Peserta, validator_user, notes=""):
    if peserta.status_validasi != StatusValidasi.DIAJUKAN:
        raise ValidationError("Status tidak bisa divalidasi level 1")

    peserta.status_validasi = StatusValidasi.VALIDATED_1
    peserta.validasi_1_pada = timezone.now()
    peserta.validasi_1_oleh = validator_user
    peserta.validasi_1_notes = notes
    peserta.save()
    return peserta


def validate_level_2(peserta: Peserta, validator_user, notes=""):
    if peserta.status_validasi != StatusValidasi.VALIDATED_1:
        raise ValidationError("Harus lolos validasi level 1 dulu")

    peserta.status_validasi = StatusValidasi.VALIDATED_2
    peserta.validasi_2_pada = timezone.now()
    peserta.validasi_2_oleh = validator_user
    peserta.validasi_2_notes = notes
    peserta.save()
    return peserta


def final_approve(peserta):
    peserta.final_approve()
