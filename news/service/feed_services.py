from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from news.models import Feed
from news.service.section_services import get_section


def create_feed(**dict_feed):
    return Feed.objects.get_or_create(**dict_feed)


def delete_feed(section_id, feed_id, user_id):
    if user_has_feed(user_id, feed_id):
        section = get_section(section_id)
        section.feeds.remove(get_feed(feed_id))
        section.save()
        return True
    else:
        raise PermissionDenied


def get_feed(feed_id):
    return get_object_or_404(Feed, pk=feed_id)


def get_section_by_feed(feed_id, user_id):
    return get_feed(feed_id).sections.all().get(user__user_id=user_id)


def all_feeds_link(user_id=None):
    if user_id is None:
        return Feed.objects.all().values('link_rss')
    else:
        return Feed.objects.all().exclude(sections__user__user_id=user_id).values('link_rss')


def get_feeds_by_user(user_id):
    return Feed.objects.filter(sections__user__user_id=user_id).all()


def user_has_feed(user_id, feed_id):
    return get_feeds_by_user(user_id).filter(id=feed_id).exists()


def exists_feed_id_by_link(link_rss):
    return Feed.objects.filter(link_rss=link_rss).exists()


def get_feed_by_link(link_rss):
    return Feed.objects.get(link_rss=link_rss)
