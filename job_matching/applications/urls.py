from django.urls import path
from . import views

urlpatterns = [
    path("", views.LamaranListView.as_view(), name="lamaran_list"),
    path("tambah/", views.LamaranCreateView.as_view(), name="lamaran_create"),
    path("<int:pk>/", views.LamaranDetailView.as_view(), name="lamaran_detail"),
    path("<int:pk>/status/", views.LamaranUpdateStatusView.as_view(), name="lamaran_status"),
    path("<int:pk>/hapus/", views.LamaranDeleteView.as_view(), name="lamaran_delete"),
]