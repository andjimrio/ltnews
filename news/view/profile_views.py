from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from news.serializers import ProfileSerializer
from news.service.profile_services import get_profile, get_status_read_stats_by_user, get_status_like_stats_by_user


class ProfileDetail(APIView):
    @staticmethod
    def get(request):
        profile = get_profile(request.user.id)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    @staticmethod
    def put(request):
        profile = get_profile(request.user.id)
        serializer = ProfileSerializer(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileStats(APIView):
    @staticmethod
    def get(request, stat):
        profile_id = request.user.profile.id

        if stat == 'read':
            stats = get_status_read_stats_by_user(profile_id)
        elif stat == 'like':
            stats = get_status_like_stats_by_user(profile_id)
        else:
            stats = []

        return Response(stats)
