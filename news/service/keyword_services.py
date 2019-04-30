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