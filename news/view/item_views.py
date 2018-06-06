from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from news.forms import ItemSearchForm, CommentForm
from news.service.item_services import get_item, get_last_items_by_user, get_status_by_user_item,\
    get_item_query, get_item_similarity, query_multifield_dict, get_item_recommend, stats_items, get_summary, \
    get_item_saved
from news.service.comment_services import delete_comment, get_comments_by_item
from news.services import get_pagination


@login_required
def item_view(request, item_id=None):
    like = request.GET.get('like')
    save = request.GET.get('save')
    web = request.GET.get('web')
    delete = request.GET.get('delete')

    item = get_item(item_id)

    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.item = item
        comment.user = request.user.profile
        comment.save()

        comment_form = CommentForm()
    else:
        if comment_form.errors:
            print(comment_form.errors)

    news = get_item_similarity(item_id, 6, request.user.id)
    comments = get_comments_by_item(item.id)
    status = get_status_by_user_item(request.user.id, item_id)[0]
    status.as_read()

    if web:
        status.as_web()
        return redirect(item.link)

    if like == 'True':
        status.as_like()
    elif like == 'False':
        status.as_unlike()

    if save == 'True':
        status.as_save()
    elif save == 'False':
        status.as_unsave()

    if delete:
        delete_comment(delete, request.user.id)

    return render(request, 'item/item_view.html', {'item': item, 'news': news, 'status': status,
                                                   'comments': comments, 'comment_form': comment_form})


@login_required
def item_list(request):
    follow = request.GET.get('follow')

    if follow is not None:
        for item_id in request.session.get('news_ids', []):
            status = get_status_by_user_item(request.user.id, item_id)[0]
            status.as_view()

    news = get_pagination(request.GET.get('page'), get_last_items_by_user(request.user.id))
    request.session['news_ids'] = [x['item_id'] for x in news]

    return render(request, 'item/item_list.html', {'news': news})


@login_required
def item_query(request, query):
    queryset = get_item_query(query, request.user.profile.id)
    news = get_pagination(request.GET.get('page'), queryset)
    stats = stats_items(queryset)

    return render(request, 'item/item_query.html', {'news': news, 'query': query, 'stats': stats})


@login_required
def item_recommend(request):
    news = get_pagination(request.GET.get('page'), get_item_recommend(request.user.profile.id))

    return render(request, 'item/item_recommend.html', {'news': news})


@login_required
def item_search(request):
    news = None
    total = 0
    cleaned_data = request.session.get('cleaned_data', None)

    if request.method == 'POST':
        search_form = ItemSearchForm(request.user, request.POST)

        if search_form.is_valid():
            cleaned_data = search_form.cleaned_data
            if cleaned_data['feed']:
                cleaned_data['feed'] = cleaned_data['feed'].title
            request.session['cleaned_data'] = search_form.cleaned_data

        else:
            print(search_form.errors)
    elif cleaned_data:
        search_form = ItemSearchForm(request.user, initial=cleaned_data)
    else:
        search_form = ItemSearchForm(request.user)

    if cleaned_data:
        query = query_multifield_dict(cleaned_data, request.user.profile.id)
        total = len(query)
        news = get_pagination(request.GET.get('page'), query)

    return render(request, 'item/item_search.html', {'news': news, 'form': search_form, 'total': total})


@login_required
def item_summary(request):
    summary_keywords = get_summary(request.user.id)

    return render(request, 'item/item_summary.html', {'summary_keywords': summary_keywords})


@login_required
def item_saved(request):
    news = get_pagination(request.GET.get('page'), get_item_saved(request.user.id))
    return render(request, 'item/item_saved.html', {'news': news})
