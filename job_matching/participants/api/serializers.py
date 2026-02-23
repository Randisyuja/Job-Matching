from rest_framework import serializers
from .models import (
    Peserta,
    RiwayatPendidikan,
    RiwayatPekerjaan,
    DataKeluarga,
    DokumenPeserta
)


class RiwayatPendidikanSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiwayatPendidikan
        exclude = ["peserta"]


class RiwayatPekerjaanSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiwayatPekerjaan
        exclude = ["peserta"]


class DataKeluargaSerializer(serializers.ModelSerializer):
    usia = serializers.ReadOnlyField()

    class Meta:
        model = DataKeluarga
        exclude = ["peserta"]


class DokumenPesertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DokumenPeserta
        exclude = ["peserta"]


class PesertaDetailSerializer(serializers.ModelSerializer):
    usia = serializers.ReadOnlyField()

    riwayat_pendidikan = RiwayatPendidikanSerializer(many=True, read_only=True)
    riwayat_pekerjaan = RiwayatPekerjaanSerializer(many=True, read_only=True)
    data_keluarga = DataKeluargaSerializer(many=True, read_only=True)
    dokumen = DokumenPesertaSerializer(many=True, read_only=True)

    class Meta:
        model = Peserta
        fields = "__all__"


class PesertaWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Peserta
        exclude = [
            "created_at",
            "updated_at",
            "validasi_1_pada",
            "validasi_2_pada",
            "tervalidasi_pada"
        ]
        read_only_fields = [
            "status_validasi",
            "validasi_1_oleh",
            "validasi_2_oleh"
        ]



