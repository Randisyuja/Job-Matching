# apps/participants/serializers.py
from rest_framework import serializers
from ..models import (
    Peserta, RiwayatPendidikan, RiwayatPekerjaan,
    DataKeluarga, DokumenPeserta
)
from job_matching.accounts.api.serializers import UserSerializer


class RiwayatPendidikanSerializer(serializers.ModelSerializer):
    jenjang_display = serializers.CharField(source='get_jenjang_display', read_only=True)

    class Meta:
        model = RiwayatPendidikan
        fields = ['id', 'peserta', 'jenjang', 'jenjang_display', 
                  'nama_institusi', 'tahun_masuk', 'tahun_lulus']
        read_only_fields = ['id', 'peserta']


class RiwayatPekerjaanSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiwayatPekerjaan
        fields = ['id', 'peserta', 'nama_perusahaan', 'bidang_usaha',
                  'jabatan', 'gaji', 'tanggal_masuk', 'tanggal_keluar']
        read_only_fields = ['id', 'peserta']


class DataKeluargaSerializer(serializers.ModelSerializer):
    hubungan_display = serializers.CharField(source='get_hubungan_keluarga_display', read_only=True)
    
    class Meta:
        model = DataKeluarga
        fields = ['id', 'peserta', 'hubungan_keluarga', 'hubungan_display',
                  'nama', 'usia', 'pekerjaan']
        read_only_fields = ['id', 'peserta']


class DokumenPesertaSerializer(serializers.ModelSerializer):
    """Serializer for participant documents"""

    jenis_display = serializers.CharField(source='get_jenis_dokumen_display', read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = DokumenPeserta
        fields = ['id', 'peserta', 'jenis_dokumen', 'jenis_display',
                  'nama_dokumen', 'file_path', 'file_url', 'uploaded_at']
        read_only_fields = ['id', 'peserta', 'uploaded_at']
    
    def get_file_url(self, obj):
        if obj.file_path:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file_path.url)
        return None


class PesertaListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    
    status_display = serializers.CharField(source='get_status_validasi_display', read_only=True)
    usia = serializers.ReadOnlyField()
    validation_progress = serializers.ReadOnlyField()
    
    class Meta:
        model = Peserta
        fields = ['user', 'nama_lengkap', 'tanggal_lahir', 'usia',
                  'jenis_kelamin', 'nomor_hp', 'minat_program',
                  'status_validasi', 'status_display', 'validation_progress',
                  'created_at']


class PesertaDetailSerializer(serializers.ModelSerializer):
    """Full serializer for detail views"""
    
    user = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_validasi_display', read_only=True)
    usia = serializers.ReadOnlyField()
    can_apply_jobs = serializers.ReadOnlyField()
    validation_progress = serializers.ReadOnlyField()
    
    # Related data
    riwayat_pendidikan = RiwayatPendidikanSerializer(many=True, read_only=True)
    riwayat_pekerjaan = RiwayatPekerjaanSerializer(many=True, read_only=True)
    data_keluarga = DataKeluargaSerializer(many=True, read_only=True)
    dokumen = DokumenPesertaSerializer(many=True, read_only=True)
    
    # Validators
    validated_1_by_email = serializers.EmailField(source='validated_1_by.email', read_only=True)
    validated_2_by_email = serializers.EmailField(source='validated_2_by.email', read_only=True)
    
    class Meta:
        model = Peserta
        fields = '__all__'
        read_only_fields = ['user', 'status_validasi', 'validated_1_at', 'validated_1_by',
                           'validation_1_notes', 'validated_2_at', 'validated_2_by',
                           'validation_2_notes', 'approved_at', 'rejection_reason',
                           'created_at', 'updated_at', 'updated_by']


class PesertaCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating peserta"""
    
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = Peserta
        fields = ['email', 'password', 'nama_lengkap', 'nama_lengkap_katakana',
                  'tanggal_lahir', 'jenis_kelamin', 'agama', 'nomor_hp',
                  'status_pernikahan', 'alamat_ktp', 'alamat_domisili',
                  'minat_program', 'pengalaman_ke_jepang', 'tujuan_ke_jepang',
                  'penghasilan_keluarga', 'target_penabungan', 'berat_badan',
                  'tinggi_badan', 'cek_mata_kanan', 'cek_mata_kiri',
                  'golongan_darah', 'tangan_dominan', 'alergi_makanan',
                  'pantangan_makanan', 'riwayat_penyakit', 'kelebihan',
                  'kekurangan', 'hobi']
    
    def create(self, validated_data):
        from apps.accounts.services import UserService
        
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        
        user, peserta = UserService.create_peserta_account(
            email=email,
            password=password,
            **validated_data
        )
        
        return peserta


class PesertaUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating peserta (restricted fields based on status)"""
    
    class Meta:
        model = Peserta
        exclude = ['user', 'status_validasi', 'validated_1_at', 'validated_1_by',
                   'validation_1_notes', 'validated_2_at', 'validated_2_by',
                   'validation_2_notes', 'approved_at', 'rejection_reason',
                   'created_at', 'updated_at', 'updated_by']
    
    def validate(self, attrs):
        # Prevent editing if already submitted
        instance = self.instance
        if instance and instance.status_validasi not in ['draft', 'rejected_1', 'rejected_2']:
            raise serializers.ValidationError(
                "Cannot edit profile once submitted. Contact admin if changes needed."
            )
        return attrs


class ValidationSerializer(serializers.Serializer):
    """Serializer for validation actions"""
    
    notes = serializers.CharField(required=False, allow_blank=True)
    reason = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, attrs):
        action = self.context.get('action')
        
        if action in ['reject_level_1', 'reject_level_2', 'suspend']:
            if not attrs.get('reason'):
                raise serializers.ValidationError({
                    'reason': 'Reason is required for rejection/suspension'
                })
        
        return attrs