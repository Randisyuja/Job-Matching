from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Count


from .models import JenisPekerjaan, Lowongan, Persyaratan
from .forms import (
    JenisPekerjaanForm,
    LowonganForm,
    PersyaratanForm,
    PersyaratanFormSet
)
from . import services as svc


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class StaffJenisListView(View):
    def get(self, request):
        data = JenisPekerjaan.objects.annotate(
            total_lowongan=Count("lowongan")
        )
        return render(request, "staff/jenis_list.html", {"data": data})


class StaffJenisCreateView(View):

    def get(self, request):
        form = JenisPekerjaanForm()
        return render(request, "staff/jenis_form.html", {"form": form})

    def post(self, request):
        form = JenisPekerjaanForm(request.POST, request.FILES)

        if form.is_valid():
            svc.create_jenis(form)
            messages.success(request, "Berhasil ditambahkan")
            return redirect("staff_jenis_list")

        return render(request, "staff/jenis_form.html", {"form": form})


class StaffJenisUpdateView(View):

    def get(self, request, pk):
        obj = get_object_or_404(JenisPekerjaan, pk=pk)
        form = JenisPekerjaanForm(instance=obj)
        return render(request, "jobs/jenis_form.html", {"form": form})

    def post(self, request, pk):
        obj = get_object_or_404(JenisPekerjaan, pk=pk)
        form = JenisPekerjaanForm(request.POST, request.FILES, instance=obj)

        if form.is_valid():
            svc.update_jenis(form)
            messages.success(request, "Berhasil diupdate")
            return redirect("staff_jenis_list")

        return render(request, "jobs/jenis_form.html", {"form": form})


class StaffJenisDeleteView(View):

    def post(self, request, pk):
        obj = get_object_or_404(JenisPekerjaan, pk=pk)

        try:
            svc.delete_jenis(obj)
            messages.success(request, "Berhasil dihapus")
        except ValidationError as e:
            messages.error(request, e.message)

        return redirect("staff_jenis_list")


class StaffLowonganListView(View):
    def get(self, request):
        is_active = request.GET.get("is_active")
        jenis_id = request.GET.get("jenis_id")
        selected_jenis = None

        if is_active == "True":
            data = svc.get_active_lowongan(True)
        elif is_active == "False":
            data = svc.get_active_lowongan(False)
        else:
            data = svc.get_all_lowongan()

        if jenis_id:
            data = data.filter(jenis_pekerjaan_id=jenis_id)
            selected_jenis = JenisPekerjaan.objects.filter(pk=jenis_id).first()

        paginator = Paginator(data, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj,
            "selected_jenis": selected_jenis,
        }

        return render(request, "staff/lowongan_list.html", context)


class StaffLowonganDetailView(View):
    def get(self, request, pk):
        lowongan, persyaratan = svc.get_lowongan_detail(pk)

        context = {
            "obj": lowongan,
            "persyaratan": persyaratan
        }

        return render(request, "staff/lowongan_detail.html", context)

    def post(self, request, pk):
        from applications.models import Lamaran
        from django.core.exceptions import (
            ValidationError as DjangoValidationError
        )

        lowongan, persyaratan = svc.get_lowongan_detail(pk)
        catatan = request.POST.get("catatan", "")

        try:
            # Check if user has peserta profile
            if not hasattr(request.user, 'peserta_profile'):
                messages.error(
                    request,
                    "Anda harus memiliki profil peserta untuk melamar."
                )
                return redirect("staff_lowongan_detail", pk=pk)

            peserta = request.user.peserta_profile

            if not peserta.can_apply_jobs:
                messages.error(
                    request,
                    "Profil Anda belum approved. Silakan tunggu validasi "
                    "sebelum melamar."
                )
                return redirect("staff_lowongan_detail", pk=pk)

            # Check if already applied
            if Lamaran.objects.filter(
                peserta=peserta,
                lowongan=lowongan
            ).exists():
                messages.warning(
                    request,
                    "Anda sudah pernah melamar lowongan ini."
                )
                return redirect("lowongan_detail", pk=pk)

            # Create lamaran
            lamaran = Lamaran(
                peserta=peserta,
                lowongan=lowongan,
                catatan=catatan,
                created_by=request.user,
                updated_by=request.user
            )
            lamaran.save()

            messages.success(
                request,
                "Lamaran berhasil dikirim! Anda dapat memantau status "
                "lamaran di halaman lamaran Anda."
            )
            return redirect("staff_lamaran_list")

        except (ValueError, DjangoValidationError) as e:
            messages.error(request, str(e))
            return redirect("staff_lowongan_detail", pk=pk)
        except Exception as e:
            messages.error(
                request,
                f"Terjadi kesalahan: {str(e)}"
            )
            return redirect("staff_lowongan_detail", pk=pk)


class StaffLowonganCreateView(View):

    def get(self, request):
        form = LowonganForm()
        formset = PersyaratanFormSet()

        context = {
            "form": form,
            "formset": formset
        }

        return render(request, "staff/lowongan_form.html", context)

    def post(self, request):
        form = LowonganForm(request.POST)
        formset = PersyaratanFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            svc.create_lowongan(form, formset, request.user)
            messages.success(request, "Lowongan berhasil dibuat")
            return redirect("staff_lowongan_list")

        context = {
            "form": form,
            "formset": formset
        }

        return render(request, "staff/lowongan_form.html", context)


class StaffLowonganUpdateView(View):

    def get(self, request, pk):
        obj = get_object_or_404(Lowongan, pk=pk)
        form = LowonganForm(instance=obj)
        return render(request, "staff/lowongan_form.html", {"form": form})

    def post(self, request, pk):
        obj = get_object_or_404(Lowongan, pk=pk)
        form = LowonganForm(request.POST, instance=obj)

        if form.is_valid():
            svc.update_lowongan(form, request.user)
            messages.success(request, "Lowongan berhasil diupdate")
            return redirect("staff_lowongan_list")

        return render(request, "staff/lowongan_form.html", {"form": form})


class StaffLowonganDeleteView(View):

    def post(self, request, pk):
        obj = get_object_or_404(Lowongan, pk=pk)
        svc.delete_lowongan(obj)
        messages.success(request, "Lowongan berhasil dihapus")
        return redirect("staff_lowongan_list")


class JenisListView(View):
    def get(self, request):
        data = JenisPekerjaan.objects.annotate(
            total_lowongan=Count("lowongan")
        )
        return render(request, "peserta/jenis_list.html", {"data": data})


class LowonganListView(View):
    def get(self, request):
        is_active = request.GET.get("is_active")
        jenis_id = request.GET.get("jenis_id")
        selected_jenis = None

        if is_active == "True":
            data = svc.get_active_lowongan(True)
        elif is_active == "False":
            data = svc.get_active_lowongan(False)
        else:
            data = svc.get_all_lowongan()

        if jenis_id:
            data = data.filter(jenis_pekerjaan_id=jenis_id)
            selected_jenis = JenisPekerjaan.objects.filter(pk=jenis_id).first()

        paginator = Paginator(data, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj,
            "selected_jenis": selected_jenis,
        }

        return render(request, "peserta/lowongan_list.html", context)


class LowonganDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        lowongan, persyaratan = svc.get_lowongan_detail(pk)

        context = {
            "obj": lowongan,
            "persyaratan": persyaratan
        }

        return render(request, "peserta/lowongan_detail.html", context)

    def post(self, request, pk):
        from applications.models import Lamaran
        from django.core.exceptions import (
            ValidationError as DjangoValidationError
        )

        lowongan, persyaratan = svc.get_lowongan_detail(pk)
        catatan = request.POST.get("catatan", "")

        try:
            # Check if user has peserta profile
            if not hasattr(request.user, 'peserta_profile'):
                messages.error(
                    request,
                    "Anda harus memiliki profil peserta untuk melamar."
                )
                return redirect("lowongan_detail", pk=pk)

            peserta = request.user.peserta_profile

            if not peserta.can_apply_jobs:
                messages.error(
                    request,
                    "Profil Anda belum approved. Silakan tunggu validasi "
                    "sebelum melamar."
                )
                return redirect("lowongan_detail", pk=pk)

            # Check if already applied
            if Lamaran.objects.filter(
                peserta=peserta,
                lowongan=lowongan
            ).exists():
                messages.warning(
                    request,
                    "Anda sudah pernah melamar lowongan ini."
                )
                return redirect("lowongan_detail", pk=pk)

            # Create lamaran
            lamaran = Lamaran(
                peserta=peserta,
                lowongan=lowongan,
                catatan=catatan,
                created_by=request.user,
                updated_by=request.user
            )
            lamaran.save()

            messages.success(
                request,
                "Lamaran berhasil dikirim! Anda dapat memantau status "
                "lamaran di halaman lamaran Anda."
            )
            return redirect("lamaran_peserta")

        except (ValueError, DjangoValidationError) as e:
            messages.error(request, str(e))
            return redirect("lowongan_detail", pk=pk)
        except Exception as e:
            messages.error(
                request,
                f"Terjadi kesalahan: {str(e)}"
            )
            return redirect("lowongan_detail", pk=pk)


class PersyaratanListView(View):
    def get(self, request):
        data = Persyaratan.objects.all()
        return render(request, "jobs/persyaratan_list.html", {"data": data})


class PersyaratanCreateView(LoginRequiredMixin, StaffRequiredMixin, View):

    def get(self, request):
        form = PersyaratanForm()
        return render(request, "jobs/persyaratan_form.html", {"form": form})

    def post(self, request):
        form = PersyaratanForm(request.POST)

        if form.is_valid():
            try:
                svc.create_persyaratan(form)
                messages.success(request, "Berhasil ditambahkan")
                return redirect("persyaratan_list")
            except ValidationError as e:
                form.add_error(None, e.message)

        return render(request, "jobs/persyaratan_form.html", {"form": form})


class PersyaratanUpdateView(LoginRequiredMixin, StaffRequiredMixin, View):

    def get(self, request, pk):
        obj = get_object_or_404(Persyaratan, pk=pk)
        form = PersyaratanForm(instance=obj)
        return render(request, "jobs/persyaratan_form.html", {"form": form})

    def post(self, request, pk):
        obj = get_object_or_404(Persyaratan, pk=pk)
        form = PersyaratanForm(request.POST, instance=obj)

        if form.is_valid():
            try:
                svc.update_persyaratan(form)
                messages.success(request, "Berhasil diupdate")
                return redirect("persyaratan_list")
            except ValidationError as e:
                form.add_error(None, e.message)

        return render(request, "jobs/persyaratan_form.html", {"form": form})


class PersyaratanDeleteView(LoginRequiredMixin, StaffRequiredMixin, View):

    def post(self, request, pk):
        obj = get_object_or_404(Persyaratan, pk=pk)
        svc.delete_persyaratan(obj)
        messages.success(request, "Berhasil dihapus")
        return redirect("persyaratan_list")
