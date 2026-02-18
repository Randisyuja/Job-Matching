from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.utils import timezone

from ..models import JenisPekerjaan, Lowongan, Persyaratan
from .serializers import (
    JenisPekerjaanSerializer,
    LowonganListSerializer,
    LowonganWriteSerializer,
    LowonganDetailSerializer,
    PersyaratanSerializer
)
from .services import LowonganService


class JenisPekerjaanViewSet(viewsets.ModelViewSet):
    queryset = JenisPekerjaan.objects.all()
    serializer_class = JenisPekerjaanSerializer


class LowonganViewSet(viewsets.ModelViewSet):
    queryset = Lowongan.objects.select_related("jenis_pekerjaan").all()

    def get_serializer_class(self):
        if self.action == "list":
            return LowonganListSerializer
        if self.action == "retrieve":
            return LowonganDetailSerializer
        if self.action in ["create", "update", "partial_update"]:
            return LowonganWriteSerializer
        return LowonganListSerializer

    def perform_create(self, serializer):
        data = LowonganService.create_lowongan(
            data=serializer.validated_data,
            user=self.request.user
        )
        serializer.save(**data)

    def perform_update(self, serializer):
        data = LowonganService.update_lowongan(
            instance=self.get_object(),
            data=serializer.validated_data,
            user=self.request.user
        )
        serializer.save(**data)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            return queryset.filter(is_active=True)
        return queryset


class PersyaratanViewSet(viewsets.ModelViewSet):
    queryset = Persyaratan.objects.all()
    serializer_class = PersyaratanSerializer
