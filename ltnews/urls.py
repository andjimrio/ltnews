from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from ltnews.routers import router
from news import views
from news.view import feed_views, item_views, profile_views, section_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),

    path('profile/', include([
        path('view/', profile_views.profile_view, name='profile_view'),
        path('edit/', profile_views.profile_edit, name='profile_edit'),
    ])),

    path('section/', include([
        path('view/<int:section_id>/', section_views.section_view, name='section_view'),
        path('edit/<int:section_id>/', section_views.section_edit, name='section_edit'),
        path('delete/<int:section_id>/', section_views.section_delete, name='section_delete'),
    ])),

    path('feed/', include([
        path('list/', feed_views.feed_list, name='feed_list'),
        path('view/<int:feed_id>/', feed_views.feed_view, name='feed_view'),
        path('edit/<int:feed_id>/', feed_views.feed_create, name='feed_create'),
        path('delete/<int:section_id>/<int:feed_id>/', feed_views.feed_delete, name='feed_delete'),
    ])),

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
