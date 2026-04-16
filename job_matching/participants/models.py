from django.db import models
from django.forms import ValidationError
from accounts.models import User
from .choices import JenisKelamin, Agama, StatusPernikahan, GolonganDarah, TanganDominan, Jenjang, HubunganKeluarga, DokumenPesertaChoices, StatusValidasi
from datetime import date


class Peserta(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='peserta_profile'
    )

    # DATA PRIBADI
    nama_lengkap = models.CharField("Nama Lengkap", max_length=50, blank=True)
    nama_lengkap_katakana = models.CharField("Nama Lengkap (Katakana)", max_length=50, blank=True)

    tanggal_lahir = models.DateField("Tanggal Lahir", blank=True, null=True)

    jenis_kelamin = models.CharField(
        "Jenis Kelamin",
        max_length=50,
        choices=JenisKelamin.choices,
        blank=True
    )

    agama = models.CharField(
        "Agama",
        max_length=50,
        choices=Agama.choices,
        blank=True
    )

    nomor_hp = models.CharField("Nomor HP", max_length=50, blank=True)

    status_pernikahan = models.CharField(
        "Status Pernikahan",
        max_length=50,
        choices=StatusPernikahan.choices,
        blank=True
    )

    # ALAMAT
    alamat_ktp = models.TextField("Alamat KTP", blank=True)
    alamat_domisili = models.TextField("Alamat Domisili", blank=True)

    # PROGRAM & MOTIVASI
    minat_program = models.CharField("Minat Program", max_length=50, blank=True)
    pengalaman_ke_jepang = models.TextField("Pengalaman ke Jepang", blank=True)
    tujuan_ke_jepang = models.TextField("Tujuan ke Jepang", blank=True)

    # EKONOMI
    penghasilan_keluarga = models.IntegerField("Penghasilan Keluarga", blank=True, null=True)
    target_penabungan = models.IntegerField("Target Penabungan", blank=True, null=True)

    # FISIK & KESEHATAN
    berat_badan = models.IntegerField("Berat Badan (kg)", blank=True, null=True)
    tinggi_badan = models.IntegerField("Tinggi Badan (cm)", blank=True, null=True)

    cek_mata_kanan = models.FloatField("Cek Mata Kanan", blank=True, null=True)
    cek_mata_kiri = models.FloatField("Cek Mata Kiri", blank=True, null=True)

    golongan_darah = models.CharField(
        "Golongan Darah",
        max_length=50,
        choices=GolonganDarah.choices,
        blank=True
    )

    tangan_dominan = models.CharField(
        "Tangan Dominan",
        max_length=50,
        choices=TanganDominan.choices,
        blank=True
    )

    alergi_makanan = models.TextField("Alergi Makanan", blank=True)
    pantangan_makanan = models.TextField("Pantangan Makanan", blank=True)
    riwayat_penyakit = models.TextField("Riwayat Penyakit", blank=True)

    # PERSONAL
    kelebihan = models.TextField("Kelebihan", blank=True)
    kekurangan = models.TextField("Kekurangan", blank=True)
    hobi = models.TextField("Hobi", blank=True)

    # STATUS & VALIDASI
    status_validasi = models.CharField(
        "Status Validasi",
        choices=StatusValidasi.choices,
        default=StatusValidasi.DIAJUKAN,
        db_index=True
    )

    # VALIDASI LEVEL 1
    validasi_1_pada = models.DateTimeField("Tanggal Validasi 1", null=True, blank=True)
    validasi_1_oleh = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='validated_peserta_level_1'
    )
    validasi_1_notes = models.TextField("Catatan Validasi 1", blank=True)

    # VALIDASI LEVEL 2
    validasi_2_pada = models.DateTimeField("Tanggal Validasi 2", null=True, blank=True)
    validasi_2_oleh = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='validated_peserta_level_2'
    )
    validasi_2_notes = models.TextField("Catatan Validasi 2", blank=True)

    # FINAL
    tervalidasi_pada = models.DateTimeField("Tanggal Approved", null=True, blank=True)
    alasan_penolakan = models.TextField("Alasan Ditolak", blank=True)

    # META
    created_at = models.DateTimeField("Tanggal Dibuat", auto_now_add=True)
    updated_at = models.DateTimeField("Tanggal Diupdate", auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_peserta_profiles'
    )

    def is_complete(self):
        required_fields = [
            self.nama_lengkap,
            self.tanggal_lahir,
            self.nomor_hp,
            self.alamat_ktp,
            self.minat_program,
        ]
        return all(required_fields)

    def __str__(self):
        return self.nama_lengkap or self.user.username

    class Meta:
        db_table = 'peserta'
        verbose_name = 'Peserta'
        verbose_name_plural = 'Peserta'

    def __str__(self):
        return self.nama_lengkap

    @property
    def usia(self):
        today = date.today()
        age = today.year - self.tanggal_lahir.year
        if (today.month, today.day) < (self.tanggal_lahir.month, self.tanggal_lahir.day):
            age -= 1
        return age

    def validate_level_1(self, validator_user, notes=''):
        """Admin validates - Level 1"""
        if self.status_validasi != StatusValidasi.DIAJUKAN:
            raise ValidationError('Can only validate submitted profiles')

        from django.utils import timezone
        self.status_validasi = StatusValidasi.VALIDATED_1
        self.validasi_1_pada = timezone.now()
        self.validasi_1_oleh = validator_user
        self.validasi_1_notes = notes
        self.save()

    def validate_level_2(self, validator_user, notes=''):
        """Koordinator validates - Level 2"""
        if self.status_validasi != StatusValidasi.VALIDATED_1:
            raise ValidationError('Can only validate level-1 approved profiles')

        from django.utils import timezone
        self.status_validasi = StatusValidasi.APPROVED
        self.validasi_2_pada = timezone.now()
        self.validasi_2_oleh = validator_user
        self.validasi_2_notes = notes
        self.save()

    def reject(self, validator_user, reason):
        """Koordinator rejects - Level 2"""
        if self.status_validasi != StatusValidasi.VALIDATED_1:
            raise ValidationError('Can only reject level-1 approved profiles')

        from django.utils import timezone
        self.status_validasi = StatusValidasi.REJECTED
        self.validasi_2_pada = timezone.now()
        self.validasi_2_oleh = validator_user
        self.alasan_penolakan = reason
        self.save()

    def final_approve(self):
        """Final approval - ready to apply for jobs"""
        if self.status_validasi != StatusValidasi.VALIDATED_1:
            raise ValidationError('Must pass both validations first')

        from django.utils import timezone
        self.status_validasi = StatusValidasi.APPROVED
        self.tervalidasi_pada = timezone.now()
        self.save()

    def suspend(self, reason):
        """Suspend peserta"""
        self.status_validasi = StatusValidasi.SUSPENDED
        self.alasan_penolakan = reason
        self.save()

    @property
    def can_apply_jobs(self):
        """Check if peserta can apply for jobs"""
        return self.status_validasi == StatusValidasi.APPROVED

    @property
    def validation_progress(self):
        """Get validation progress percentage"""
        status_weight = {
            StatusValidasi.DIAJUKAN: 0,
            StatusValidasi.VALIDATED_1: 50,
            StatusValidasi.APPROVED: 100,
            StatusValidasi.REJECTED: 0,
            StatusValidasi.SUSPENDED: 0,
        }
        return status_weight.get(self.status_validasi, 0)


class RiwayatPendidikan(models.Model):
    peserta = models.ForeignKey(
        Peserta,
        on_delete=models.CASCADE,
        related_name='riwayat_pendidikan'
    )
    jenjang = models.CharField(
        "Jenjang",
        max_length=50,
        choices=Jenjang.choices,
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
        unique_together = ('peserta', 'jenjang', 'nama_institusi')

    def __str__(self):
        return f"{self.peserta.nama_lengkap} - {self.jenjang} - {self.nama_institusi}"


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

    def __str__(self):
        return f"{self.peserta.nama_lengkap} - {self.jabatan} di {self.nama_perusahaan}"


class DataKeluarga(models.Model):
    peserta = models.ForeignKey(
        Peserta,
        on_delete=models.CASCADE,
        related_name='data_keluarga'
    )
    hubungan_keluarga = models.CharField(
        "Hubungan Keluarga",
        max_length=50,
        choices=HubunganKeluarga.choices,
        blank=False
    )
    tanggal_lahir = models.DateField("Tanggal Lahir", blank=False)
    pekerjaan = models.CharField("Pekerjaan", max_length=50, blank=False)

    class Meta:
        db_table = 'data_keluarga'
        verbose_name = "Data Keluarga"
        verbose_name_plural = 'Data Keluarga'

    @property
    def usia(self):
        today = date.today()
        age = today.year - self.tanggal_lahir.year
        if (today.month, today.day) < (self.tanggal_lahir.month, self.tanggal_lahir.day):
            age -= 1
        return age

    def __str__(self):
        return f"{self.peserta.nama_lengkap} - {self.hubungan_keluarga}"


class DokumenPeserta(models.Model):
    peserta = models.ForeignKey(
        Peserta,
        on_delete=models.CASCADE,
        related_name='dokumen'
    )
    jenis_dokumen = models.CharField(
        "Jenis Dokumen",
        max_length=50,
        choices=DokumenPesertaChoices.choices,
        blank=False
    )
    nama_dokumen = models.CharField("Nama Dokumen", max_length=50, blank=False)
    file_path = models.FileField("File", upload_to="peserta/dokumen/%Y/%m/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dokumen_peserta'
        verbose_name = "Dokumen Peserta"
        verbose_name_plural = 'Dokumen Peserta'

    def __str__(self):
        return f"{self.peserta.nama_lengkap} - {self.jenis_dokumen}"
