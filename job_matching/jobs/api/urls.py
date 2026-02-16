from rest_framework.routers import DefaultRouter
from .views import (
    JenisPekerjaanViewSet,
    LowonganViewSet,
    PersyaratanViewSet
)

router = DefaultRouter()
router.register("jenis-pekerjaan", JenisPekerjaanViewSet)
router.register("lowongan", LowonganViewSet)
router.register("persyaratan", PersyaratanViewSet)

urlpatterns = router.urls
