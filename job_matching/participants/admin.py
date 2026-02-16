from django.contrib import admin
from .models import Peserta, RiwayatPendidikan, RiwayatPekerjaan, DataKeluarga, DokumenPeserta


class RiwayatPendidikanInline(admin.TabularInline):
    model = RiwayatPendidikan
    extra = 1


class RiwayatPekerjaanInline(admin.TabularInline):
    model = RiwayatPekerjaan
    extra = 1


class DataKeluargaInline(admin.TabularInline):
    model = DataKeluarga
    extra = 1


class DokumenPesertaInline(admin.TabularInline):
    model = DokumenPeserta
    extra = 1


@admin.register(Peserta)
class PesertaAdmin(admin.ModelAdmin):
    list_display = ['nama_lengkap', 'tanggal_lahir', 'jenis_kelamin', 'nomor_hp', 'minat_program', 'created_at']
    list_filter = ['jenis_kelamin', 'agama', 'status_pernikahan', 'minat_program', 'created_at']
    search_fields = ['nama_lengkap', 'nama_lengkap_katakana', 'nomor_hp']
    readonly_fields = ['user', 'created_at', 'updated_at', 'updated_by']

    fieldsets = (
        ('User Account', {
            'fields': ('user',)
        }),
        ('Data Pribadi', {
            'fields': ('nama_lengkap', 'nama_lengkap_katakana', 'tanggal_lahir', 'jenis_kelamin', 
                        'agama', 'nomor_hp', 'status_pernikahan')
        }),
        ('Alamat', {
            'fields': ('alamat_ktp', 'alamat_domisili')
        }),
        ('Program & Tujuan', {
            'fields': ('minat_program', 'pengalaman_ke_jepang', 'tujuan_ke_jepang')
        }),
        ('Finansial', {
            'fields': ('penghasilan_keluarga', 'target_penabungan')
        }),
        ('Data Fisik', {
            'fields': ('berat_badan', 'tinggi_badan', 'cek_mata_kanan', 'cek_mata_kiri', 
                      'golongan_darah', 'tangan_dominan')
        }),
        ('Kesehatan', {
            'fields': ('alergi_makanan', 'pantangan_makanan', 'riwayat_penyakit')
        }),
        ('Personality', {
            'fields': ('kelebihan', 'kekurangan', 'hobi')
        }),
        ('Audit', {
            'fields': ('created_at', 'updated_at', 'updated_by')
        }),
    )

    inlines = [RiwayatPendidikanInline, RiwayatPekerjaanInline, DataKeluargaInline, DokumenPesertaInline]


@admin.register(RiwayatPendidikan)
class RiwayatPendidikanAdmin(admin.ModelAdmin):
    list_display = ['peserta', 'jenjang', 'nama_institusi', 'tahun_lulus']
    list_filter = ['jenjang']
    search_fields = ['peserta__nama_lengkap', 'nama_institusi']


@admin.register(RiwayatPekerjaan)
class RiwayatPekerjaanAdmin(admin.ModelAdmin):
    list_display = ['peserta', 'nama_perusahaan', 'jabatan', 'tanggal_masuk', 'tanggal_keluar']
    list_filter = ['bidang_usaha']
    search_fields = ['peserta__nama_lengkap', 'nama_perusahaan', 'jabatan']


@admin.register(DataKeluarga)
class DataKeluargaAdmin(admin.ModelAdmin):
    list_display = ['peserta', 'hubungan_keluarga', 'usia', 'pekerjaan']
    list_filter = ['hubungan_keluarga']
    search_fields = ['peserta__nama_lengkap']


@admin.register(DokumenPeserta)
class DokumenPesertaAdmin(admin.ModelAdmin):
    list_display = ['peserta', 'jenis_dokumen', 'nama_dokumen', 'uploaded_at']
    list_filter = ['jenis_dokumen', 'uploaded_at']
    search_fields = ['peserta__nama_lengkap', 'nama_dokumen']