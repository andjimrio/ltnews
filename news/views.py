from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from news.forms import UserForm


def index(request):
    return render(request, 'index.html', {})


def bad_request(request):
    return render(request, 'errors/error400.html', {})


def permission_denied(request):
    return render(request, 'errors/error403.html', {})


def page_not_found(request):
    return render(request, 'errors/error404.html', {})


def server_error(request):
    return render(request, 'errors/error500.html', {})


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            Profile.objects.get_or_create(user_id=user.id)

            # Para el auto-login al crear un usuario
            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password'])

            if user is not None:
                login(request, new_user)

            return redirect('feed_list')

        else:
            print(user_form.errors)

    else:
        user_form = UserForm()

    return render(request, 'register.html', {'user_form': user_form})
