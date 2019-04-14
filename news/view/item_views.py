from rest_framework import status, serializers
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from news.serializers import ItemSerializer
from news.service.item_services import get_item, get_last_items_by_user, get_status_by_user_item, get_item_query, \
    get_item_similarity, get_item_simple_search, get_item_advanced_search, get_item_recommend, stats_items, get_summary, \
    get_item_saved, get_item_keywords


class ItemList(APIView):
    serializer_class = ItemSerializer
    pagination_class = PageNumberPagination()

    def get(self, request):
        items = get_last_items_by_user(request.user.id)

        follow = request.GET.get('follow', None)
        if follow is not None:
            for item_id in request.session.get('news_ids', []):
                get_status_by_user_item(request.user.id, item_id).as_view()
        request.session['news_ids'] = [x.id for x in items]

        page = self.pagination_class.paginate_queryset(items, request)
        serializer = self.serializer_class(page, many=True, context={'request': self.request})
        return self.pagination_class.get_paginated_response(serializer.data)


class ItemDetail(APIView):
    @staticmethod
    def get(request, item_id):
        item = get_item(item_id)
        get_status_by_user_item(request.user.id, item_id).as_read()
        serializer = ItemSerializer(item, context={'request': request})
        return Response(serializer.data)

    @staticmethod
    def put(request, item_id):
        item_status = get_status_by_user_item(request.user.id, item_id)

        like = request.data.get('like', None)
        if like is not None:
            if like:
                item_status.as_like()
            else:
                item_status.as_unlike()

        save = request.data.get('saves', None)
        if save is not None:
            if save:
                item_status.as_save()
            else:
                item_status.as_unsave()

        web = request.data.get('web', None)
        if web:
            item_status.as_web()

        return Response(status=status.HTTP_201_CREATED)


class ItemQuery(APIView):
    @staticmethod
    def get(request, query):
        items = get_item_query(query, request.user.profile.id)
        request.session['stats_items'] = stats_items(items)
        return Response(ItemSerializer(items, many=True, context={'request': request}).data)


class ItemRecommend(ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        return get_item_recommend(self.request.user.profile.id)


class ItemSimilarity(ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        limit = 6
        return get_item_similarity(self.kwargs['item_id'], limit, self.request.user.id)


class ItemKeywords(APIView):
    @staticmethod
    def get(request, item_id):
        links = get_item_keywords(item_id)
        return Response(links)


class ItemSummary(ListAPIView):
    serializer_class = serializers.Serializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return get_summary(self.request.user.id)


class ItemSaved(ListAPIView):
    serializer_class = ItemSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return get_item_saved(self.request.user.id)


class ItemSearch(ListAPIView):
    serializer_class = ItemSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        cleaned_data = self.request.query_params.get('query', '')
        limit = 24
        return get_item_simple_search(cleaned_data, limit, self.request.user.id)
