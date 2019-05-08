from collections import Counter
from news.utility.python_utilities import floor_log


class SectionSummaryKeywords:
    def __init__(self, section_title):
        self.section = section_title
        self.keywords_counters = {}
        self.counts_counters = Counter()

    def add_keyword(self, keywords, item):
        for key in keywords:
            keyword = key.term
            self.counts_counters[keyword] += 1

            if keyword in self.keywords_counters:
                self.keywords_counters[keyword].update(item)
            else:
                self.keywords_counters[keyword] = KeywordCounter(keyword, item)


    def most_common(self, number=None):
        if not number and self.counts_counters:
            number = floor_log(len(self.counts_counters))
        else:
            number = 0

        results = []
        titles = []

        for keyword, score in self.counts_counters.most_common(number*2):
            counter = self.keywords_counters[keyword]
            if score > 1 and counter.sample_title not in titles:
                results.append(counter.to_dict())
                titles.append(counter.sample_title)

            if len(titles) == number:
                break

        return results

    def __str__(self):
        return "SSK: {} - {}".format(self.section, len(self.keywords_counters))


class KeywordCounter:
    def __init__(self, keyword, item):
        self.keyword = keyword
        self.counts = 1
        self.sample_title = item['title']
        self.items = [item]

    def update(self, item):
        self.counts += 1
        self.items.append(item)

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return "KC: {} - {}".format(self.keyword, self.counts)
