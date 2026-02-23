from rest_framework.routers import DefaultRouter
from .views import PesertaViewSet

router = DefaultRouter()
router.register("peserta", PesertaViewSet)

urlpatterns = router.urls
