import os
import django
from django.core.exceptions import ValidationError



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


# Import your models here
from main_app.models import Book

# Create queries within functions

book = Book(
    title="Short Title",
    description="A book with a short title.",
    genre="Fiction",
    author="A",
    isbn="1234"
)

try:
    book.full_clean()
    book.save()

except ValidationError as e:
    print("Validation Error for Book:")
    for field, errors in e.message_dict.items():
        print(f"{field}: {', '.join(errors)}")

