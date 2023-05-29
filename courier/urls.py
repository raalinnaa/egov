from courier.views import CouriersCenterViewSet
from rest_framework import routers

router = routers.SimpleRouter()

router.register('courier_centers', CouriersCenterViewSet, basename='courier_centers')

urlpatterns = router.urls
