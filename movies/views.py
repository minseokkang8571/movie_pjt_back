from django.shortcuts import render, get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Movie, Genre, Survey_movie
from .serializers import MovieSerializer, SurveyMovieSerializer, MovieLikeSerializer
from django.contrib.auth import get_user_model

import requests
from datetime import datetime
from pprint import pprint
# Create your views here.

@api_view(['GET'])
def survey(request): 
    survey_movie = Survey_movie.objects.all()
    serializer = SurveyMovieSerializer(survey_movie, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_list(request):
    if request.user.is_authenticated:
        like_genre = request.user.get_like_genre()
        if like_genre == 0:
            survey_genre = request.user.survey_genre_id
            if not survey_genre:
                movies = Movie.objects.all().order_by('?')[:10]
            else:
                movies = Movie.objects.filter(genres=survey_genre).order_by('?')[:10]
        else:
            movies = Movie.objects.filter(genres=like_genre).order_by('?')[:10]
    else:
        movies = Movie.objects.all().order_by('?')[:10]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def random_movie(request):
    movies = Movie.objects.all().order_by('?')[:20]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.like.filter(pk=request.user.pk).exists():
        movie.like.remove(request.user)
    else:
        movie.like.add(request.user)
    serializer = MovieLikeSerializer(movie)
    return Response(serializer.data)

# 진흥위원회
@api_view(['GET'])
def boxoffice(request):
    boxoffice_movie = Movie.objects.filter(isboxoffice=True)
    boxoffice_movie.delete()
    KOBIS_KEY = '57300cfaa0a7c61010118d44d33a4c86'
    yy = str(datetime.today().year)
    mm = str(datetime.today().month)
    dd = str(datetime.today().day - 1)
    if len(mm) == 1: 
        mm = '0' + mm
    if len(dd) == 1: 
        dd = '0' + mm
    targetDt = yy + mm + dd # 날짜입력 YYYYMMDD
    KOBIS_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?'
    
    response = requests.get(KOBIS_URL + '&key=' + KOBIS_KEY + '&targetDt=' + targetDt)
    kobisData = response.json().get('boxOfficeResult').get('dailyBoxOfficeList')
    release_arr = []

    KMDM_KEY = 'C850PKA90E2I7S5790PV'
    KMDB_URL = 'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?'
    detail = 'Y'
    collection = 'kmdb_new2'
    for i in range(0, 10):
        title = kobisData[i].get('movieNm')
        if title[0] in '@#/<>:-+=!~$%&*()': # title의 첫 글자에 특수문자가 들어가면 제대로 응답이 이루어지지 않음
            title = title[1:]
        releaseDts = (kobisData[i].get('openDt'))
        response = requests.get(KMDB_URL + 'ServiceKey=' + KMDM_KEY + '&collection=' + collection + '&detail=' + detail + '&title=' + title + '&releaseDts=' + releaseDts)
        kmdbData = response.json().get('Data')[0].get('Result')
        if kmdbData:
            for item in kmdbData:
                try:
                    movie = Movie()
                    movie.title =  item.get('title').replace('!HS ', '').replace(' !HE', '').replace('   ', ' ').replace('  ', ' ').strip()
                    movie.original_title = item.get('titleOrg')
                    date = item.get('repRlsDate')
                    if date:
                        movie.release_date = date[:4] + '-' + date[4:6] + '-' + date[6:]
                    else:
                        continue
                    movie.runtime = item.get('runtime')
                    if not item.get('posters'):
                        continue
                    movie.poster_path = item.get('posters')
                    movie.overview = item.get('plots').get('plot')[0].get('plotText')
                    if '불가' in item.get('rating'):
                        movie.adult = True
                    else:
                        movie.adult = False
                    if item.get('awards1') or item.get('awards2'):
                        movie.award = True
                    else:
                        movie.award = False
                    movie.keywords = item.get('keywords')
                    movie.director = item.get('directors').get('director')[0].get('directorNm')
                    actors = ""
                    for cnt, actor in enumerate(item.get('actors').get('actor')):
                        if cnt == 5: 
                            break
                        if actors:
                            actors = actors + ", " + actor.get('actorNm')
                        else:
                            actors = actor.get('actorNm')
                    movie.actors = actors
                    movie.produce_year = item.get('prodYear')
                    movie.nation = item.get('nation')
                    movie.rating = item.get('rating')
                    movie.isboxoffice = True
                    movie.stills = item.get('stlls')
                    movie.save()
                except:
                    continue

                for genre in item.get('genre').split(','):
                    if genre:
                        try:
                            exist_g = Genre.objects.get(name=genre)
                            movie.genres.add(exist_g)
                        except:
                            new_g = Genre(name=genre)
                            new_g.save()
                            movie.genres.add(new_g)

    boxoffice_movie = Movie.objects.filter(isboxoffice=True)
    serializer = MovieSerializer(boxoffice_movie, many=True)

    return Response(serializer.data)

# kmdb
@api_view(['GET'])
def api(request):
    KEY = 'C850PKA90E2I7S5790PV'
    collection = 'kmdb_new2'
    detail = 'Y'
    listCount = '100'
    releaseDts = '20000101' # 날짜입력 YYYYMMDD
    API_URL = 'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?'
    
    for startCount in range(0, 3000, 100):

        response = requests.get(API_URL + '&ServiceKey=' + KEY + '&collection=' + collection + '&detail=' + detail + '&listCount=' + listCount + '&releaseDts=' + releaseDts + "&startCount=" + str(startCount))
        jsonData = response.json().get('Data')[0].get('Result')
        context = {
            'jsonData': jsonData,
        }
        for item in jsonData:
            try:
                movie = Movie()
                movie.title = item.get('title')
                movie.original_title = item.get('titleOrg')
                date = item.get('repRlsDate')
                if date:
                    movie.release_date = date[:4] + '-' + date[4:6] + '-' + date[6:]
                else:
                    continue
                movie.runtime = item.get('runtime')
                if not item.get('posters'):
                    continue
                movie.poster_path = item.get('posters')
                movie.overview = item.get('plots').get('plot')[0].get('plotText')
                if '불가' in item.get('rating'):
                    movie.adult = True
                else:
                    movie.adult = False
                if item.get('awards1') or item.get('awards2'):
                    movie.award = True
                else:
                    movie.award = False
                movie.keywords = item.get('keywords')
                movie.director = item.get('directors').get('director')[0].get('directorNm')
                actors = ""
                for cnt, actor in enumerate(item.get('actors').get('actor')):
                    if cnt == 5: 
                        break
                    if actors:
                        actors = actors + ", " + actor.get('actorNm')
                    else:
                        actors = actor.get('actorNm')
                movie.actors = actors
                movie.produce_year = item.get('prodYear')
                movie.nation = item.get('nation')
                movie.rating = item.get('rating')
                movie.isboxoffice = False
                movie.stills = item.get('stlls')
                movie.save()
            except:
                continue

            for genre in item.get('genre').split(','):
                if genre:
                    try:
                        exist_g = Genre.objects.get(name=genre)
                        movie.genres.add(exist_g)
                    except:
                        new_g = Genre(name=genre)
                        new_g.save()
                        movie.genres.add(new_g)

    return render(request, 'movies/api.html', context)



