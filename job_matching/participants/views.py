from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError

from .models import Peserta
from .choices import StatusValidasi
from . import forms
from . import services


class PesertaListView(LoginRequiredMixin, View):

    def get(self, request):
        queryset = Peserta.objects.select_related("user")

        status = request.GET.get("status")
        if status:
            queryset = queryset.filter(status_validasi=status)

        paginator = Paginator(queryset, 10)
        page = request.GET.get("page")
        data = paginator.get_page(page)

        return render(request, "staff/peserta_list.html", {
            "data": data
        })


class PesertaCreateView(LoginRequiredMixin, View):

    def get(self, request):
        form = forms.PesertaForm()
        pendidikan = forms.RiwayatPendidikanFormSet()
        pekerjaan = forms.RiwayatPekerjaanFormSet()
        keluarga = forms.DataKeluargaFormSet()
        dokumen = forms.DokumenPesertaFormSet()

        return render(request, "participants/peserta_form.html", {
            "form": form,
            "pendidikan": pendidikan,
            "pekerjaan": pekerjaan,
            "keluarga": keluarga,
            "dokumen": dokumen
        })

    def post(self, request):
        form = forms.PesertaForm(request.POST)
        pendidikan = forms.RiwayatPendidikanFormSet(request.POST)
        pekerjaan = forms.RiwayatPekerjaanFormSet(request.POST)
        keluarga = forms.DataKeluargaFormSet(request.POST)
        dokumen = forms.DokumenPesertaFormSet(request.POST, request.FILES)

        if not form.is_valid():
            print("FORM ERROR:", form.errors)

        if not pendidikan.is_valid():
            print("PENDIDIKAN ERROR:", pendidikan.errors)

        if not pekerjaan.is_valid():
            print("PEKERJAAN ERROR:", pekerjaan.errors)

        if not keluarga.is_valid():
            print("KELUARGA ERROR:", keluarga.errors)

        if not dokumen.is_valid():
            print("DOKUMEN ERROR:", dokumen.errors)

        if all([
            form.is_valid(),
            pendidikan.is_valid(),
            pekerjaan.is_valid(),
            keluarga.is_valid(),
            dokumen.is_valid()
        ]):
            services.create_peserta(
                request.user,
                form,
                pendidikan,
                pekerjaan,
                keluarga,
                dokumen
            )
            return redirect("peserta_list")

        return render(request, "participants/peserta_form.html", {
            "form": form,
            "pendidikan": pendidikan,
            "pekerjaan": pekerjaan,
            "keluarga": keluarga,
            "dokumen": dokumen
        })


class PesertaProfileView(LoginRequiredMixin, View):

    def get(self, request, pk):
        peserta = get_object_or_404(Peserta, pk=pk)

        return render(request, "participants/profil_peserta.html", {
            "peserta": peserta
        })


class PesertaUpdateView(LoginRequiredMixin, View):

    def get(self, request, pk):
        peserta = get_object_or_404(Peserta, pk=pk)

        form = forms.PesertaForm(instance=peserta)
        pendidikan = forms.RiwayatPendidikanFormSet(instance=peserta)
        pekerjaan = forms.RiwayatPekerjaanFormSet(instance=peserta)
        keluarga = forms.DataKeluargaFormSet(instance=peserta)
        dokumen = forms.DokumenPesertaFormSet(instance=peserta)

        return render(request, "participants/peserta_form.html", {
            "form": form,
            "pendidikan": pendidikan,
            "pekerjaan": pekerjaan,
            "keluarga": keluarga,
            "dokumen": dokumen,
            "is_update": True,
        })

    def post(self, request, pk):
        peserta = get_object_or_404(Peserta, pk=pk)

        form = forms.PesertaForm(request.POST, instance=peserta)
        pendidikan = forms.RiwayatPendidikanFormSet(
            request.POST,
            instance=peserta
        )
        pekerjaan = forms.RiwayatPekerjaanFormSet(
            request.POST,
            instance=peserta
        )
        keluarga = forms.DataKeluargaFormSet(request.POST, instance=peserta)
        dokumen = forms.DokumenPesertaFormSet(
            request.POST,
            request.FILES,
            instance=peserta
        )

        if all([
            form.is_valid(),
            pendidikan.is_valid(),
            pekerjaan.is_valid(),
            keluarga.is_valid(),
            dokumen.is_valid()
        ]):
            services.update_peserta(
                request.user,
                peserta,
                form,
                pendidikan,
                pekerjaan,
                keluarga,
                dokumen
            )
            messages.success(request, "Profil berhasil diperbarui.")
            return redirect("peserta_profile", pk=pk)

        return render(request, "participants/peserta_form.html", {
            "form": form,
            "pendidikan": pendidikan,
            "pekerjaan": pekerjaan,
            "keluarga": keluarga,
            "dokumen": dokumen,
            "is_update": True,
        })


class PesertaValidateLevel1View(LoginRequiredMixin, View):

    def post(self, request, pk):
        peserta = get_object_or_404(Peserta, pk=pk)
        notes = request.POST.get("notes", "")
        services.validate_level_1(peserta, request.user, notes)
        return redirect("peserta_detail", pk=pk)


class PesertaDetailView(LoginRequiredMixin, View):

    def get(self, request, pk):
        peserta = get_object_or_404(Peserta, pk=pk)

        return render(request, "staff/peserta_detail.html", {
            "peserta": peserta,
            "status_choices": StatusValidasi.choices,
        })

    def post(self, request, pk):
        peserta = get_object_or_404(Peserta, pk=pk)
        status = request.POST.get("status_validasi", "")
        notes = request.POST.get("notes", "")

        try:
            services.update_validation_status(
                peserta=peserta,
                validator_user=request.user,
                status=status,
                notes=notes,
            )
            messages.success(
                request,
                "Status dan catatan validasi berhasil diperbarui.",
            )
        except ValidationError as error:
            messages.error(request, str(error))

        return redirect("peserta_detail", pk=pk)
