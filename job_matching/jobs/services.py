from django.core.exceptions import ValidationError
from .models import Lowongan, Persyaratan


# Jenis Pekerjaan
def create_jenis(form):
    return form.save()


def update_jenis(form):
    return form.save()


def delete_jenis(jenis):
    if Lowongan.objects.filter(jenis_pekerjaan=jenis, is_active=True).exists():
        raise ValidationError(
            "Tidak bisa dihapus karena masih digunakan oleh lowongan aktif."
        )
    jenis.delete()


# Lowongan
def create_lowongan(lowongan_form, formset, user):
    lowongan = lowongan_form.save(commit=False)
    lowongan.save()

    formset.instance = lowongan
    formset.save()

    return lowongan


def update_lowongan(form, user):
    lowongan = form.save(commit=False)
    lowongan.updated_by = user
    lowongan.save()
    return lowongan


def delete_lowongan(obj):
    obj.delete()


def sync_lowongan_completion_status():
    active_lowongan = Lowongan.objects.filter(is_active=True)
    for lowongan in active_lowongan:
        lowongan.apply_completion_rules()


def get_all_lowongan():
    sync_lowongan_completion_status()
    return Lowongan.objects.all()


def get_active_lowongan(is_active):
    sync_lowongan_completion_status()
    return Lowongan.objects.filter(is_active=is_active)


def get_lowongan_detail(pk):
    sync_lowongan_completion_status()
    lowongan = Lowongan.objects.get(pk=pk)
    persyaratan = Persyaratan.objects.filter(lowongan=lowongan)
    return lowongan, persyaratan


# Persyaratan
def create_persyaratan(form):
    lowongan = form.cleaned_data["lowongan"]
    name = form.cleaned_data["name"]

    duplicate = Persyaratan.objects.filter(
        lowongan=lowongan,
        name__iexact=name
    ).exists()

    if duplicate:
        raise ValidationError(
            "Persyaratan dengan nama yang sama sudah ada pada lowongan ini."
        )

    return form.save()


def update_persyaratan(form):
    lowongan = form.cleaned_data["lowongan"]
    name = form.cleaned_data["name"]

    duplicate = Persyaratan.objects.filter(
        lowongan=lowongan,
        name__iexact=name
    ).exclude(pk=form.instance.pk).exists()

    if duplicate:
        raise ValidationError(
            "Persyaratan dengan nama yang sama sudah ada pada lowongan ini."
        )

    return form.save()


def delete_persyaratan(obj):
    obj.delete()
