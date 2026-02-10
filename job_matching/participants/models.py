from django.db import models
from accounts.models import User
from .choices import JenisKelamin, Agama, StatusPernikahan, GolonganDarah, TanganDominan, Jenjang, HubunganKeluarga, DokumenPeserta, StatusValidasi


class Peserta(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='peserta_profile'
    )
    nama_lengkap = models.CharField(
        "Nama Lengkap",
        max_length=50,
        blank=False
    )
    nama_lengkap_katakana = models.CharField(
        "Nama Lengkap (Katakana)",
        max_length=50,
        blank=False
    )
    tanggal_lahir = models.DateField(
        "Tanggal Lahir",
        blank=False
    )
    jenis_kelamin = models.CharField(
        "Jenis Kelamin",
        max_length=50,
        choices=JenisKelamin
    )
    agama = models.CharField(
        "Agama",
        max_length=50,
        choices=Agama
    )
    nomor_hp = models.CharField(
        "Nomor HP",
        max_length=50
    )
    status_pernikahan = models.CharField(
        "Status Pernikahan",
        max_length=50,
        choices=StatusPernikahan
    )

    alamat_ktp = models.TextField(
        "Alamat KTP",
        blank=False
    )
    alamat_domisili = models.TextField(
        "Alamat Domisili",
        blank=False
    )
    minat_program = models.CharField(
        "Minat Program",
        max_length=50,
        blank=False
    )
    pengalaman_ke_jepang = models.TextField(
        "Pengalaman ke Jepang",
        blank=False
    )
    tujuan_ke_jepang = models.TextField(
        "Tujuan ke Jepang",
        blank=False
    )

    penghasilan_keluarga = models.IntegerField(
        "Penghasilan Keluarga",
        blank=False
    )
    target_penabungan = models.IntegerField(
        "Target Penabungan",
        blank=False
    )
    berat_badan = models.IntegerField(
        'Berat Badan (kg)',
        blank=False
    )
    tinggi_badan = models.IntegerField(
        'Tinggi Badan (cm)',
        blank=False
    )
    cek_mata_kanan = models.FloatField(
        'Cek Mata Kanan',
        blank=False
    )
    cek_mata_kiri = models.FloatField(
        'Cek Mata Kiri',
        blank=False
    )
    golongan_darah = models.CharField(
        'Golongan Darah',
        max_length=50,
        choices=GolonganDarah,
        blank=False
    )
    tangan_dominan = models.CharField(
        'Tangan Dominan',
        max_length=50,
        choices=TanganDominan,
        blank=False
    )
    alergi_makanan = models.TextField(
        'Alergi Makanan',
        blank=False
    )
    pantangan_makanan = models.TextField(
        'Pantangan Makanan',
        blank=False
    )
    riwayat_penyakit = models.TextField(
        'Riwayat Penyakit',
        blank=False
    )
    kelebihan = models.TextField(
        'Kelebihan',
        blank=False
    )
    kekurangan = models.TextField(
        'Kekurangan',
        blank=False
    )
    hobi = models.TextField(
        'Hobi',
        blank=False
    )
    status_validasi = models.CharField(
        "Status Validasi",
        choices=StatusValidasi,
        default=StatusValidasi.DIAJUKAN
    )

    validasi_1_pada = models.DateTimeField('Tanggal Validasi 1', null=True, blank=True)
    validasi_1_oleh = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='validated_peserta_level_1',
        verbose_name='Divalidasi 1 Oleh'
    )
    validasi_1_notes = models.TextField('Catatan Validasi 1', blank=True)

    validasi_2_pada = models.DateTimeField('Tanggal Validasi 2', null=True, blank=True)
    validasi_2_oleh = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='validated_peserta_level_2',
        verbose_name='Divalidasi 2 Oleh'
    )
    validasi_2_notes = models.TextField('Catatan Validasi 2', blank=True)

    tervalidasi_pada = models.DateTimeField('Tanggal Approved', null=True, blank=True)

    alasan_penolakan = models.TextField('Alasan Ditolak', blank=True)

    created_at = models.DateTimeField(
        'Tanggal Dibuat',
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        'Tanggal Diupdate',
        auto_now=True
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='updated_peserta_profiles',
        verbose_name='Diupdate Oleh'
    )

    class Meta:
        db_table = 'peserta'
        verbose_name = 'Peserta'
        verbose_name_plural = 'Peserta'

    def __str__(self):
        return self.nama_lengkap

    @property
    def usia(self):
        from datetime import date
        today = date.today()
        return today.year - self.tanggal_lahir.year


class RiwayatPendidikan(models.Model):
    peserta = models.ForeignKey(
        Peserta,
        on_delete=models.CASCADE,
        related_name='riwayat_pendidikan'
    )
    jenjang = models.CharField(
        "Jenjang",
        max_length=50,
        choices=Jenjang,
        blank=False
    )
    nama_institusi = models.CharField(
        "Nama Institusi",
        max_length=100,
        blank=False
    )
    tahun_masuk = models.DateField("Tahun Masuk", blank=False)
    tahun_lulus = models.DateField("Tahun Keluar", blank=False)

    class Meta:
        db_table = 'riwayat_pendidikan'
        ordering = ['-tahun_lulus']
        verbose_name = "Riwayat Pendidikan"
        verbose_name_plural = 'Riwayat Pendidikan'


class RiwayatPekerjaan(models.Model):
    peserta = models.ForeignKey(
        Peserta,
        on_delete=models.CASCADE,
        related_name='riwayat_pekerjaan'
    )
    nama_perusahaan = models.CharField(
        "Nama Perusahaan",
        max_length=100,
        blank=False
    )
    bidang_usaha = models.CharField(
        "Bidang Usaha",
        max_length=100,
        blank=False
    )
    jabatan = models.CharField("Jabatan", max_length=50, blank=False)
    gaji = models.IntegerField("Gaji", blank=False)
    tanggal_masuk = models.DateField("Tanggal Masuk", blank=False)
    tanggal_keluar = models.DateField("Tanggal Keluar", blank=False)

    class Meta:
        db_table = 'riwayat_pekerjaan'
        ordering = ['-tanggal_masuk']
        verbose_name_plural = 'Riwayat Pekerjaan'


class DataKeluarga(models.Model):
    peserta = models.ForeignKey(
        Peserta,
        on_delete=models.CASCADE,
        related_name='data_keluarga'
    )
    hubungan_keluarga = models.CharField(
        "Hubungan Keluarga",
        max_length=50,
        choices=HubunganKeluarga,
        blank=False
    )
    tanggal_lahir = models.DateField("Tanggal Lahir", blank=False)
    pekerjaan = models.CharField("Pekerjaan", max_length=50, blank=False)

    class Meta:
        db_table = 'data_keluarga'
        verbose_name = "Data Keluarga"
        verbose_name_plural = 'Data Keluarga'


class DokumenPeserta(models.Model):
    peserta = models.ForeignKey(
        Peserta,
        on_delete=models.CASCADE,
        related_name='dokumen'
    )
    jenis_dokumen = models.CharField(
        "Jenis Dokumen",
        max_length=50,
        choices=DokumenPeserta,
        blank=False
    )
    nama_dokumen = models.CharField("Nama Dokumen", max_length=50, blank=False)
    file_path = models.FileField("File", upload_to="peserta/dokumen/%Y/%m/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dokumen_peserta'
        verbose_name = "Dokumen Peserta"
        verbose_name_plural = 'Dokumen Peserta'
