from django.shortcuts import get_object_or_404
from news.services import check_user
from news.models import Profile, Section
from news.service.profile_services import get_profile


def create_section(title_section, user_id):
    return Section.objects.get_or_create(title=title_section, user=get_profile(user_id))


def get_section(section_id, user):
    section = get_object_or_404(Section, pk=section_id)
    check_user(section, user)
    return section


def delete_section(section_id, user):
    get_section(section_id, user).delete()


def get_sections_by_user(user_id):
    return Profile.objects.get(user__id=user_id).sections.all()


def get_section_items(section_id):
    return Section.objects.get(id=section_id).feeds.all()\
        .values('id', 'title', 'items__id', 'items__title', 'items__description',
                'items__pubDate', 'items__image')\
        .order_by('-items__pubDate')


def all_sections_names(user_id):
    return Profile.objects.get(user__id=user_id).sections.values_list('title', flat=True)
