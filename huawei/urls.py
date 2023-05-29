from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)
from rest_framework import routers

router = routers.SimpleRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('', include('users.urls')),
        path('', include('client.urls')),
        path('', include('courier.urls')),
        path('', include('orders.urls')),
        path('', include('con.urls')),
    ]))
]

urlpatterns += router.urls

urlpatterns += [
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
