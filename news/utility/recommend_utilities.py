from collections import Counter

from news.utility.python_utilities import floor_log
from news.service.keyword_services import delete_keyword_by_user, update_keyword_by_user
from news.service.item_services import get_filtered_status_by_user

def recommend_based_content(profile):
    cont_user = Counter()

    for status in get_filtered_status_by_user(profile.id):
        for tag in status.item.keywords.all():
            cont_user[tag.term] += status.get_score()

    delete_keyword_by_user(profile.id)
    number = floor_log(len(cont_user))
    keywords = cont_user.most_common(number)

    for tag_x, tag_y in keywords:
        update_keyword_by_user(profile, tag_x)

    return dict(cont_user), keywords