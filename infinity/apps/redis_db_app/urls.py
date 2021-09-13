from rest_framework import routers

from .views import RedisDBAppViewSet

router = routers.SimpleRouter()
router.register(r'redis_db_app', RedisDBAppViewSet, 'redis-db-app')
urlpatterns = router.urls
