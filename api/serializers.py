from rest_framework import serializers

from main.models import Bb, Comment


class BbSerializer(serializers.ModelSerializer):
    """Сериализатор для списка объявлений"""
    class Meta:
        model = Bb
        fields = ('id', 'title', 'content', 'price', 'created_at')


class BbDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для подробной информации о выбранном объявлении"""
    class Meta:
        model = Bb
        fields = ('id', 'title', 'content', 'price', 'created_at', 'contacts', 'image')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""
    class Meta:
        model = Comment
        fields = ('bb', 'author', 'content', 'created_at')
