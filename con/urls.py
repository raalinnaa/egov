from con.views import ConViewSet
from rest_framework import routers

router = routers.SimpleRouter()

router.register('con', ConViewSet, basename='con')

urlpatterns = router.urls
