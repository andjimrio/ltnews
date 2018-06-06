from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from news.forms import UserEditForm, ProfileForm
from news.service.profile_services import get_profile, get_status_read_stats_by_user, get_status_like_stats_by_user


@login_required
def profile_view(request):
    profile = get_profile(request.user.id)
    read_stats = get_status_read_stats_by_user(profile.id)
    like_stats = get_status_like_stats_by_user(profile.id)
    return render(request, 'profile/profile_view.html', {'profile': profile, 'read_stats': read_stats,
                                                         'like_stats': like_stats})


@login_required
def profile_edit(request):
    user_form = UserEditForm(request.POST or None, instance=request.user)
    profile_form = ProfileForm(request.POST or None, instance=get_profile(request.user.id))

    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        return redirect('profile_view')
    else:
        print(user_form.errors)
        print(profile_form.errors)

    return render(request, 'profile/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})