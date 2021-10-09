from rest_framework import routers

from .views import InfiniteRedisViewSet

router = routers.SimpleRouter()
router.register(r"infinite_redis", InfiniteRedisViewSet, "infinite-redis")
urlpatterns = router.urls
