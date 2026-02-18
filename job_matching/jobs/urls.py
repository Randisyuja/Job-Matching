from django.urls import path, include
from . import views


urlpatterns = [
    path('jenis-pekerjaan/', views.JenisListView.as_view(), name="jenis_list"),
    path('jenis-pekerjaan/tambah/', views.JenisCreateView.as_view(), name="jenis_create"),
    path('jenis-pekerjaan/<int:pk>/', include([
        path('edit/', views.JenisUpdateView.as_view(), name="jenis_update"),
        path('hapus/', views.JenisDeleteView.as_view(), name="jenis_delete")
    ])),
    path('lowongan/', views.LowonganListView.as_view(), name="lowongan_list"),
    path('lowongan/tambah/', views.LowonganCreateView.as_view(), name="lowongan_create"),
    path('lowongan/<int:pk>/', include([
        path('', views.LowonganDetailView.as_view(), name="lowongan_detail"),
        path('edit/', views.LowonganUpdateView.as_view(), name="lowongan_update"),
        path('hapus/', views.LowonganDeleteView.as_view(), name="lowongan_delete")
    ])),
]
