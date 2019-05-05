from collections import Counter

from django.utils import timezone
from django.shortcuts import get_object_or_404
from elasticsearch_dsl import Q
from elasticsearch_dsl.query import MoreLikeThis

from news.models import Item, Profile, Section, Status, Feed
from news.documents import ItemDocument
from news.utility.python_utilities import floor_log
from news.service.profile_services import get_profile, get_keywords_by_user
from news.service.section_services import get_sections_by_user


def create_item(**dict_item):
    return Item.objects.get_or_create(**dict_item)


def get_item(item_id):
    return get_object_or_404(Item, pk=item_id)


def exists_item_by_link(link):
    return Item.objects.filter(link=link).exists()


def get_status_by_user_item(user_id, item_id):
    return Status.objects.get_or_create(user_id=get_profile(user_id).id, item_id=item_id)[0]


def get_filtered_status_by_user(user_id):
    return Status.objects.filter(user_id=user_id, read=True)


def get_last_items_by_user(user_id, unview=False):
    if unview:
        items_id = Profile.objects.get(user__id=user_id).sections.all() \
            .values_list('feeds__items', flat=True)
    else:
        items_id = Profile.objects.get(user__id=user_id).statuses.all().filter(view=False) \
            .values_list('item', flat=True)

    return Item.objects.filter(id__in=items_id).order_by('-pubDate')


def get_last_items_by_feed(feed_id):
    return Feed.objects.get(id=feed_id).items.order_by('-pubDate')


def get_item_today_by_section(section_id, days=0, hours=0):
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=days, hours=hours)
    return Section.objects.filter(id=section_id).filter(feeds__items__pubDate__range=[start_date, end_date]) \
        .values('feeds__items__id', 'feeds__items__title')


def get_item_similarity(item_id, limit, user_id):
    doc_id = ItemDocument.get_internal_id(item_id)
    more_results = ItemDocument.search() \
        .query(MoreLikeThis(like={'_id': doc_id}, fields=['article'], min_term_freq=1)) \
        .extra(size=limit) \
        .to_queryset() \
        .filter(statuses__user__user_id=user_id).order_by('-pubDate')
    return more_results


def get_item_query(query, profile_id):
    results = Item.objects.filter(keywords__term__contains=query) \
        .filter(feed__sections__user_id=profile_id) \
        .order_by('-pubDate')
    return results


def get_item_search(query, limit, user_id):
    if isinstance(query, str):
        query_in = Q("multi_match", query=query, fields=['title', 'article'])
    else:
        query_in = Q('bool', must=[Q({'match': {k: v}}) for k, v in query.items()])

    results = ItemDocument.search()\
        .query(query_in)\
        .extra(size=limit) \
        .to_queryset() \
        .filter(statuses__user__user_id=user_id).order_by('-pubDate')
    return results


def stats_items(queryset):
    stats = [x.pubDate.strftime("%m/%Y") for x in queryset]
    return dict(Counter(stats))


def get_item_recommend(profile_id):
    results = Item.objects.filter(feed__sections__user_id=profile_id) \
        .exclude(statuses__view=True) \
        .filter(keywords__in=get_keywords_by_user(profile_id)) \
        .order_by('-pubDate')
    return results


def get_item_saved(user_id):
    return Item.objects.filter(statuses__user__user_id=user_id) \
        .filter(statuses__saves=True) \
        .order_by('-pubDate')


def get_summary(user_id):
    summary_keywords = dict()

    for section in get_sections_by_user(user_id):
        section_summary_keywords = SectionSummaryKeywords(section.title)
        for item in get_item_today_by_section(section.id, days=1):
            keywords = get_item(item['feeds__items__id']).keywords.all()
            if len(keywords) > 0:
                section_summary_keywords.add_keyword(keywords, item['feeds__items__id'], item['feeds__items__title'])

        summary_keywords[section.title] = section_summary_keywords.most_common()

    return summary_keywords


class SectionSummaryKeywords:
    def __init__(self, section_title):
        self.section = section_title
        self.keywords_counters = dict()
        self.counts_counters = Counter()

    def add_keyword(self, keywords, item_id, item_title):
        exists = False
        keyword = keywords[0]

        for key in keywords:
            if key in self.keywords_counters:
                exists = True
                keyword = key
                break

        if exists:
            self.keywords_counters[keyword].update(item_id, item_title)
        else:
            keyword_counter = KeywordCounter(keyword, item_id, item_title)
            self.keywords_counters[keyword] = keyword_counter

        self.counts_counters[keyword] += 1

    def most_common(self, number=None):
        if not number and self.counts_counters:
            number = floor_log(len(self.counts_counters))
        else:
            number = 0
        return [self.keywords_counters[keyword[0]] for keyword in self.counts_counters.most_common(number)]

    def __str__(self):
        return "SSK: {} - {}".format(self.section, len(self.keywords_counters))


class KeywordCounter:
    def __init__(self, keyword, item_id, item_title):
        self.keyword = keyword
        self.counts = 1
        self.sample_title = item_title
        self.items = dict()
        self.items[item_id] = item_title

    def update(self, item_id, item_title):
        self.counts += 1
        self.items[item_id] = item_title

    def __str__(self):
        return "KC: {} - {}".format(self.keyword, self.counts)
