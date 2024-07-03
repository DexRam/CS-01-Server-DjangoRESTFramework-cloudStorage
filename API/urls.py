from django.urls import path, include
from rest_framework import routers
from .views import FileViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r"user", UserViewSet)
router.register(r"file", FileViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
