from django.db import models
from django.conf import settings

class Genre(models.Model):
    name = models.CharField(max_length=20)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    release_date = models.DateField()
    runtime = models.IntegerField()
    poster_path = models.TextField()
    overview = models.TextField() # plot
    adult = models.BooleanField() # rating
    genres = models.ManyToManyField(Genre, related_name="movies")
    award = models.BooleanField()
    keywords = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    actors = models.TextField()
    produce_year = models.CharField(max_length=30)
    nation = models.CharField(max_length=30)
    rating = models.CharField(max_length=30)
    isboxoffice = models.BooleanField()
    like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name='like_set')
    stills = models.TextField()

class Survey_movie(models.Model):
    title = models.CharField(max_length=100)
    poster_path = models.TextField()
    genres = models.ManyToManyField(Genre, related_name="survey_movies")
