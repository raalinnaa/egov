from rest_framework import routers
from orders.views import AddressViewSet,  OrderViewSet

router = routers.SimpleRouter()

router.register('address', AddressViewSet, basename='address')
router.register('order', OrderViewSet, basename='order')

urlpatterns = router.urls
