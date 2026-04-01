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


class StaffPesertaListView(LoginRequiredMixin, View):

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


class StaffPesertaStatusListView(LoginRequiredMixin, View):
    status_value = ""
    template_name = ""
    page_title = ""

    def get(self, request):
        queryset = Peserta.objects.select_related("user").filter(
            status_validasi=self.status_value
        )

        paginator = Paginator(queryset.order_by("-updated_at"), 10)
        page = request.GET.get("page")
        data = paginator.get_page(page)

        return render(request, self.template_name, {
            "data": data,
            "page_title": self.page_title,
        })


class PesertaCreateView(LoginRequiredMixin, View):

    def _peserta_form(self, request):
        data = request.session.get("peserta_form")
        if data:
            return forms.PesertaForm(data)
        return forms.PesertaForm()

    def _pendidikan_formset(self, request):
        data = request.session.get("pendidikan_form")
        if data:
            return forms.RiwayatPendidikanFormSet(data)
        return forms.RiwayatPendidikanFormSet()

    def _pekerjaan_formset(self, request):
        data = request.session.get("pekerjaan_form")
        if data:
            return forms.RiwayatPekerjaanFormSet(data)
        return forms.RiwayatPekerjaanFormSet()

    def _keluarga_formset(self, request):
        data = request.session.get("keluarga_form")
        if data:
            return forms.DataKeluargaFormSet(data)
        return forms.DataKeluargaFormSet()

    def _dokumen_formset(self, request):
        return forms.DokumenPesertaFormSet()

    def _clear_session(self, request):
        keys = ["peserta_form", "pendidikan_form", "pekerjaan_form", "keluarga_form"]
        for key in keys:
            request.session.pop(key, None)

    def get(self, request):
        step = request.GET.get("step", "1")
        context = {
            "current_step": step,
            "form": self._peserta_form(request),
            "pendidikan": self._pendidikan_formset(request),
            "pekerjaan": self._pekerjaan_formset(request),
            "keluarga": self._keluarga_formset(request),
            "dokumen": self._dokumen_formset(request),
        }
        return render(request, "peserta/peserta_form.html", context)

    def post(self, request):
        step = request.POST.get("step", "1")

        if step in ["1", "2", "3", "4", "5", "6"]:
            form = forms.PesertaForm(request.POST)
            if form.is_valid():
                request.session["peserta_form"] = request.POST
                return redirect(f"{request.path}?step={int(step) + 1}")
            return render(request, "peserta/peserta_form.html", {"form": form, "current_step": step})

        if step == "7":
            pendidikan = forms.RiwayatPendidikanFormSet(request.POST)
            if pendidikan.is_valid():
                request.session["pendidikan_form"] = request.POST
                return redirect(f"{request.path}?step=8")
            return render(request, "peserta/peserta_form.html", {"pendidikan": pendidikan, "current_step": step})

        if step == "8":
            pekerjaan = forms.RiwayatPekerjaanFormSet(request.POST)
            keluarga = forms.DataKeluargaFormSet(request.POST)
            dokumen = forms.DokumenPesertaFormSet(request.POST, request.FILES)

            peserta = forms.PesertaForm(request.session.get("peserta_form", {}))
            pendidikan = forms.RiwayatPendidikanFormSet(request.session.get("pendidikan_form", {}))

            if all([peserta.is_valid(), pendidikan.is_valid(), pekerjaan.is_valid(), keluarga.is_valid(), dokumen.is_valid()]):
                services.create_peserta(
                    request.user,
                    peserta,
                    pendidikan,
                    pekerjaan,
                    keluarga,
                    dokumen,
                )
                self._clear_session(request)
                return redirect("peserta_list")

            return render(request, "peserta/peserta_form.html", {
                "form": peserta,
                "pendidikan": pendidikan,
                "pekerjaan": pekerjaan,
                "keluarga": keluarga,
                "dokumen": dokumen,
                "current_step": step,
            })

        return redirect(f"{request.path}?step=1")


class PesertaProfileView(LoginRequiredMixin, View):

    def get(self, request):
        peserta = getattr(request.user, "peserta_profile", None)
        is_incomplete = peserta is None

        return render(request, "peserta/profil_peserta.html", {
            "peserta": peserta,
            "is_incomplete": is_incomplete,
        })


class PesertaUpdateView(LoginRequiredMixin, View):

    def get(self, request, pk):
        peserta = get_object_or_404(Peserta, pk=pk)

        form = forms.PesertaForm(instance=peserta)
        pendidikan = forms.RiwayatPendidikanFormSet(instance=peserta)
        pekerjaan = forms.RiwayatPekerjaanFormSet(instance=peserta)
        keluarga = forms.DataKeluargaFormSet(instance=peserta)
        dokumen = forms.DokumenPesertaFormSet(instance=peserta)

        return render(request, "peserta/peserta_form.html", {
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

        return render(request, "peserta/peserta_form.html", {
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

        return render(request, "peserta/peserta_detail.html", {
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
