from django.db import models


class StatusValidasi(models.TextChoices):
    DIAJUKAN = "Diajukan", "Menunggu Validasi"
    VALIDATED_1 = "Validasi 1", "Validasi 1"
    APPROVED = "Approved", "Approved"
    REJECTED = "Rejected", "Rejected"
    SUSPENDED = "Suspended", "Suspended"


class JenisKelamin(models.TextChoices):
    LAKI = "Laki-laki", "Laki-laki"
    PEREMPUAN = "Perempuan", "Perempuan"


class Agama(models.TextChoices):
    ISLAM = "Islam", "Islam"
    KRISTEN = "Kristen", "Kristen"
    KATOLIK = "Katolik", "Katolik"
    HINDU = "Hindu", "Hindu"
    BUDDHA = "Buddha", "Buddha"
    KONGHUCU = "Konghucu", "Konghucu"


class StatusPernikahan(models.TextChoices):
    LAJANG = "Lajang", "Lajang"
    MENIKAH = "Menikah", "Menikah"
    CERAIMATI = "Cerai Mati", "Cerai Mati"
    CERAIHIDUP = "Cerai Hidup", "Cerai Hidup"


class GolonganDarah(models.TextChoices):
    GOL_A = "A", "A"
    GOL_B = "B", "B"
    GOL_AB = "AB", "AB"
    GOL_O = "O", "O"


class TanganDominan(models.TextChoices):
    KANAN = "Kanan", "Kanan"
    KIRI = "Kiri", "Kiri"


class Jenjang(models.TextChoices):
    SD = "sd", "Sekolah Dasar"
    SMP = "smp", "Sekolah Menengah Pertama"
    SMA = "sma", "Sekolah Menengah Atas"
    SMK = "smk", "Sekolah Menengah Kejuruan"
    D3 = "d3", "Diploma 3"
    S1 = "s1", "Sarjana"
    S2 = "s2", "Magister"
    S3 = "s3", "Doktor"


class HubunganKeluarga(models.TextChoices):
    AYAH = "Ayah", "Ayah"
    IBU = "Ibu", "Ibu"
    SUAMI = "Suami", "Suami"
    ISTRI = "Istri", "Istri"
    ANAK = "Anak", "Anak"
    KAKAK = "Kakak", "Kakak"
    ADIK = "Adik", "Adik"
    SAUDARA = "Saudara", "Saudara"


class DokumenPesertaChoices(models.TextChoices):
    JLPT = "JLPT", "JLPT"
    JFT = "JFT", "JFT"
    SSW = "SSW", "SSW"
    JITCO = "JITCO", "JITCO"
    FOTO = "FOTO PROFIL", "FOTO PROFIL"
