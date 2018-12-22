from elasticsearch_dsl import analyzer
from django_elasticsearch_dsl import DocType, Index, fields
from news.models import Item

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

item_index = Index('items')
item_index.settings(number_of_shards=1, number_of_replicas=0)


@item_index.doc_type
class ItemDocument(DocType):
    article = fields.TextField(
        analyzer=html_strip,
        fields={'raw': fields.KeywordField()}
    )

    class Meta:
        model = Item
        fields = ['title', 'pubDate', 'creator']


if __name__ == '__main__':
    qs = ItemDocument.search().query("match", article="messi")
    print(qs)
