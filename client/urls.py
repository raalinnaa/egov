from client.views import RequestViewSet
from rest_framework import routers

router = routers.SimpleRouter()

router.register('clients', RequestViewSet, basename='clients')

urlpatterns = router.urls
