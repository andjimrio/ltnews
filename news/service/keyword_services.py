from news.models import Keyword
from news.documents import ItemDocument


def create_keywords(item):
    item_id = item.id
    elk_id = ItemDocument.get_internal_id(item_id)

    for section in item.feed.sections.all():
        for term in ItemDocument.keywords(elk_id):
            keyword, created = Keyword.objects.get_or_create(term=term)
            keyword.items.add(item)
            keyword.users.add(section.user)
            keyword.save()

def update_keyword_by_user(profile, term):
    keyword, created = Keyword.objects.get_or_create(term=term)
    keyword.users.add(profile)
    keyword.save()


def get_item_keywords(item_id, profile_id):
    keys = Keyword.objects.filter(items__id=item_id, users__id=profile_id)
    if keys.count():
        return keys.values_list('term', flat=True)
    else:
        doc_id = ItemDocument.get_internal_id(item_id)
        return ItemDocument.keywords(doc_id)

def delete_keyword_by_user(profile_id):
    Keyword.objects.filter(users__id=profile_id).delete()