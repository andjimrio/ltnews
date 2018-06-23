from rest_framework import viewsets
from news.models import Profile, Section
from news.serializer.serializers import ProfileSerializer, SectionSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer