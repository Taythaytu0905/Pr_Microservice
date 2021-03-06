from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

from products.views import ProductViewSet, UserAPIView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'product', ProductViewSet, basename="product")
urlpatterns = [
    url(r'^', include(router.urls)),
    path('user', UserAPIView.as_view())
]

