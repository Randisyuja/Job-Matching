from django.contrib import admin
from .models import JenisPekerjaan, Lowongan, Persyaratan


@admin.register(JenisPekerjaan)
class JenisPekerjaanAdmin(admin.ModelAdmin):
    list_display = ('nama_pekerjaan', 'file_path')
    search_fields = ('nama_pekerjaan',)
    ordering = ('nama_pekerjaan',)


class PersyaratanInline(admin.TabularInline):
    model = Persyaratan
    extra = 1


@admin.register(Lowongan)
class LowonganAdmin(admin.ModelAdmin):
    list_display = (
        'nama_perusahaan',
        'jenis_pekerjaan',
        'kuota',
        'sisa_kuota',
        'batas_lamar',
        'is_active',
        'is_expired',
    )

    list_filter = (
        'is_active',
        'jenis_pekerjaan',
        'batas_lamar',
    )

    search_fields = (
        'nama_perusahaan',
        'lokasi_kerja',
    )

    ordering = ('-batas_lamar',)

    readonly_fields = (
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
        'is_expired',
        'sisa_kuota',
    )

    inlines = [PersyaratanInline]

    fieldsets = (
        ('Informasi Perusahaan', {
            'fields': (
                'nama_perusahaan',
                'jenis_pekerjaan',
                'lokasi_kerja',
            )
        }),
        ('Detail Lowongan', {
            'fields': (
                'kuota',
                'batas_bawah_usia',
                'batas_atas_usia',
                'batas_lamar',
                'deskripsi_pekerjaan',
                'is_active',
            )
        }),
        ('Monitoring', {
            'fields': (
                'sisa_kuota',
                'is_expired',
            )
        }),
        ('Informasi Sistem', {
            'fields': (
                'created_at',
                'created_by',
                'updated_at',
                'updated_by',
            ),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        from django.utils import timezone

        if not change:
            obj.created_by = request.user
            obj.created_at = timezone.now()

        obj.updated_by = request.user
        obj.updated_at = timezone.now()

        super().save_model(request, obj, form, change)


@admin.register(Persyaratan)
class PersyaratanAdmin(admin.ModelAdmin):
    list_display = ('name', 'lowongan')
    search_fields = ('name',)
    list_filter = ('lowongan',)
