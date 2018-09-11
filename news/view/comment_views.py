from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from news.serializers import CommentSerializer
from news.service.item_services import get_item
from news.service.comment_services import get_comments_by_item, delete_comment


class CommentList(APIView):
    @staticmethod
    def get(request, item_id):
        comments = get_comments_by_item(item_id)
        return Response(CommentSerializer(comments, many=True).data)

    @staticmethod
    def post(request, item_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user.profile, item=get_item(item_id))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    @staticmethod
    def delete(request, comment_id):
        delete_comment(comment_id, request.user.profile.id)
        return Response(status=status.HTTP_204_NO_CONTENT)
