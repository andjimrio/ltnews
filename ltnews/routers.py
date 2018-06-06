from rest_framework import routers
from news.serializer.viewsets import ProfileViewSet

router = routers.DefaultRouter()

router.register(r'profile', ProfileViewSet)