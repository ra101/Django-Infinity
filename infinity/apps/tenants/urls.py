from rest_framework.routers import SimpleRouter

from .views import ViewForTenantShared


router = SimpleRouter()
router.register(r'tenants', ViewForTenantShared)

urlpatterns = router.urls
