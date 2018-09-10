from rest_framework import status, serializers
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from news.serializers import ItemSerializer
from news.service.item_services import get_item, get_last_items_by_user, get_status_by_user_item, get_item_query,\
    get_item_similarity, query_multifield_dict, get_item_recommend, stats_items, get_summary, get_item_saved


class ItemList(APIView):
    @staticmethod
    def get(request):
        items = get_last_items_by_user(request.user.id)

        follow = request.GET.get('follow', None)
        if follow is not None:
            for item_id in request.session.get('news_ids', []):
                get_status_by_user_item(request.user.id, item_id).as_view()
        request.session['news_ids'] = [x.id for x in items]

        return Response(ItemSerializer(items, many=True).data)


class ItemDetail(APIView):
    @staticmethod
    def get(request, item_id):
        item = get_item(item_id)
        get_status_by_user_item(request.user.id, item_id).as_read()
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    @staticmethod
    def post(request, item_id):
        item_status = get_status_by_user_item(request.user.id, item_id)

        like = request.data.get('like', None)
        if like == 'True':
            item_status.as_like()
        elif like == 'False':
            item_status.as_unlike()

        save = request.data.get('save', None)
        if save == 'True':
            item_status.as_save()
        elif save == 'False':
            item_status.as_unsave()

        web = request.data.get('web', None)
        if web == 'True':
            item_status.as_web()

        return Response(status=status.HTTP_201_CREATED)


class ItemQuery(APIView):
    @staticmethod
    def get(request, query):
        items = get_item_query(query, request.user.profile.id)
        request.session['stats_items'] = stats_items(items)
        return Response(ItemSerializer(items, many=True).data)


class ItemRecommend(ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        return get_item_recommend(self.request.user.profile.id)


class ItemSimilarity(ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        return get_item_similarity(self.kwargs['item_id'], 6, self.request.user.id)


class ItemSummary(ListAPIView):
    serializer_class = serializers.Serializer

    def get_queryset(self):
        return get_summary(self.request.user.id)


class ItemSaved(ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        return get_item_saved(self.request.user.id)


class ItemSearch(ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        params = ['title', 'creator', 'description', 'feed']
        cleaned_data = [self.request.query_params.get(param, None) for param in params]
        return query_multifield_dict(cleaned_data, self.request.user.profile.id)
