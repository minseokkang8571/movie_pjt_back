from rest_framework import serializers
from .models import Movie, Survey_movie, Genre

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['name']

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, required=False)

    class Meta:
        model = Movie
        fields = '__all__'
        read_only_fields = ['id']

class MovieLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['like']

class SurveyMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Survey_movie
        fields = '__all__'
        read_only_fields = ['id']