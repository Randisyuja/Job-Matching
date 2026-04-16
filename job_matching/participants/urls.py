from django.urls import path
from . import views

urlpatterns = [
    path("", views.StaffPesertaListView.as_view(), name="staff_peserta_list"),
    path(
        "validasi-1/",
        views.StaffPesertaStatusListView.as_view(
            status_value=views.StatusValidasi.DIAJUKAN,
            template_name="staff/validasi_1.html",
            page_title="Peserta Validasi 1",
        ),
        name="staff_validasi_1",
    ),
    path(
        "validasi-2/",
        views.StaffPesertaStatusListView.as_view(
            status_value=views.StatusValidasi.VALIDATED_1,
            template_name="staff/validasi_2.html",
            page_title="Peserta Validasi 2",
        ),
        name="staff_validasi_2",
    ),
    path(
        "disetujui/",
        views.StaffPesertaStatusListView.as_view(
            status_value=views.StatusValidasi.APPROVED,
            template_name="staff/peserta_disetujui.html",
            page_title="Peserta Disetujui",
        ),
        name="staff_peserta_disetujui",
    ),
    path(
        "ditolak/",
        views.StaffPesertaStatusListView.as_view(
            status_value=views.StatusValidasi.REJECTED,
            template_name="staff/peserta_ditolak.html",
            page_title="Peserta Ditolak",
        ),
        name="staff_peserta_ditolak",
    ),
    path(
        "tambah/",
        views.PesertaCreateView.as_view(),
        name="peserta_create",
    ),
    path(
        "<int:pk>/",
        views.PesertaProfileView.as_view(),
        name="peserta_profile",
    ),
    path(
        "<int:pk>/update/",
        views.PesertaUpdateView.as_view(),
        name="peserta_update",
    ),
    path(
        "<int:pk>/validate-1/",
        views.PesertaValidateLevel1View.as_view(),
        name="validate_1",
    ),
    path(
        "<int:pk>/detail/",
        views.PesertaDetailView.as_view(),
        name="peserta_detail",
    ),
]
