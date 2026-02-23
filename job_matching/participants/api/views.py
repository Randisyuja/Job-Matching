from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ..models import Peserta
from .serializers import PesertaDetailSerializer, PesertaWriteSerializer
from ..services import validate_level_1, validate_level_2, final_approve
from ..permissions import IsValidator


class PesertaViewSet(viewsets.ModelViewSet):

    queryset = Peserta.objects.select_related("user").prefetch_related(
        "riwayat_pendidikan",
        "riwayat_pekerjaan",
        "data_keluarga",
        "dokumen"
    )

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PesertaDetailSerializer
        return PesertaWriteSerializer

    def get_permissions(self):
        if self.action in ["validate_level_1", "validate_level_2", "approve"]:
            return [IsValidator()]
        return [permissions.IsAuthenticated()]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
