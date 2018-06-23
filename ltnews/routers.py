from rest_framework import routers
from news.serializer.viewsets import ProfileViewSet, SectionViewSet

router = routers.DefaultRouter()

router.register(r'profile', ProfileViewSet)
router.register(r'section', SectionViewSet)
