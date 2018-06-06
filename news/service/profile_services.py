from django.db.models import Count
from news.models import Profile, Status, Keyword


def all_profile():
    return Profile.objects.all()


def get_profile(user_id):
    return Profile.objects.get(user=user_id)


def get_filtered_status_by_profile(profile_id):
    return Status.objects.filter(user_id=profile_id).filter(read=True)\
        .union(Status.objects.filter(user_id=profile_id).filter(like=True))


def get_status_read_stats_by_user(profile_id):
    return Status.objects.filter(user_id=profile_id) \
        .filter(read=True) \
        .values('item__feed__sections__title')\
        .annotate(total=Count('id'))


def get_status_like_stats_by_user(profile_id):
    return Status.objects.filter(user_id=profile_id) \
        .filter(like=True) \
        .values('item__feed__sections__title')\
        .annotate(total=Count('id'))


def get_keywords_by_user(user_id):
    return Keyword.objects.filter(users__user=user_id).all()


def exists_user(username):
    return Profile.objects.filter(user__username__exact=username).exists()
