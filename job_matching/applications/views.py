from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Lamaran
from .forms import LamaranCreateForm, LamaranUpdateStatusForm
from .choices import StatusLamaran
from . import services


def _is_peserta_without_profile(user):
    return (
        user.is_authenticated
        and not user.is_staff
        and not user.is_superuser
        and not hasattr(user, "peserta_profile")
    )


class StaffLamaranListView(LoginRequiredMixin, View):

    def get(self, request):
        queryset = Lamaran.objects.select_related(
            "peserta",
            "lowongan"
        )

        status = request.GET.get("status")
        if status:
            queryset = queryset.filter(status_lamaran=status)

        paginator = Paginator(queryset.order_by("-created_at"), 10)
        page = request.GET.get("page")
        data = paginator.get_page(page)

        # Gunakan template berbeda untuk peserta vs staff
        template = "staff/list.html"

        return render(request, template, {
            "data": data,
            "status_choices": StatusLamaran.choices,
            "selected_status": status,
        })


class StaffLamaranCreateView(LoginRequiredMixin, View):

    def get(self, request):
        if _is_peserta_without_profile(request.user):
            messages.warning(
                request,
                "Lengkapi profil peserta terlebih dahulu sebelum melamar.",
            )
            return redirect("peserta_create")

        form = LamaranCreateForm()

        # Pre-fill lowongan field if provided in query string
        lowongan_id = request.GET.get("lowongan")
        if lowongan_id:
            form.initial["lowongan"] = lowongan_id

        return render(request, "applications/form.html", {"form": form})

    def post(self, request):
        if _is_peserta_without_profile(request.user):
            messages.warning(
                request,
                "Lengkapi profil peserta terlebih dahulu sebelum melamar.",
            )
            return redirect("peserta_create")

        form = LamaranCreateForm(request.POST)

        if form.is_valid():
            try:
                services.create_lamaran(request.user, form)
                messages.success(request, "Lamaran berhasil dibuat")
                return redirect("lamaran_list")
            except Exception as e:
                form.add_error(None, str(e))

        return render(request, "applications/form.html", {"form": form})


class StaffLamaranDetailView(LoginRequiredMixin, View):

    def get(self, request, pk):
        lamaran = get_object_or_404(Lamaran, pk=pk)
        return render(request, "staff/detail.html", {
            "lamaran": lamaran
        })


class StaffLamaranUpdateStatusView(LoginRequiredMixin, View):

    def get(self, request, pk):
        lamaran = get_object_or_404(Lamaran, pk=pk)
        form = LamaranUpdateStatusForm(instance=lamaran)
        return render(request, "staff/status_form.html", {
            "form": form,
            "lamaran": lamaran,
        })

    def post(self, request, pk):
        lamaran = get_object_or_404(Lamaran, pk=pk)
        form = LamaranUpdateStatusForm(request.POST, instance=lamaran)

        if form.is_valid():
            services.update_status(request.user, lamaran, form)
            messages.success(request, "Status berhasil diupdate")
            return redirect("lamaran_detail", pk=pk)

        return render(request, "staff/status_form.html", {
            "form": form,
            "lamaran": lamaran,
        })


class StaffLamaranDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        lamaran = get_object_or_404(Lamaran, pk=pk)
        services.delete_lamaran(lamaran)
        messages.success(request, "Lamaran berhasil dihapus")
        return redirect("lamaran_list")


class LamaranListView(LoginRequiredMixin, View):

    def get(self, request):
        if _is_peserta_without_profile(request.user):
            messages.warning(
                request,
                "Lengkapi profil peserta terlebih dahulu untuk "
                "melihat lamaran.",
            )
            return redirect("peserta_create")

        queryset = Lamaran.objects.select_related(
            "peserta",
            "lowongan"
        )

        # Jika peserta → hanya lihat lamaran sendiri
        if hasattr(request.user, "peserta_profile"):
            queryset = queryset.filter(
                peserta=request.user.peserta_profile
            )

        status = request.GET.get("status")
        if status:
            queryset = queryset.filter(status_lamaran=status)

        paginator = Paginator(queryset.order_by("-created_at"), 10)
        page = request.GET.get("page")
        data = paginator.get_page(page)

        template = "peserta/lamaran_peserta.html"

        return render(request, template, {
            "data": data,
            "status_choices": StatusLamaran.choices,
            "selected_status": status,
        })


class LamaranPesertaDetailView(LoginRequiredMixin, View):

    def get(self, request, pk):
        if _is_peserta_without_profile(request.user):
            messages.warning(
                request,
                "Lengkapi profil peserta terlebih dahulu untuk "
                "melihat detail lamaran.",
            )
            return redirect("peserta_create")

        lamaran = get_object_or_404(Lamaran, pk=pk)

        if lamaran.peserta != request.user.peserta_profile:
            messages.error(
                request,
                "Anda tidak memiliki akses ke lamaran ini."
            )
            return redirect("lamaran_peserta")

        return render(request, "peserta/lamaran_detail.html", {
            "lamaran": lamaran,
        })


class LamaranDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        lamaran = get_object_or_404(Lamaran, pk=pk)
        services.delete_lamaran(lamaran)
        messages.success(request, "Lamaran berhasil dihapus")
        return redirect("lamaran_peserta")
