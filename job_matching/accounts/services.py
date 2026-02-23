from django.db import transaction
from django.contrib.auth import get_user_model, login, logout
from .models import Staff

User = get_user_model()


def register_user(request, form):
    user = form.save(commit=False)
    user.set_password(form.cleaned_data["password"])
    user.save()
    return user


def login_user(request, user):
    login(request, user)


def logout_user(request):
    logout(request)


def update_user(form):
    user = form.save(commit=False)

    password = form.cleaned_data.get("password")
    if password:
        user.set_password(password)

    user.save()
    return user


def delete_user(user):
    user.is_active = False
    user.save()


@transaction.atomic
def create_staff(user_form, staff_form):

    user = user_form.save(commit=False)
    user.set_password(user_form.cleaned_data["password"])
    user.is_staff = True
    user.save()

    staff = staff_form.save(commit=False)
    staff.user = user
    staff.save()

    return staff


@transaction.atomic
def update_staff(user_form, staff_form):

    user = user_form.save(commit=False)

    if user_form.cleaned_data.get("password"):
        user.set_password(user_form.cleaned_data["password"])

    user.save()

    staff = staff_form.save()
    return staff
