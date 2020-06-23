from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    survey_genre_id = models.IntegerField(null=True)

    def get_like_genre(self):
        genre_cnt = [0] * 61
        like_movies = self.like_set.all()
        for movie in like_movies.iterator():
            for genre in movie.genres.all().iterator():
                genre_cnt[genre.id] += 1

        return genre_cnt.index(max(genre_cnt))
        