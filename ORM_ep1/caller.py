import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
# Create and run your queries within functions
from django.db.models import Q, Count, Avg, F
from main_app.models import Director, Actor, Movie


def get_directors(search_name, search_nationality):
    if search_name is None and search_nationality is None:
        return ""

    query = Q()
    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name and search_nationality:
        query |= query_name & query_nationality
    elif search_name:
        query |= query_name
    elif search_nationality:
        query |= query_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ""
    result = []
    for director in directors:
        result.append(f"Director: {director.full_name}, nationality: {director.nationality}, experience: {director.years_of_experience}")

    return "\n".join(result)


def get_top_director():
    top_director = Director.objects.get_directors_by_movies_count().first()
    if not top_director:
        return ""

    return f"Top Director: {top_director.full_name}, movies: {top_director.num_movies}."


def get_top_actor():
    actor = Actor.objects.annotate(
        num_movies=Count('movies'),
        avg_movies_rating=Avg('movies__rating')
    ).order_by('-num_movies', 'full_name').first()

    if not actor or not actor.num_movies:
        return ""

    movies = ", ".join(movie.title for movie in actor.movies.all() if movie)
    return f"Top Actor: {actor.full_name}, starring in movies: {movies}, movies average rating: {actor.avg_movies_rating:.1f}"


def get_actors_by_movies_count():
    if Movie.objects.all().count() == 0:
        return ""

    actors = Actor.objects.annotate(
        num_movies=Count('movie')
    ).order_by('-num_movies', 'full_name')[:3]

    if not actors or actors[0].num_movies == 0:
        return ""

    result = []
    for actor in actors:
        result.append(f"{actor.full_name}, participated in {actor.num_movies} movies")
    return "\n".join(result)


def get_top_rated_awarded_movie():
    movie = Movie.objects.select_related(
        'starring_actor'
    ).prefetch_related(
        'actors'
    ).filter(
        is_awarded=True
    ).order_by('-rating', 'title').first()

    if not movie:
        return ""

    starring_actor = movie.starring_actor.full_name if movie.starring_actor else "N/A"
    cast = ", ".join([actor.full_name for actor in movie.actors.order_by('full_name')])

    return (f"Top rated awarded movie: {movie.title}, rating: {movie.rating}."
            f" Starring actor: {starring_actor}. Cast: {cast}.")


def increase_rating():
    movies_to_update = Movie.objects.filter(is_classic=True, rating__lt=10)

    if not movies_to_update:
        return "No ratings increased."

    updated_movies = movies_to_update.update(rating=F('rating') + 0.1)
    return f"Rating increased for {updated_movies} movies."
