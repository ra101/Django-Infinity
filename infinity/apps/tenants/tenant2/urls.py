from rest_framework.routers import SimpleRouter

from .views import ViewForTenant2


router = SimpleRouter()
router.register(r'tenant2', ViewForTenant2)

urlpatterns = router.urls
