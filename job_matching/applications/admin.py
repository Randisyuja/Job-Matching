from django.contrib import admin
from .models import Lamaran


@admin.register(Lamaran)
class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ['id', 'peserta', 'lowongan', 'status_lamaran', 'catatan', 'created_at', 'created_by', 'updated_at', 'updated_by']
    list_filter = ['lowongan', 'status_lamaran', 'created_by', 'updated_by']
    search_fields = ['peserta__nama_lengkap', 'lowongan__jenis_pekerjaan__nama_pekerjaan', 'catatan']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
