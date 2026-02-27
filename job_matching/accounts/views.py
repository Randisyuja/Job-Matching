from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model

from .models import Staff
from .forms import RegisterForm, LoginForm, UserUpdateForm, StaffForm
from . import services

User = get_user_model()


def homepage_peserta(request):
    return render(request, template_name='peserta/homepage.html')

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
            services.register_user(request, form)
            messages.success(request, "Register berhasil")
            return redirect("login")

        return render(request, "register.html", {"form": form})


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data["user"]
            services.login_user(request, user)
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
