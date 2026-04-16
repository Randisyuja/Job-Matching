from django.db import transaction
from django.core.exceptions import ValidationError
from participants.models import Peserta


@transaction.atomic
def create_lamaran(user, form):
    try:
        peserta = user.peserta_profile
    except Peserta.DoesNotExist as exc:
        raise ValidationError("User bukan peserta") from exc

    if not peserta.can_apply_jobs:
        raise ValidationError(
            "Peserta belum approved. Profil harus disetujui sebelum melamar."
        )

    lamaran = form.save(commit=False)
    lamaran.peserta = peserta
    lamaran.created_by = user
    lamaran.updated_by = user
    lamaran.save()

    return lamaran


def update_status(user, lamaran, form):
    lamaran = form.save(commit=False)
    lamaran.updated_by = user
    lamaran.save()
    lamaran.lowongan.apply_completion_rules()
    return lamaran


def delete_lamaran(lamaran):
    lamaran.delete()
