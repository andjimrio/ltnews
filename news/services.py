from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied


def get_pagination(page, query):
    paginator = Paginator(query, 20)

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    return news


def check_user(model, user):
    if model.user.user.id != user.id:
        raise PermissionDenied


def add_profile_data(data, user):
    data['user'] = user.profile.id
    return data
