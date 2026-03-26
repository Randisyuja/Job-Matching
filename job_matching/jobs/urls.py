from django.urls import path, include
from . import views


urlpatterns = [
    path('jenis-pekerjaan/', views.JenisListView.as_view(), name="jenis_list"),
    path('lowongan/', views.LowonganListView.as_view(), name="lowongan_list"),
    path('lowongan/<int:pk>/', views.LowonganDetailView.as_view(), name="lowongan_detail"),
    path("staff/jenis-pekerjaan/", views.StaffJenisListView.as_view(), name="staff_jenis_list"),
    path('staff/jenis-pekerjaan/tambah/', views.StaffJenisCreateView.as_view(), name="staff_jenis_create"),
    path('staff/jenis-pekerjaan/<int:pk>/', include([
        path('edit/', views.StaffJenisUpdateView.as_view(), name="staff_jenis_update"),
        path('hapus/', views.StaffJenisDeleteView.as_view(), name="staff_jenis_delete")
    ])),
    path('staff/lowongan/', views.StaffLowonganListView.as_view(), name="staff_lowongan_list"),
    path('staff/lowongan/tambah/', views.StaffLowonganCreateView.as_view(), name="staff_lowongan_create"),
    path('staff/lowongan/<int:pk>/', include([
        path('', views.StaffLowonganDetailView.as_view(), name="staff_lowongan_detail"),
        path('edit/', views.StaffLowonganUpdateView.as_view(), name="staff_lowongan_update"),
        path('hapus/', views.StaffLowonganDeleteView.as_view(), name="staff_lowongan_delete")
    ])),
]
