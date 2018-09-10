from rest_framework import serializers
from news.models import Profile, Section, Feed, Item
from news.utility.populate_utilities import populate_rss


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'title', 'description')


class FeedSerializer(serializers.ModelSerializer):
    sections = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Feed
        fields = '__all__'


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
