from django import forms
from django.contrib.auth import get_user_model, authenticate
from .models import Staff

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        user = authenticate(username=email, password=password)

        if not user:
            raise forms.ValidationError("Email atau password salah")

        if not user.is_active:
            raise forms.ValidationError("User tidak aktif")

        cleaned_data["user"] = user
        return cleaned_data


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password != confirm:
            raise forms.ValidationError("Password tidak sama")

        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = User
        fields = ["email", "password", "is_active"]


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            "nama",
            "jabatan",
            "unit_kerja",
            "nomor_hp",
            "is_active"
        ]
