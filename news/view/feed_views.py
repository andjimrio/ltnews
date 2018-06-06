from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from news.forms import FeedForm
from news.utility.populate_utilities import populate_rss
from news.services import get_pagination
from news.service.feed_services import get_feed, all_feeds_link, user_has_feed, get_section_by_feed, delete_feed
from news.service.section_services import get_sections_by_user


@login_required
def feed_create(request):
    error = False

    if request.method == 'POST':
        feed_form = FeedForm(request.POST)

        if feed_form.is_valid():
            url = feed_form.data['url']
            title_section = feed_form.data['section']

            feed = populate_rss(url, title_section, request.user.id)

            if feed:
                return redirect('feed_list')
            else:
                error = True

        else:
            print(feed_form.errors)

    else:
        feed_form = FeedForm(initial={'url': request.GET.get('url', ),
                                      'section': request.GET.get('section', )})

    urls = all_feeds_link(request.user.id)
    sections = get_sections_by_user(request.user.id)

    return render(request, 'feed/feed_create.html',
                  {'feed_form': feed_form, 'error': error, 'urls': urls, 'sections': sections})


@login_required
def feed_view(request, feed_id):
    feeder = get_feed(feed_id)
    news = get_pagination(request.GET.get('page'), feeder.items.all())
    has_feed = user_has_feed(request.user.id, feed_id)
    if has_feed:
        section_id = get_section_by_feed(feed_id, request.user.id).id
    else:
        section_id = 0

    return render(request, 'feed/feed_view.html', {'feed': feeder, 'news': news,
                                                   'has_feed': has_feed, 'section_id': section_id})


@login_required
def feed_list(request):
    sections = get_sections_by_user(request.user.id)
    return render(request, 'feed/feed_list.html', {'sections': sections})


@login_required
def feed_delete(request, section_id, feed_id):
    delete_feed(section_id, feed_id, request.user.id)
    return redirect('feed_list')
