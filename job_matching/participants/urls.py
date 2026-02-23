from django.urls import path
from . import views

urlpatterns = [
    path("", views.PesertaListView.as_view(), name="peserta_list"),
    path("tambah/", views.PesertaCreateView.as_view(), name="peserta_create"),
    path("<int:pk>/", views.PesertaDetailView.as_view(), name="peserta_detail"),
    path("<int:pk>/validate-1/", views.PesertaValidateLevel1View.as_view(), name="validate_1"),
]
