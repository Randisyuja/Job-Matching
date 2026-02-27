from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Lamaran
from .forms import LamaranCreateForm, LamaranUpdateStatusForm
from . import services


class LamaranListView(LoginRequiredMixin, View):

    def get(self, request):
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

        # Gunakan template berbeda untuk peserta vs staff
        template = "peserta/lamaran_peserta.html"
        if request.user.is_staff:
            template = "applications/list.html"

        return render(request, template, {
            "data": data
        })


class LamaranCreateView(LoginRequiredMixin, View):

    def get(self, request):
        form = LamaranCreateForm()

        # Pre-fill lowongan field if provided in query string
        lowongan_id = request.GET.get("lowongan")
        if lowongan_id:
            form.initial["lowongan"] = lowongan_id

        return render(request, "applications/form.html", {"form": form})

    def post(self, request):
        form = LamaranCreateForm(request.POST)

        if form.is_valid():
            try:
                services.create_lamaran(request.user, form)
                messages.success(request, "Lamaran berhasil dibuat")
                return redirect("lamaran_list")
            except Exception as e:
                form.add_error(None, str(e))

        return render(request, "applications/form.html", {"form": form})


class LamaranDetailView(LoginRequiredMixin, View):

    def get(self, request, pk):
        lamaran = get_object_or_404(Lamaran, pk=pk)
        return render(request, "peserta/detail.html", {
            "lamaran": lamaran
        })


class LamaranUpdateStatusView(LoginRequiredMixin, View):

    def get(self, request, pk):
        lamaran = get_object_or_404(Lamaran, pk=pk)
        form = LamaranUpdateStatusForm(instance=lamaran)
        return render(request, "applications/status_form.html", {
            "form": form
        })

    def post(self, request, pk):
        lamaran = get_object_or_404(Lamaran, pk=pk)
        form = LamaranUpdateStatusForm(request.POST, instance=lamaran)

        if form.is_valid():
            services.update_status(request.user, lamaran, form)
            messages.success(request, "Status berhasil diupdate")
            return redirect("lamaran_detail", pk=pk)

        return render(request, "applications/status_form.html", {
            "form": form
        })


class LamaranDeleteView(LoginRequiredMixin, View):

    def post(self, request, pk):
        lamaran = get_object_or_404(Lamaran, pk=pk)
        services.delete_lamaran(lamaran)
        messages.success(request, "Lamaran berhasil dihapus")
        return redirect("lamaran_list")
