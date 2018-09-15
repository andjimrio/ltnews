from rest_framework import serializers
from news.models import Profile, Section, Feed, Item, User, Comment
from news.utility.populate_utilities import populate_rss


class UserSerializer(serializers.ModelSerializer):
    # TODO Link with Profile
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('user',)


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
