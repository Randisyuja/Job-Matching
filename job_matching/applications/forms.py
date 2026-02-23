from django import forms
from .models import Lamaran


class LamaranCreateForm(forms.ModelForm):
    class Meta:
        model = Lamaran
        fields = ["lowongan", "catatan"]


class LamaranUpdateStatusForm(forms.ModelForm):
    class Meta:
        model = Lamaran
        fields = ["status_lamaran", "catatan"]
