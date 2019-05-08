from django.contrib import admin
from django.urls import path, include
from news.view import feed_views, item_views, profile_views, section_views, comment_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),

    path('auth/', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),

    path('profile/', profile_views.ProfileDetail.as_view(), name='profile_detail'),
    path('profile/stats/<slug:stat>/', profile_views.ProfileStats.as_view(), name='profile_detail'),

    path('section/', section_views.SectionList.as_view(), name='section_list'),
    path('section/<int:section_id>/', section_views.SectionDetail.as_view(), name='section_detail'),
    path('section/names/', section_views.SectionNames.as_view(), name='section_names'),

    path('feed/', feed_views.FeedList.as_view(), name='feed_list'),
    path('feed/<int:feed_id>/', feed_views.FeedDetail.as_view(), name='feed_detail'),
    path('feed/<int:feed_id>/items/', feed_views.FeedItems.as_view(), name='feed_items'),
    path('feed/links/', feed_views.FeedLinks.as_view(), name='feed_links'),

    path('item/', item_views.ItemList.as_view(), name='item_list'),
    path('item/<int:item_id>/', item_views.ItemDetail.as_view(), name='item_detail'),
    path('item/<int:item_id>/similarity/', item_views.ItemSimilarity.as_view(), name='item_similarity'),
    path('item/<int:item_id>/keywords/', item_views.ItemKeywords.as_view(), name='item_keywords'),
    path('item/query/<str:query>/', item_views.ItemQuery.as_view(), name='item_query'),
    path('item/recommend/', item_views.ItemRecommend.as_view(), name='item_recommend'),
    path('item/summary/', item_views.ItemSummary.as_view(), name='item_summary'),
    path('item/search/', item_views.ItemSearch.as_view(), name='item_search'),
    path('item/saved/', item_views.ItemSaved.as_view(), name='item_saved'),

    path('item/<int:item_id>/comments/', comment_views.CommentList.as_view(), name='comment_list'),
    path('comment/<int:comment_id>/', comment_views.CommentDetail.as_view(), name='comment_detail'),
]
