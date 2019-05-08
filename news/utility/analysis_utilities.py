from collections import Counter
from news.utility.python_utilities import floor_log


class SectionSummaryKeywords:
    def __init__(self, section_title):
        self.section = section_title
        self.keywords_counters = {}
        self.counts_counters = Counter()

    def add_keyword(self, keywords, item_id, item_title):
        exists = False
        keyword = keywords[0]

        for key in keywords:
            if key in self.keywords_counters:
                exists = True
                keyword = key
                break

        keyword = keyword.term

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
        return [self.keywords_counters[keyword[0]].to_dict() for keyword in self.counts_counters.most_common(number)]

    def __str__(self):
        return "SSK: {} - {}".format(self.section, len(self.keywords_counters))


class KeywordCounter:
    def __init__(self, keyword, item_id, item_title):
        self.keyword = keyword
        self.counts = 1
        self.sample_title = item_title
        self.items = [{'id': item_id, 'title': item_title}]

    def update(self, item_id, item_title):
        self.counts += 1
        self.items.append({'id': item_id, 'title': item_title})

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return "KC: {} - {}".format(self.keyword, self.counts)