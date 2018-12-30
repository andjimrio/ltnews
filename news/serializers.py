from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from news.models import Profile, Section, Feed, Item, User, Comment
from news.utility.populate_utilities import populate_rss


class UserRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    image = serializers.URLField(required=False)

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

    def create(self, validated_data):
        super().create(validated_data)

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save(update_fields=['first_name', 'last_name'])

        image = self.validated_data.get('image', '')
        Profile.objects.create(user=user, image=image)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class FeedSerializer(serializers.ModelSerializer):
    sections = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Feed
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    feeds = FeedSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        exclude = ('user',)


class FeedFormSerializer(serializers.Serializer):
    url = serializers.URLField()
    section = serializers.CharField()
    user_id = serializers.IntegerField()

    def create(self, validated_data, user=None):
        return populate_rss(validated_data['url'], validated_data['section'], validated_data['user_id'])

    def update(self, instance, validated_data):
        pass


class ItemSerializer(serializers.ModelSerializer):
    feed = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Item
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
