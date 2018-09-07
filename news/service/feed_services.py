from django.shortcuts import get_object_or_404
from news.models import Feed


def create_feed(**dict_feed):
    return Feed.objects.get_or_create(**dict_feed)


def get_feed(feed_id, user):
    feed = get_object_or_404(Feed, pk=feed_id)
    return feed


def delete_feed(feed_id, user):
    feed = get_feed(feed_id, user)
    section = get_section_by_feed(feed, user)
    section.feeds.remove(feed)
    section.save()


def get_section_by_feed(feed, user):
    return feed.sections.all().get(user__user_id=user.id)


def all_feeds_link(user_id=None):
    if user_id is None:
        return Feed.objects.all().values_list('link_rss', flat=True)
    else:
        return Feed.objects.all().exclude(sections__user__user_id=user_id).values_list('link_rss', flat=True)


def get_feeds_by_user(user_id):
    return Feed.objects.filter(sections__user__user_id=user_id).all()


def exists_feed_id_by_link(link_rss):
    return Feed.objects.filter(link_rss=link_rss).exists()


def get_feed_by_link(link_rss):
    return Feed.objects.get(link_rss=link_rss)
