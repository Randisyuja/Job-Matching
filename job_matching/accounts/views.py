from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model, login
from jobs.models import Lowongan

from .models import Staff
from .forms import RegisterForm, LoginForm, UserUpdateForm, StaffForm
from . import services

User = get_user_model()


def _is_peserta_without_profile(user):
    return (
        user.is_authenticated
        and not user.is_staff
        and not user.is_superuser
        and not hasattr(user, "peserta_profile")
    )


def homepage_peserta(request):
    if _is_peserta_without_profile(request.user):
        return redirect('peserta_create')

    latest_jobs = Lowongan.objects.select_related(
        "jenis_pekerjaan"
    ).filter(is_active=True).order_by("-created_at")[:6]

    articles = [
        {
            "title": "Cara menyiapkan profil yang lebih dilirik recruiter",
            "excerpt": (
                "Fokus pada ringkasan pengalaman, kelengkapan dokumen, dan "
                "konsistensi data agar proses seleksi lebih cepat."
            ),
            "category": "Tips Karier",
            "date": "09 Apr 2026",
            "read_time": "4 menit baca",
            "link": "/news",
        },
        {
            "title": "3 hal yang perlu dicek sebelum melamar lowongan terbaru",
            "excerpt": (
                "Pastikan batas usia, kuota aktif, dan tanggal penutupan "
                "masih sesuai sebelum mengirim lamaran."
            ),
            "category": "Persiapan",
            "date": "08 Apr 2026",
            "read_time": "3 menit baca",
            "link": "/news",
        },
        {
            "title": "Mengapa validasi profil penting untuk proses lamaran",
            "excerpt": (
                "Profil yang sudah tervalidasi membantu peserta melanjutkan "
                "ke tahapan lamaran tanpa hambatan tambahan."
            ),
            "category": "Panduan",
            "date": "07 Apr 2026",
            "read_time": "5 menit baca",
            "link": "/news",
        },
    ]

    return render(request, 'peserta/homepage.html', {
        "latest_jobs": latest_jobs,
        "articles": articles,
    })


def homepage_staff(request):
    return render(request, template_name='staff/homepage.html')


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = services.register_user(request, form)
            messages.success(request, "Register berhasil")
            login(request, user)
            return redirect("peserta_create")

        return render(request, "register.html", {"form": form})


class PesertaRegisterView(View):

    def get(self, request):
        return redirect("register")

    def post(self, request):
        return redirect("register")


class StaffRegisterView(View):

    def get(self, request):
        messages.warning(
            request,
            "Registrasi staff tidak tersedia di halaman ini.",
        )
        return redirect("register")

    def post(self, request):
        messages.warning(
            request,
            "Registrasi staff tidak tersedia di halaman ini.",
        )
        return redirect("register")


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data["user"]

            if user.is_staff or user.is_superuser:
                form.add_error(
                    None,
                    "Halaman login ini khusus peserta.",
                )
                return render(request, "login.html", {"form": form})

            services.login_user(request, user)

            if _is_peserta_without_profile(user):
                messages.warning(
                    request,
                    "Lengkapi profil peserta terlebih dahulu "
                    "sebelum melanjutkan.",
                )
                return redirect("peserta_create")

            return redirect("home")

        return render(request, "login.html", {"form": form})


class LogoutView(LoginRequiredMixin, View):

    def post(self, request):
        services.logout_user(request)
        return redirect("login")


class UserUpdateView(View):

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserUpdateForm(instance=user)
        return render(request, "user_form.html", {"form": form})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserUpdateForm(request.POST, instance=user)

        if form.is_valid():
            services.update_user(form)
            messages.success(request, "User berhasil diupdate")
            return redirect("user_list")

        return render(request, "user_form.html", {"form": form})


class UserDeleteView(View):

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        services.delete_user(user)
        messages.success(request, "User berhasil dinonaktifkan")
        return redirect("user_list")


class StaffListView(View):

    def get(self, request):
        data = Staff.objects.select_related("user").all()
        return render(request, "accounts/staff_list.html", {"data": data})


class StaffCreateView(View):

    def get(self, request):
        user_form = UserCreateForm()
        staff_form = StaffForm()

        return render(request, "accounts/staff_form.html", {
            "user_form": user_form,
            "staff_form": staff_form
        })

    def post(self, request):
        user_form = UserCreateForm(request.POST)
        staff_form = StaffForm(request.POST)

        if user_form.is_valid() and staff_form.is_valid():
            services.create_staff(user_form, staff_form)
            messages.success(request, "Staff berhasil dibuat")
            return redirect("staff_list")

        return render(request, "accounts/staff_form.html", {
            "user_form": user_form,
            "staff_form": staff_form
        })


class StaffUpdateView(View):

    def get(self, request, pk):
        staff = get_object_or_404(Staff, pk=pk)

        user_form = UserCreateForm(instance=staff.user)
        staff_form = StaffForm(instance=staff)

        return render(request, "accounts/staff_form.html", {
            "user_form": user_form,
            "staff_form": staff_form
        })

    def post(self, request, pk):
        staff = get_object_or_404(Staff, pk=pk)

        user_form = UserCreateForm(request.POST, instance=staff.user)
        staff_form = StaffForm(request.POST, instance=staff)

        if user_form.is_valid() and staff_form.is_valid():
            services.update_staff(user_form, staff_form)
            messages.success(request, "Staff berhasil diupdate")
            return redirect("staff_list")

        return render(request, "accounts/staff_form.html", {
            "user_form": user_form,
            "staff_form": staff_form
        })


class StaffDeleteView(View):

    def post(self, request, pk):
        staff = get_object_or_404(Staff, pk=pk)
        services.delete_staff(staff)
        messages.success(request, "Staff berhasil dinonaktifkan")
        return redirect("staff_list")
