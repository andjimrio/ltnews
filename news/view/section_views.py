from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from news.models import Section
from news.forms import SectionForm
from news.services import get_pagination, check_user
from news.service.section_services import get_section_items, delete_section


@login_required
def section_view(request, section_id):
    section = get_object_or_404(Section, pk=section_id)
    check_user(section, request.user)
    news = get_pagination(request.GET.get('page'), get_section_items(section_id))

    return render(request, 'section/section_view.html', {'section': section, 'news': news})


@login_required
def section_edit(request, section_id):
    section = get_object_or_404(Section, pk=section_id)
    check_user(section, request.user)

    section_form = SectionForm(request.POST or None, instance=section)

    if section_form.is_valid():
        section_form.save()
        return redirect('section_view', section_id=section_id)
    else:
        print(section_form.errors)

    return render(request, 'section/section_edit.html', {'section_form': section_form, 'section_id': section.id})


@login_required
def section_delete(request, section_id):
    delete_section(section_id, request.user.id)
    return redirect('feed_list')