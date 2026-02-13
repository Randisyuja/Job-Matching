from rest_framework import serializers
from .models import JenisPekerjaan, Lowongan, Persyaratan


class JenisPekerjaanSerializer(serializers.ModelSerializer):
    class Meta:
        model = JenisPekerjaan
        fields = "__all__"


class PersyaratanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persyaratan
        fields = ["id", "name"]


class LowonganListSerializer(serializers.ModelSerializer):
    jenis_pekerjaan = JenisPekerjaanSerializer(read_only=True)
    persyaratan = PersyaratanSerializer(
        many=True,
        read_only=True
    )
    is_expired = serializers.ReadOnlyField()
    sisa_kuota = serializers.ReadOnlyField()

    class Meta:
        model = Lowongan
        fields = [
            "id",
            "nama_perusahaan",
            "jenis_pekerjaan",
            "persyaratan",
            "kuota",
            "lokasi_kerja",
            "batas_lamar",
            "is_active",
            "is_expired",
            "sisa_kuota",
        ]


class LowonganWriteSerializer(serializers.ModelSerializer):
    jenis_pekerjaan = serializers.PrimaryKeyRelatedField(
        queryset=JenisPekerjaan.objects.all()
    )

    class Meta:
        model = Lowongan
        exclude = ("created_by", "updated_by")


class LowonganDetailSerializer(serializers.ModelSerializer):
    jenis_pekerjaan = JenisPekerjaanSerializer(read_only=True)
    persyaratan = PersyaratanSerializer(
        many=True,
        read_only=True
    )
    is_expired = serializers.ReadOnlyField()
    sisa_kuota = serializers.ReadOnlyField()

    class Meta:
        model = Lowongan
        fields = "__all__"
