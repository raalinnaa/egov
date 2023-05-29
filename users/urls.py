from users.views import UserViewSet
from rest_framework import routers

router = routers.SimpleRouter()

router.register('users', UserViewSet, basename='users')

urlpatterns = router.urls
