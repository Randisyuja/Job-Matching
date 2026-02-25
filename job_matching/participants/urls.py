from django.urls import path
from . import views

urlpatterns = [
    path("", views.PesertaListView.as_view(), name="peserta_list"),
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
