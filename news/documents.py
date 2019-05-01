from elasticsearch_dsl import analyzer
from elasticsearch_dsl.connections import connections

from django_elasticsearch_dsl import DocType, Index, fields
from news.models import Item
from news.utility.python_utilities import calc_tf_idf, floor_log

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "asciifolding", "stop", "snowball"],
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

    @classmethod
    def keywords(cls, es_id, field='article'):
        if not es_id:
            return []

        cn = connections.get_connection()
        keys = cn.termvectors(
            index='items',
            doc_type='doc',
            id=es_id,
            fields=field,
            term_statistics=True,
            positions=False,
            offsets=False,
            payloads=False
        )

        total = keys['term_vectors'][field]['field_statistics']
        key_dict = keys['term_vectors'][field]['terms']

        key_tfidf = {k: calc_tf_idf(v['term_freq'], v['doc_freq'], total['doc_count']) for k, v in key_dict.items()}
        key_list = [k[0] for k in sorted(key_tfidf.items(), key=lambda kv: kv[1], reverse=True) if not k[0].isnumeric()]
        index = floor_log(total['sum_ttf'] / total['doc_count'])

        return key_list[:index]

    @classmethod
    def get_internal_id(cls, item_id):
        res = ItemDocument.search().filter("match", id=item_id).execute()
        return res.hits[0].meta.id if res.hits.total else None

    class Meta:
        model = Item
        fields = ['id', 'title', 'pubDate', 'creator']


if __name__ == '__main__':
    qs = ItemDocument.search().query("match_phrase", article="messi")
    print(qs)
