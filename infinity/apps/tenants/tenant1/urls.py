from rest_framework.routers import SimpleRouter

from .views import ViewForTenant1


router = SimpleRouter()
router.register(r'tenant1', ViewForTenant1)

urlpatterns = router.urls
