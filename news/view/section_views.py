from rest_framework.views import APIView
from rest_framework.response import Response
from news.services import check_user, add_profile_data
from news.service.section_services import get_sections_by_user
from news.service.section_services import get_section, delete_section
from news.serializer.serializers import SectionSerializer
from rest_framework import status


class SectionList(APIView):
    @staticmethod
    def get(request):
        sections = get_sections_by_user(request.user.id)
        return Response(SectionSerializer(sections, many=True).data)

    @staticmethod
    def post(request):
        serializer = SectionSerializer(data=add_profile_data(request.data, request.user))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SectionDetail(APIView):
    @staticmethod
    def get(request, section_id):
        section = get_section(section_id)
        check_user(section, request.user)
        serializer = SectionSerializer(section)
        return Response(serializer.data)

    @staticmethod
    def put(request, section_id):
        section = get_section(section_id)
        check_user(section, request.user)
        serializer = SectionSerializer(section, data=add_profile_data(request.data, request.user))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, section_id):
        delete_section(section_id, request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)
