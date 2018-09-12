from rest_framework.authtoken.models import Token
from news.models import User, Profile

NUM_OBJECTS = 3


def authenticate(api):
    for i in range(NUM_OBJECTS):
        username = 'username{}'.format(i)
        password = 'password{}'.format(i)
        user = User.objects.create(username=username, password=password)
        Profile.objects.create(user=user)

        if i == 1:
            api.username = username
            api.password = password
            api.user = user

    api.token = Token.objects.create(user=api.user)
    api.client.credentials(HTTP_AUTHORIZATION='Token ' + api.token.key)


def get_profile(api):
    return Profile.objects.get(user__username=api.username)


def get_entity(entity):
    return type(entity).__name__
