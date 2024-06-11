import os
import django
from django.db.models import Count, Avg, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Actor, Director, Movie

# Create and run your queries within functions


def get_directors(search_name=None, search_nationality=None):

    if not search_name and not search_nationality:
        return ""

    if search_name and search_nationality:
        directors = Director.objects.filter(
            full_name__icontains=search_name,
            nationality__icontains=search_nationality
        ).order_by('full_name')
    elif search_name:
        directors = Director.objects.filter(
            full_name__icontains=search_name
        ).order_by('full_name')
    elif search_nationality:
        directors = Director.objects.filter(
            nationality__icontains=search_nationality
        ).order_by('full_name')

    if not directors:
        return ""

    result = []
    for director in directors:
        result.append(
            f"Director: {director.full_name}, nationality: {director.nationality}, experience: {director.years_of_experience}")

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

    top_actors = Actor.objects.annotate(
        num_movies=Count('movie')
    ).order_by(
        '-num_movies',
        'full_name'
    )[:3]

    if not top_actors or top_actors[0].num_movies == 0:
        return ""

    result = []
    for actor in top_actors:
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
    updated_movies = Movie.objects.filter(
        is_classic=True,
        rating__lt=10.0
    ).update(
        rating=F('rating') + 0.1
    )

    if not updated_movies:
        return "No ratings increased."

    return f"Rating increased for {updated_movies} movies."