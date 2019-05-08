from news.models import Keyword, Profile
from news.documents import ItemDocument


def create_keywords(item):
    item_id = item.id
    elk_id = ItemDocument.get_internal_id(item_id)

    for term in ItemDocument.keywords(elk_id):
        keyword, created = Keyword.objects.get_or_create(term=term)
        keyword.items.add(item)
        keyword.save()


def update_keyword_by_user(profile, term):
    keyword, created = Keyword.objects.get_or_create(term=term)
    keyword.users.add(profile)
    keyword.save()


def get_keywords_by_user(profile_id):
    return Keyword.objects.filter(users__id=profile_id).all()


def get_item_keywords(item_id):
    keys = Keyword.objects.filter(items__id=item_id)
    if keys.count():
        return keys.values_list('term', flat=True)
    else:
        doc_id = ItemDocument.get_internal_id(item_id)
        return ItemDocument.keywords(doc_id)


def delete_keyword_by_user(profile_id):
    Profile.objects.get(id=profile_id).keywords.clear()