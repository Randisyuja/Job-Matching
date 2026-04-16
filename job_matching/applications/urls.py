from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.StaffLamaranListView.as_view(),
        name="lamaran_list"
    ),
    path(
        "tambah/",
        views.StaffLamaranCreateView.as_view(),
        name="lamaran_create"
    ),
    path(
        "<int:pk>/",
        views.StaffLamaranDetailView.as_view(),
        name="lamaran_detail"
    ),
    path(
        "<int:pk>/status/",
        views.StaffLamaranUpdateStatusView.as_view(),
        name="lamaran_status"
    ),
    path(
        "<int:pk>/hapus/",
        views.StaffLamaranDeleteView.as_view(),
        name="lamaran_delete"
    ),
    path(
        "peserta/",
        views.LamaranListView.as_view(),
        name="lamaran_peserta"
    ),
    path(
        "peserta/<int:pk>/",
        views.LamaranPesertaDetailView.as_view(),
        name="lamaran_peserta_detail"
    ),
    path(
        "peserta/<int:pk>/hapus/",
        views.LamaranDeleteView.as_view(),
        name="lamaran_peserta_delete"
    ),
]
