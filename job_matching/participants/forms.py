from django import forms
from django.forms import inlineformset_factory
from .models import (
    Peserta,
    RiwayatPendidikan,
    RiwayatPekerjaan,
    DataKeluarga,
    DokumenPeserta,
)


class PesertaForm(forms.ModelForm):
    class Meta:
        model = Peserta
        exclude = [
            "user",
            "status_validasi",
            "validasi_1_pada",
            "validasi_1_oleh",
            "validasi_1_notes",
            "validasi_2_pada",
            "validasi_2_oleh",
            "validasi_2_notes",
            "tervalidasi_pada",
            "alasan_penolakan",
            "created_at",
            "updated_at",
            "updated_by",
        ]
        widgets = {
            "tanggal_lahir": forms.DateInput(attrs={"type": "date"})
        }




class RiwayatPendidikanForm(forms.ModelForm):
    tahun_masuk = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"})
    )
    tahun_lulus = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = RiwayatPendidikan
        fields = "__all__"
        widgets = {
            "tahun_masuk": forms.DateInput(attrs={"type": "date"}),
            "tahun_lulus": forms.DateInput(attrs={"type": "date"}),
        }


class RiwayatPekerjaanForm(forms.ModelForm):
    tanggal_masuk = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"})
    )
    tanggal_keluar = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = RiwayatPekerjaan
        fields = "__all__"


class DataKeluargaForm(forms.ModelForm):
    tanggal_lahir = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = DataKeluarga
        fields = "__all__"
        widgets = {
            "tanggal_lahir": forms.DateInput(attrs={"type": "date"}),
        }


class DokumenPesertaForm(forms.ModelForm):
    class Meta:
        model = DokumenPeserta
        fields = "__all__"


RiwayatPendidikanFormSet = inlineformset_factory(
    Peserta,
    RiwayatPendidikan,
    form=RiwayatPendidikanForm,
    extra=1,
    can_delete=False
)

RiwayatPekerjaanFormSet = inlineformset_factory(
    Peserta,
    RiwayatPekerjaan,
    form=RiwayatPekerjaanForm,
    extra=1,
    can_delete=False
)

DataKeluargaFormSet = inlineformset_factory(
    Peserta,
    DataKeluarga,
    form=DataKeluargaForm,
    extra=1,
    can_delete=False
)

DokumenPesertaFormSet = inlineformset_factory(
    Peserta,
    DokumenPeserta,
    form=DokumenPesertaForm,
    extra=1,
    can_delete=False
)
