from django import forms
from django.forms import inlineformset_factory
from .models import Lowongan, JenisPekerjaan, Persyaratan


class JenisPekerjaanForm(forms.ModelForm):
    class Meta:
        model = JenisPekerjaan
        fields = ["nama_pekerjaan", "file_path"]


class LowonganForm(forms.ModelForm):
    class Meta:
        model = Lowongan
        fields = [
            "nama_perusahaan",
            "jenis_pekerjaan",
            "kuota",
            "batas_bawah_usia",
            "batas_atas_usia",
            "lokasi_kerja",
            "deskripsi_pekerjaan",
            "batas_lamar",
            "is_active",
        ]
        widgets = {
            "batas_lamar": forms.DateInput(attrs={"type": "date"})
        }

    def clean(self):
        cleaned_data = super().clean()

        usia_bawah = cleaned_data.get("batas_bawah_usia")
        usia_atas = cleaned_data.get("batas_atas_usia")

        if usia_bawah and usia_atas and usia_bawah > usia_atas:
            raise forms.ValidationError(
                "Batas bawah usia tidak boleh lebih besar dari batas atas usia."
            )

        return cleaned_data


class PersyaratanForm(forms.ModelForm):
    class Meta:
        model = Persyaratan
        fields = ["lowongan", "name"]


PersyaratanFormSet = inlineformset_factory(
    Lowongan,
    Persyaratan,
    fields=("name",),
    extra=1,
    can_delete=False
)
