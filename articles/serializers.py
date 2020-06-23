from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Article, Comment

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'user', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')


class ArticleListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Article
        fields = ('title', 'movieTitle', 'user', 'id', 'created_at')
        read_only_fields = ('created_at', 'id', )


class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    comment = CommentSerializer(source="comment_set", many=True, required=False)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')