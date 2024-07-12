import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Article, Review
from django.db.models import Q, Count, Avg
from django.core.exceptions import ObjectDoesNotExist


# Create and run your queries within functions


def get_authors(search_name=None, search_email=None):

    if search_name is None and search_email is None:
        return ""

    query = Q()
    if search_name and search_email:
        query = Q(full_name__icontains=search_name) & Q(email__icontains=search_email)
    elif search_name:
        query = Q(full_name__icontains=search_name)
    elif search_email:
        query = Q(email__icontains=search_email)

    authors = Author.objects.filter(query).order_by('-full_name')

    if not authors:
        return ""

    return "\n".join(
        f"Author: {a.full_name}, email: {a.email}, status: {'Banned' if a.is_banned else 'Not Banned'}"
        for a in authors
    )


def get_top_publisher():
    top_author = Author.objects.annotate(
            num_articles=Count('articles')
        ).filter(
            num_articles__gt=0
        ).order_by(
            '-num_articles',
            'email'
        ).first()

    if not top_author or not Article.objects.all().exists():
        return ""

    return f"Top Author: {top_author.full_name} with {top_author.num_articles} published articles."


def get_top_reviewer():
    top_reviewer = Author.objects.annotate(
            num_reviews=Count('reviews')
        ).filter(
            num_reviews__gt=0
        ).order_by(
            '-num_reviews',
            'email'
        ).first()

    if not top_reviewer:
        return ""

    return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.num_reviews} published reviews."


def get_latest_article():
    last_article = Article.objects.prefetch_related('article_reviews').last()

    if last_article is None:
        return ""

    avg_rating = last_article.article_reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0.0
    authors_names = ", ".join(sorted(author.full_name for author in last_article.authors.all()))

    return (f"The latest article is: {last_article.title}. Authors: {authors_names}. "
            f"Reviewed: {last_article.article_reviews.count()} times. Average Rating: {avg_rating:.2f}.")


def get_top_rated_article():
    top_article = Article.objects.annotate(
        avg_rating=Avg('article_reviews__rating')
    ).order_by(
        '-avg_rating',
        'title'
    ).first()

    if not top_article or top_article.article_reviews.count() == 0:
        return ""

    average_rating = top_article.avg_rating if top_article.avg_rating else 0.00
    return (f"The top-rated article is: {top_article.title}, with an average rating of "
            f"{average_rating:.2f}, reviewed {top_article.article_reviews.count()} times.")


def ban_author(email=None):
    if email is None:
        return "No authors banned."

    try:
        author = Author.objects.get(email=email)
    except ObjectDoesNotExist:
        return "No authors banned."

    num_reviews = author.reviews.count()
    author.reviews.all().delete()
    author.is_banned = True
    author.save()

    return f"Author: {author.full_name} is banned! {num_reviews} reviews deleted."



