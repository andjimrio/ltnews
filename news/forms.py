from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from news.models import Section, Profile, Comment
from news.service.profile_services import exists_user
from news.service.feed_services import get_feeds_by_user


class UserForm(forms.ModelForm):
    username = forms.CharField(label=_("username"), required=True, widget=forms.TextInput(attrs={'class': 'validate'}))
    email = forms.EmailField(label=_("email"), required=True, widget=forms.EmailInput(attrs={'class': 'validate'}))
    password = forms.CharField(label=_("password"), required=True, widget=forms.PasswordInput())
    repassword = forms.CharField(label=_("repassword"), required=True, widget=forms.PasswordInput())

    def clean(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('repassword'):
            self.add_error('repassword', _("not_passwords"))
        if exists_user(cd.get('username')):
            self.add_error('username', _("user_repeat"))
        return cd

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class FeedForm(forms.Form):
    url = forms.URLField(label=_("link"), widget=forms.URLInput(attrs={'class': 'validate autocomplete'}))
    section = forms.CharField(label=_("section"), widget=forms.TextInput(attrs={'class': 'validate'}))


class ItemSearchForm(forms.Form):
    title = forms.CharField(label=_("title"), required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    creator = forms.CharField(label=_("creator"), required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    description = forms.CharField(label=_("description"), required=False,
                                  widget=forms.TextInput(attrs={'class': 'validate'}))
    feed = forms.ModelChoiceField(label=_("newspaper"), required=False, queryset=None)

    def __init__(self, user, *args, **kwargs):
        super(ItemSearchForm, self).__init__(*args, **kwargs)

        self.fields['feed'].queryset = get_feeds_by_user(user)


class SectionForm(forms.ModelForm):
    title = forms.CharField(label=_("title"), widget=forms.TextInput(attrs={'class': 'validate'}))
    description = forms.CharField(label=_("description"), required=False,
                                  widget=forms.TextInput(attrs={'class': 'validate'}))

    class Meta:
        model = Section
        fields = ('title', 'description')


class UserEditForm(forms.ModelForm):
    username = forms.CharField(label=_("username"), widget=forms.TextInput(attrs={'class': 'validate'}))
    email = forms.EmailField(label=_("email"), widget=forms.EmailInput(attrs={'class': 'validate'}))

    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileForm(forms.ModelForm):
    image = forms.CharField(label=_("image_link"), required=False, widget=forms.URLInput(attrs={'class': 'validate'}))

    class Meta:
        model = Profile
        fields = ('image',)


class CommentForm(forms.ModelForm):
    description = forms.CharField(label=_("comment"),
                                  widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}))

    class Meta:
        model = Comment
        fields = ('description',)
