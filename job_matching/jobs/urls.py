from rest_framework.routers import DefaultRouter
from .views import (
    JenisPekerjaanViewSet,
    LowonganViewSet,
    PersyaratanViewSet
)

router = DefaultRouter()
router.register(r'jenis-pekerjaan', JenisPekerjaanViewSet)
router.register(r'lowongan', LowonganViewSet)
router.register(r'persyaratan', PersyaratanViewSet)

urlpatterns = router.urls
