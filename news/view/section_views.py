from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from news.serializers import SectionSerializer
from news.service.section_services import get_section, delete_section, get_sections_by_user


class SectionList(APIView):
    @staticmethod
    def get(request):
        sections = get_sections_by_user(request.user.id)
        return Response(SectionSerializer(sections, many=True).data)

    @staticmethod
    def post(request):
        serializer = SectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user.profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SectionDetail(APIView):
    @staticmethod
    def get(request, section_id):
        section = get_section(section_id, request.user)
        serializer = SectionSerializer(section)
        return Response(serializer.data)

    @staticmethod
    def put(request, section_id):
        section = get_section(section_id, request.user)
        serializer = SectionSerializer(section, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user.profile)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, section_id):
        delete_section(section_id, request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
