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
    path('feed/links/', feed_views.FeedMoreDetail.as_view(), name='feed_links'),

    path('item/', include([
        path('list/', item_views.item_list, name='item_list'),
        path('view/<int:item_id>/', item_views.item_view, name='item_view'),
        path('query/<slug:query>/', item_views.item_query, name='item_query'),
        path('recommend/', item_views.item_recommend, name='item_recommend'),
        path('summary/', item_views.item_summary, name='item_summary'),
        path('search/', item_views.item_search, name='item_search'),
        path('saved/', item_views.item_saved, name='item_saved'),
    ])),
]
