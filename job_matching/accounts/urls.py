from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("register/peserta/", views.PesertaRegisterView.as_view(), name="register_peserta"),
    path("register/staff/", views.StaffRegisterView.as_view(), name="register_staff"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("users/<int:pk>/edit/", views.UserUpdateView.as_view(), name="user_update"),
    path("users/<int:pk>/hapus/", views.UserDeleteView.as_view(), name="user_delete"),
    path("staff/", views.StaffListView.as_view(), name="staff_list"),
    path("staff/tambah/", views.StaffCreateView.as_view(), name="staff_create"),
    path("staff/<int:pk>/edit/", views.StaffUpdateView.as_view(), name="staff_update"),
    path("staff/<int:pk>/hapus/", views.StaffDeleteView.as_view(), name="staff_delete"),
]
