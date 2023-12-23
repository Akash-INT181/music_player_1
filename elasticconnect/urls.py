from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ElasticViewSet,
)


router = DefaultRouter()

router.register(r"elasticsongs", ElasticViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
