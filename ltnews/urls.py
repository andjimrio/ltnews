from django.contrib import admin
from django.urls import path, include
from news.view import feed_views, item_views, profile_views, section_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),

    path('profile/', include([
        path('view/', profile_views.profile_view, name='profile_view'),
        path('edit/', profile_views.profile_edit, name='profile_edit'),
    ])),

    path('section/', section_views.SectionList.as_view(), name='section_list'),
    path('section/<int:section_id>/', section_views.SectionDetail.as_view(), name='section_detail'),

    path('feed/', feed_views.FeedList.as_view(), name='feed_list'),
    path('feed/<int:feed_id>/', feed_views.FeedDetail.as_view(), name='feed_detail'),
    path('feed/links/', feed_views.FeedLinks.as_view(), name='feed_links'),

    path('item/', item_views.ItemList.as_view(), name='item_list'),
    path('item/<int:item_id>/', item_views.ItemDetail.as_view(), name='item_detail'),
    path('item/<int:item_id>/similarity/', item_views.ItemSimilarity.as_view(), name='item_similarity'),
    path('item/query/<slug:query>/', item_views.ItemQuery.as_view(), name='item_query'),
    path('item/recommend/', item_views.ItemRecommend.as_view(), name='item_recommend'),
    path('item/summary/', item_views.ItemSummary.as_view(), name='item_summary'),
    path('item/search/', item_views.ItemSearch.as_view(), name='item_search'),
    path('item/saved/', item_views.ItemSaved.as_view(), name='item_saved'),
]
